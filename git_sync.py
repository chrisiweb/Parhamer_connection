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


def git_reset_repo_to_origin():
    try:
        repo = porcelain.Repo(database)
        porcelain.fetch(repo)

        tree_head_id = repo[repo[b'refs/heads/master'].tree].id
        tree_origin_master_id = repo[repo[b'refs/remotes/origin/master'].tree].id

        store=repo.object_store
        list_all_files_head = list_all_files(store, tree_head_id)
        list_all_files_origin_master = list_all_files(store, tree_origin_master_id)

        deleted_files = list(set(list_all_files_head)-set(list_all_files_origin_master))

        if deleted_files !=[]:
            for all in deleted_files:
                file_path = os.path.join(database, all.decode('utf-8'))
                os.remove(file_path)

            status=porcelain.status(repo) 

            repo.stage(status.unstaged)

            porcelain.commit(repo, message="delete files")


        ###working###
        porcelain.reset(repo, "hard", treeish=b"refs/remotes/origin/master")

        porcelain.clean(repo=repo, target_dir=database)

        resolve_divergence()
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


def check_for_changes(database):
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
