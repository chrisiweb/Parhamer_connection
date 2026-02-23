import shutil
import os
from config_start import database, lama_developer_credentials, lama_user_credentials
from dulwich import porcelain
from dulwich.index import build_index_from_tree
import stat
import posixpath
from urllib3.exceptions import MaxRetryError, ProtocolError
import socket



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


# # In git_sync.py
# import os
# import shutil
# import stat
# import time
# from dulwich import porcelain
# from dulwich.repo import Repo
# from dulwich.index import build_index_from_tree

# Optional: Wenn du LOG-Ausgaben willst, setze VERBOSE=True
VERBOSE = False

def _log(msg):
    if VERBOSE:
        print(msg)

def _ensure_writable(path):
    try:
        mode = os.stat(path).st_mode
        # Schreibschutz entfernen (Windows/Unix)
        os.chmod(path, mode | stat.S_IWUSR)
    except FileNotFoundError:
        pass
    except PermissionError:
        pass

def _iter_tracked_paths_from_tree(object_store, tree_id):
    """Gibt ein Set aller relativem Pfade (mit /) im Tree zurück."""
    tracked = set()
    for p_b, mode, sha in object_store.iter_tree_contents(tree_id):
        tracked.add(p_b.decode("utf-8"))
    return tracked

IGNORED_PATHS = {
    "_local_database.json",
    "Bilder_local",
    "Bilder_local/",
    "Bilder_addon",
    "Bilder_addon/",
    "_database_addon.json",
}

def _remove_untracked_files(workdir, tracked_paths):
    """
    Löscht alle Dateien/Ordner unter workdir, die nicht getrackt sind und nicht in IGNORED_PATHS stehen.
    - Dateien: exakte Matches ignorieren
    - Ordner: Prefix-Match (alles darunter bleibt erhalten)
    - .git bleibt unberührt
    """
    # --- Normalisierung ---
    def norm(p: str) -> str:
        return p.replace("\\", "/").lstrip("./").rstrip("/")

    # tracked normalisieren
    tracked_paths = {norm(p) for p in tracked_paths}

    # ignore normalisieren
    ignore_set = {norm(p) for p in IGNORED_PATHS}

    # Hilfsfunktion: ist path ignoriert (Datei ODER liegt unter ignoriertem Ordner)?
    def is_ignored(rel_path: str) -> bool:
        rp = norm(rel_path)
        if rp in ignore_set:
            return True
        for ign in ignore_set:
            if ign and rp.startswith(ign + "/"):
                return True
        return False

    git_dir = os.path.join(workdir, ".git")
    git_dir_norm = norm(os.path.relpath(git_dir, workdir))

    # --- Walk: topdown=True, damit wir in ignorierte Ordner gar nicht absteigen ---
    for root, dirs, files in os.walk(workdir, topdown=True):
        rel_root = norm(os.path.relpath(root, workdir))

        # .git niemals anfassen / betreten
        # (Falls wir zufällig im .git sind oder darunter)
        if rel_root == git_dir_norm or rel_root.startswith(git_dir_norm + "/"):
            # prunen: weder Dateien noch Unterordner unter .git bearbeiten
            dirs[:] = []
            continue

        # PRUNING: ignorierte Ordner NICHT betreten
        # (alles darunter soll unangetastet bleiben)
        pruned = []
        for d in list(dirs):
            rel_dir = norm(os.path.join(rel_root, d)) if rel_root else norm(d)
            if is_ignored(rel_dir):
                pruned.append(d)
        # entferne ignorierte Ordner aus dirs -> os.walk steigt dort nicht ein
        dirs[:] = [d for d in dirs if d not in pruned]

        # Dateien behandeln
        for f in files:
            rel_file = norm(os.path.join(rel_root, f)) if rel_root else norm(f)

            # ignorierte Datei behalten
            if is_ignored(rel_file):
                continue

            # untracked -> löschen
            if rel_file not in tracked_paths:
                full = os.path.join(root, f)
                _ensure_writable(full)
                try:
                    os.remove(full)
                    _log(f"Removed untracked file: {rel_file}")
                except Exception:
                    pass

    # Zweiter Durchlauf (bottom-up), um LEERE Ordner zu löschen, die NICHT ignoriert sind
    for root, dirs, files in os.walk(workdir, topdown=False):
        rel_root = norm(os.path.relpath(root, workdir))

        # .git niemals löschen
        if rel_root == git_dir_norm or rel_root.startswith(git_dir_norm + "/"):
            continue

        # ignorierte Ordner niemals löschen
        if is_ignored(rel_root):
            continue

        # workdir selbst nicht löschen
        if rel_root == "." or rel_root == "":
            continue

        # nur leere Ordner entfernen
        try:
            if not os.listdir(root):
                os.rmdir(root)
        except Exception:
            pass


def _checkout_tree_to_workdir(repo, tree_id, workdir):
    """Schreibt alle Blobs aus dem Tree in den Arbeitsbaum (legt Ordner an, setzt Ausführbarkeit bestmöglich)."""
    store = repo.object_store
    for p_b, mode, sha in store.iter_tree_contents(tree_id):
        rel = p_b.decode("utf-8")
        abspath = os.path.join(workdir, rel)
        os.makedirs(os.path.dirname(abspath), exist_ok=True)
        blob = store[sha]
        _ensure_writable(abspath)
        with open(abspath, "wb") as f:
            f.write(blob.data)
        # Ausführbarkeit setzen, falls im Git-Mode angegeben
        try:
            if mode & stat.S_IXUSR:  # executable bit
                cur = os.stat(abspath).st_mode
                os.chmod(abspath, cur | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        except Exception:
            pass

def _detect_remote_target_ref(repo, remote=b"origin", prefer_branch=None):
    """
    Ermittelt ein sinnvolles Ziel-Ref auf dem Remote:
    - prefer_branch (falls angegeben)
    - sonst origin/HEAD
    - sonst origin/master
    - sonst origin/main
    """
    refs = repo.refs
    if prefer_branch:
        cand = f"refs/remotes/{remote.decode()}/{prefer_branch}".encode()
        if cand in refs:
            return cand

    # origin/HEAD ist oft Symbolik auf master oder main
    origin_head = f"refs/remotes/{remote.decode()}/HEAD".encode()
    if origin_head in refs:
        # Das hier gibt meist direkt die Ziel-Ref zurück
        try:
            head_target = refs.read_ref(origin_head)  # kann die Ziel-Ref liefern
            if head_target in refs:
                return head_target
        except Exception:
            pass

    for name in (b"refs/remotes/%s/master" % remote, b"refs/remotes/%s/main" % remote):
        if name in refs:
            return name

    raise RuntimeError("Konnte keinen geeigneten Remote-Branch finden (origin/HEAD, origin/master, origin/main fehlen).")

def _force_move_head_and_branch(repo, local_branch_ref, target_commit_id):
    """
    Setzt local_branch_ref (z. B. refs/heads/master) hart auf target_commit_id
    und zeigt HEAD symbolisch auf diesen Branch.
    """
    refs = repo.refs
    refs[local_branch_ref] = target_commit_id
    refs.set_symbolic_ref(b"HEAD", local_branch_ref)

def _try_nuke_and_reclone(database, remote_url):
    """
    Fallback: vollständiges Neu-Klonen in temp-Ordner, dann Inhalte ersetzen.
    Achtung: Löscht lokale Dateien (destruktiv).
    """
    tmp = database.rstrip("/\\") + "_tmp_clone"
    if os.path.isdir(tmp):
        shutil.rmtree(tmp, ignore_errors=True)

    porcelain.clone(source=remote_url, target=tmp, checkout=True)

    # Bestehenden Arbeitsbaum (außer .git) löschen
    for name in os.listdir(database):
        if name == ".git":
            # Entferne alte .git, da wir die neue übernehmen wollen (sauberer Zustand)
            shutil.rmtree(os.path.join(database, name), ignore_errors=True)
            continue
        full = os.path.join(database, name)
        if os.path.isfile(full) or os.path.islink(full):
            _ensure_writable(full)
            os.remove(full)
        else:
            shutil.rmtree(full, ignore_errors=True)

    # Inhalte aus tmp herüberkopieren
    for name in os.listdir(tmp):
        src = os.path.join(tmp, name)
        dst = os.path.join(database, name)
        if os.path.isfile(src) or os.path.islink(src):
            shutil.copy2(src, dst)
        else:
            shutil.copytree(src, dst)
    shutil.rmtree(tmp, ignore_errors=True)

def git_reset_repo_to_origin(remote_name="origin", prefer_branch=None, remote_url="https://github.com/chrisiweb/lama_latest_update.git"):
    """
    Ersetzt ALLES lokal so, wie es in origin/<branch> liegt.
    - Ermittelt den passenden Remote-Ref (HEAD/master/main)
    - Force-setzt lokalen Branch (master) + HEAD
    - Rebuild Index
    - Löscht alle untracked Dateien/Ordner
    - Schreibt alle Dateien aus Remote-Tree in den Arbeitsbaum
    - Validiert lokaler Head == Remote-Commit

    Rückgabe:
      True bei Erfolg, ansonsten Exception-Objekt.
    """
    try:
        repo = porcelain.Repo(database)
        repo._worktree_path = database

    except Exception:
        # Kein Repo vorhanden? -> frisch klonen
        try:
            porcelain.clone(source=remote_url, target=database, checkout=True)
            return True
        except Exception as e:
            return e

    try:
        # 1) fetch
        try:
            porcelain.fetch(repo, remote_location=remote_name)
        except Exception as e:
            _log(f"fetch failed: {e}")

        # 2) Ziel-Ref finden
        target_remote_ref = _detect_remote_target_ref(repo, remote=remote_name.encode(), prefer_branch=prefer_branch)
        target_commit = repo[target_remote_ref]  # Commit-Objekt
        target_tree_id = target_commit.tree

        # 3) Lokale Branch-Ref setzen (wir bleiben bei 'master', um kompatibel mit deinem Code zu bleiben)
        local_branch = b"refs/heads/master"
        _force_move_head_and_branch(repo, local_branch, target_commit.id)

        # 4) Index aus dem Ziel-Tree neu aufbauen
        build_index_from_tree(repo.path, repo.index_path(), repo.object_store, target_tree_id)

        # 5) Untracked/Abweichendes löschen und Tree ausschreiben
        tracked = _iter_tracked_paths_from_tree(repo.object_store, target_tree_id)
        _remove_untracked_files(database, tracked)
        _checkout_tree_to_workdir(repo, target_tree_id, database)

        # 6) Optional: zusätzliche Cleanups, falls Dulwich noch Metadaten hängen hat
        try:
            porcelain.clean(repo=repo, target_dir=database)
        except Exception:
            pass

        # 7) Validierung
        head_commit = repo[b"HEAD"]
        if head_commit.id != target_commit.id:
            raise RuntimeError("HEAD stimmt nach Reset nicht mit Remote-Commit überein.")

        return True

    except Exception as e:
        # Letzter Fallback: nuke & reclone
        try:
            _try_nuke_and_reclone(database, remote_url=remote_url)
            return True
        except Exception as e2:
            # Original-Fehler anreichern
            return RuntimeError(f"Hard Reset fehlgeschlagen: {e}\nFallback (Reclone) ebenfalls fehlgeschlagen: {e2}")



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


def to_str(x):
    return x.decode("utf-8") if isinstance(x, bytes) else x

def check_for_changes(database):
    repo = porcelain.Repo(database)
    repo._worktree_path = database
    status = porcelain.status(repo)
    untracked = [to_str(p) for p in status.untracked]
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