import shutil
import os
from config_start import database, lama_developer_credentials, lama_user_credentials
from dulwich import porcelain
from dulwich.index import build_index_from_tree
import stat
import posixpath
from urllib3.exceptions import MaxRetryError, ProtocolError
import socket
import tempfile, time, ssl
from contextlib import contextmanager
import json
import urllib.request

def check_internet_connection():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        return False

    # try:
    #     urlopen('http://216.58.192.142') ## IP for google
    #     return True
    # except URLError:
    #     return False




def git_clone_repo(errstream=None):
    try:
        porcelain.clone(
            source="https://github.com/chrisiweb/lama_latest_update.git",
            target=database,
            checkout=True,
            errstream=errstream,
            )
        return True
    except Exception as e:
        return e


def list_all_files(store, treeid, base=None, list_of_all_files=None):
    if list_of_all_files == None:
        _list = []
    else:
        _list = list_of_all_files

    for (name, mode, sha) in store[treeid].iteritems():   
        if base != None:
            name = posixpath.join(base, name)

        _list.append(name)

        if stat.S_ISDIR(mode):
            list_all_files(store, sha, name, list_of_all_files=_list)
    return _list

def resolve_divergence():
    head = os.path.join(database, '.git', 'refs', 'heads', 'master')
    origin = os.path.join(database, '.git', 'refs', 'remotes', 'origin', 'master')
    shutil.copyfile(origin, head)

def restore_working_tree():
    repo = porcelain.Repo(database)
    repo._worktree_path = database

    branch_ref = b"refs/remotes/origin/master"
    commit = repo[branch_ref]          # Commit-Objekt
    tree_id = commit.tree              # SHA des Trees, nicht das Objekt selbst

    # Jede Datei aus dem Tree neu schreiben
    for entry_path, mode, sha in repo.object_store.iter_tree_contents(tree_id):
        abs_path = os.path.join(database, entry_path.decode())
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        blob = repo.object_store[sha]
        with open(abs_path, "wb") as f:
            f.write(blob.data)

    print("📄 Alle Dateien aus origin/master neu geschrieben.")



# ========== Mutex gegen parallele Refresh-Läufe ==========
class FileMutex:
    def __init__(self, name="lama_refresh.lock", dir=None):
        if dir is None:
            dir = tempfile.gettempdir()
        self.path = os.path.join(dir, name)

    def acquire(self, timeout=5, poll=0.1):
        t0 = time.time()
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                return True
            except FileExistsError:
                if (time.time() - t0) > timeout:
                    return False
                time.sleep(poll)

    def release(self):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass

@contextmanager
def refresh_mutex():
    m = FileMutex()
    ok = m.acquire()
    try:
        if not ok:
            raise RuntimeError("Ein anderer Aktualisierungsvorgang läuft bereits.")
        yield
    finally:
        if ok:
            m.release()


# ========== Watcher/Leser kurz pausieren (No-Op, falls du keine Watcher hast) ==========
def suspend_watchers(self_obj, enabled: bool):
    try:
        self_obj._suspend_watchers_flag = bool(enabled)
        # Falls du QFileSystemWatcher / watchdog nutzt:
        # self_obj.watcher.stop() / self_obj.watcher.start(paths)
    except Exception:
        pass


# ========== Atomisch schreiben (Temp -> os.replace) mit Backoff ==========
def atomic_write_bytes(data: bytes, target_path: str, retries=12, base_delay=0.05):
    target_dir = os.path.dirname(target_path)
    os.makedirs(target_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix="_db_", dir=target_dir)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        for i in range(retries):
            try:
                os.replace(tmp_path, target_path)  # „atomic enough“ auf Windows
                return True
            except PermissionError:  # [WinError 32]: Datei kurz gesperrt
                time.sleep(base_delay * (2 ** i))
        raise PermissionError(f"Konnte {target_path} nicht ersetzen (Datei in Benutzung).")
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

def atomic_write_json(obj, target_path: str, **kwargs):
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
    return atomic_write_bytes(data, target_path, **kwargs)


# ========== Download -> atomisches Ablegen ==========
def download_atomic(url: str, target_path: str, retries=12, base_delay=0.05, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "LaMA/1.0"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = resp.read()
    atomic_write_bytes(data, target_path, retries=retries, base_delay=base_delay)
    return data  # optional, wenn du die Inhalte gleich weiterverarbeiten willst


# ========== Lesen mit kleinem Retry (falls Virenscanner kurz blockiert) ==========
def read_json_with_retry(path: str, retries=6, base_delay=0.05):
    last = None
    for i in range(retries):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (PermissionError, OSError) as e:
            last = e
            time.sleep(base_delay * (2 ** i))
    if last:
        raise last


# ========== Dulwich/Git: Index sanft neu bauen, falls nicht vorhanden ==========
def ensure_git_index(repo_path: str):
    git_dir = os.path.join(repo_path, ".git")
    index_path = os.path.join(git_dir, "index")
    if not os.path.isdir(git_dir):
        return
    if os.path.exists(index_path):
        return
    try:
        from dulwich.repo import Repo
        from dulwich.index import build_index_from_tree
        repo = Repo(repo_path)
        head = repo.head()
        build_index_from_tree(repo.path, index_path, repo.object_store, repo[head].tree)
    except Exception:
        # Keine harte Eskalation – Refresh soll trotzdem weiterlaufen
        pass


# ====== (G) Generischer Retry-Wrapper (für Reset/Clean/Remove) ======
def with_retry(fn, *, attempts=8, base_delay=0.05, catch=(PermissionError,)):
    for i in range(attempts):
        try:
            return fn()
        except catch:
            time.sleep(base_delay * (2 ** i))
    # letzter Versuch ohne try, damit Ausnahme sichtbar bleibt
    return fn()


# ===== Hilfsfunktionen zum Löschen unter Windows mit Backoff =====
def _robust_remove(path):
    # Win: schreibgeschützte Dateien zuerst entsperren
    try:
        os.chmod(path, 0o666)
    except Exception:
        pass
    os.remove(path)

def _robust_rmdir(path):
    # Leeres Verzeichnis entfernen; bei Bedarf rekursiv anpassen
    try:
        os.rmdir(path)
    except OSError:
        # Notfalls rekursiv
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                _robust_remove(os.path.join(root, name))
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception:
                    pass
        os.rmdir(path)


def git_reset_repo_to_origin():
    try:
        ensure_git_index(database)
        repo = porcelain.Repo(database)
        # porcelain.fetch(repo)
        with_retry(lambda: porcelain.fetch(repo), attempts=3, base_delay=0.2, catch=(Exception,))

        try:

            head_commit = repo[b'refs/heads/master']
            origin_commit = repo[b'refs/remotes/origin/master']
            
            # tree_head_id = repo[repo[b'refs/heads/master'].tree].id
            # tree_origin_master_id = repo[repo[b'refs/remotes/origin/master'].tree].id

            store=repo.object_store

            tree_head_id = head_commit.tree
            tree_origin_master_id = origin_commit.tree

            list_all_files_head = list_all_files(store, tree_head_id)
            list_all_files_origin_master = list_all_files(store, tree_origin_master_id)



            deleted_files = list(set(list_all_files_head) - set(list_all_files_origin_master))
        except Exception:
            deleted_files = []

        for entry in deleted_files:
            try:
                file_path = os.path.join(database, entry.decode('utf-8'))
            except AttributeError:
                file_path = os.path.join(database, entry)
            if os.path.isfile(file_path):
                with_retry(lambda: _robust_remove(file_path), attempts=12, base_delay=0.05)
            elif os.path.isdir(file_path):
                # Falls Verzeichnisse in der Liste vorkommen sollten
                with_retry(lambda: _robust_rmdir(file_path), attempts=12, base_delay=0.05)


        # if deleted_files !=[]:
        #     for all in deleted_files:
        #         file_path = os.path.join(database, all.decode('utf-8'))
        #         os.remove(file_path)

        try:
            status = porcelain.status(repo)
            if status.unstaged:
                repo.stage(status.unstaged)
                porcelain.commit(repo, message="delete files")
        except Exception:
            # Nicht fatal – wir setzen trotzdem hart zurück
            pass

            # status=porcelain.status(repo) 

            # repo.stage(status.unstaged)

            # porcelain.commit(repo, message="delete files")


        # 5) harter Reset auf origin/master (mit Retry bei WinError 32)
        with_retry(
            lambda: porcelain.reset(repo, "hard", treeish=b"refs/remotes/origin/master"),
            attempts=12, base_delay=0.05, catch=(PermissionError,)
        )

        # 6) clean Working Tree (ebenfalls mit Retry)
        with_retry(
            lambda: porcelain.clean(repo=repo, target_dir=database),
            attempts=12, base_delay=0.05, catch=(PermissionError,)
        )

        # 7) (Optional) Divergenz-Routine (dein Code)
        try:
            resolve_divergence()
        except Exception:
            pass

        # 8) Index nachziehen (manchmal nötig nach Reset/Clean)
        try:
            ensure_git_index(database)
        except Exception:
            pass

        try:
            repo.close()  # Deskriptoren freigeben
        except Exception:
            pass

        return True


    except PermissionError as e:
        print('PermissionError')
        return e
    except MaxRetryError as e:
        print('MaxRetryError')
        return e
    except ProtocolError as e:
        print('ProtocolError')
        return e

        ###working###
        # porcelain.reset(repo, "hard", treeish=b"refs/remotes/origin/master")

        # porcelain.clean(repo=repo, target_dir=database)

        # resolve_divergence()
        ########


        return True

    except PermissionError as e:
        print('PermissionError')
        return e
    
    except MaxRetryError as e:
        print('MaxRetryError')
        return e

    except ProtocolError as e:
        print('ProtocolError')
        return e



def create_dir_if_not_existing(path):
    if os.path.isdir(path) == False:
        os.mkdir(path)

def copy_all_changed_files(staged_files):
    git_temp = os.path.join(database,".git", "git_temp")
    git_temp_add = os.path.join(git_temp, "add")
    git_temp_modify = os.path.join(git_temp, "modify")
    if os.path.isdir(git_temp) == False:
        create_dir_if_not_existing(git_temp)
        create_dir_if_not_existing(git_temp_add)
        create_dir_if_not_existing(git_temp_modify)

    with open(os.path.join(database, ".git", "git_temp", "staged_files"), "w") as file:
        file.write(str(staged_files))

    if staged_files['add'] != []:
        for all in staged_files['add']:
            filename=os.path.basename(all)
            shutil.copyfile(os.path.join(database,all.decode()), os.path.join(git_temp_add, filename.decode()))

    if staged_files['modify'] != []:
        for all in staged_files['modify']:
            filename=os.path.basename(all)
            shutil.copyfile(os.path.join(database,all.decode()), os.path.join(git_temp_modify, filename.decode()))


def restore_all_changes():
    with open(os.path.join(database, ".git", "git_temp", "staged_files"), "r") as file:
        staged_files = file.read()
    staged_files = eval(staged_files)

    git_temp = os.path.join(database,".git", "git_temp")
    git_temp_add = os.path.join(git_temp, "add")
    git_temp_modify = os.path.join(git_temp, "modify")

    for all in staged_files['add']:
        filename=os.path.basename(all)
        backup_path = os.path.join(git_temp_add, filename.decode())
        move_path = os.path.join(database, all.decode())
        shutil.move(backup_path, move_path)

    for all in staged_files['delete']:
        remove_path = os.path.join(database, all.decode())
        os.remove(remove_path)

    for all in staged_files['modify']:
        filename=os.path.basename(all)
        backup_path = os.path.join(git_temp_modify, filename.decode())
        move_path = os.path.join(database, all.decode())
        shutil.move(backup_path, move_path)

def get_access_token(mode):
    credential_path = os.path.join(database, "_config")
    if mode == 'developer':
        _file_1 = lama_developer_credentials
        with open(_file_1, "r", encoding="utf-8") as f:
            credentials_1 = f.read()
        _center_ = "fb108a5430"
        _file_2 = os.path.join(credential_path, "developer_credentials.txt")

    if mode == 'user':
        credentials_1 = lama_user_credentials
        _center_ = "WSPUnRFoMX"
        _file_2 = os.path.join(credential_path, "user_credentials.txt")


    with open(_file_2, "r", encoding="utf-8") as f:
        credentials_2 = f.read()
    access_token = credentials_1 + _center_ + credentials_2

    return access_token 


def check_branches():
    repo = porcelain.open_repo(database)
    porcelain.fetch(repo)

    head_id = repo[b'refs/heads/master'].id
    origin_id = repo[b'refs/remotes/origin/master'].id

    if head_id == origin_id:
        print("Branches are the same ...")
        return True
    else:
        print("Branches diverge ...")
        return False


def git_push_to_origin(ui, admin, file_list, message, worker_text):
        # local_appdata = os.getenv('LOCALAPPDATA')
        # credentials_file = os.path.join(os.getenv('LOCALAPPDATA'),"LaMA", "credentials","developer_credentials.txt")

        if admin == True:
            access_token = get_access_token('developer')
        else:
            access_token = get_access_token('user')

        repo = porcelain.open_repo(database)
        if admin == True:
            status = porcelain.status(repo)
            repo.stage(status.unstaged + status.untracked)

            if status.unstaged==[] and status.untracked == []:
                # information_window("Es wurden keine Änderungen gefunden.")
                return False
        

        
        for file in file_list:
            file_path = os.path.join(database, file)
            porcelain.add(repo, paths= file_path)

        ui.label.setText("{} (27%)".format(worker_text))

        if admin == True:
            mode = 'Administrator'
        else:
            mode = 'User'

        porcelain.commit(repo, message="New Update ({0}) - {1}".format(mode, message))
        ui.label.setText("{} (84%)".format(worker_text))
        i = 0
        while True:
            try:
                porcelain.push(repo,"https://lama-user:{}@github.com/chrisiweb/lama_latest_update.git".format(access_token),"master")
                break
            except Exception as e:
                print(e)
                value = 84 + i*5
                ui.label.setText(f"{worker_text} ({value}%)")
                if i == 3: 
                    return e
                i += 1
        ui.label.setText("{} (100%)".format(worker_text))        

        return True


def _to_str_path(p):
    # Dulwich kann bytes ODER str liefern, je nach Version/Plattform
    if isinstance(p, bytes):
        return p.decode("utf-8", errors="surrogateescape")
    return p  # bereits str


def check_for_changes(database):
    repo = porcelain.Repo(database)
    repo._worktree_path = database
    status = porcelain.status(repo)
    untracked = [_to_str_path(p) for p in status.untracked]
    changed = []

    head_commit = repo[b"HEAD"]
    tree_id = head_commit.tree
    blob_map = {path: sha for path, mode, sha in repo.object_store.iter_tree_contents(tree_id)}

    for path_b in status.unstaged:
        abs_path = os.path.join(database, path_b.decode("utf-8"))
        if not os.path.exists(abs_path):
            changed.append(path_b.decode())
            continue

        blob_sha = blob_map.get(path_b)
        if not blob_sha:
            changed.append(path_b.decode())
            continue

        blob_data = repo.object_store[blob_sha].data
        with open(abs_path, "rb") as f:
            file_data = f.read()

        if blob_data != file_data:
            changed.append(path_b.decode())

    return changed, untracked



def check_for_lokal_repo_changes():
    repo = porcelain.Repo(database)
    repo._worktree_path = database
    status = porcelain.status(repo)
    untracked = [p.decode("utf-8") for p in status.untracked]
    changed = []

    head_commit = repo[b"HEAD"]
    tree_id = head_commit.tree
    blob_map = {path: sha for path, mode, sha in repo.object_store.iter_tree_contents(tree_id)}

    for path_b in status.unstaged:
        abs_path = os.path.join(database, path_b.decode("utf-8"))
        if not os.path.exists(abs_path):
            changed.append(path_b.decode())
            continue

        blob_sha = blob_map.get(path_b)
        if not blob_sha:
            changed.append(path_b.decode())
            continue

        blob_data = repo.object_store[blob_sha].data
        with open(abs_path, "rb") as f:
            file_data = f.read()

        if blob_data != file_data:
            changed.append(path_b.decode())

    return {"unstaged": changed, "untracked": untracked}
