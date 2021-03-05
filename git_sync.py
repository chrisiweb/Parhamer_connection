import shutil
import os
from config import database, path_localappdata_lama
from dulwich import porcelain, index
from dulwich.objectspec import parse_tree
import stat
import posixpath
from urllib3.exceptions import MaxRetryError
from datetime import datetime
from standard_dialog_windows import information_window
from time import sleep


def git_clone_repo():
    try:
        porcelain.clone("https://github.com/chrisiweb/lama_latest_update.git", database)
        return True
    except MaxRetryError:
        return False


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

        porcelain.reset(repo, "hard", treeish=b"refs/remotes/origin/master")

        porcelain.clean(repo=repo, target_dir=database)


        if deleted_files !=[]:
            for all in deleted_files:
                file_path = os.path.join(database, all.decode('utf-8'))
                os.remove(file_path)

            status=porcelain.status(repo) 

            repo.stage(status.unstaged)

            porcelain.commit(repo, message="delete files")
        return True

    except MaxRetryError:
        return False




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
    # if staged_files['delete'] != []:
    #     for all in staged_files['delete']:
    #         filename=os.path.basename(all)
    #         shutil.copyfile(os.path.join(path_programm,"_database" ,all.decode()), os.path.join(git_temp_delete, filename.decode()))
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


def git_push_to_origin(ui):
        local_appdata = os.getenv('LOCALAPPDATA')
        access_token_file = os.path.join(os.getenv('LOCALAPPDATA'),"LaMA", "credentials","access_token.txt")
        credentials_file = os.path.join(os.getenv('LOCALAPPDATA'),"LaMA", "credentials","developer_credentials.txt")
        with open(credentials_file, "r", encoding="utf-8") as f:
            credentials = f.read()
        access_token = credentials + "5f96d9808ebbc5adbf2b56b1f8aaf4"

        repo = porcelain.open_repo(database)
        path_origin = os.path.join(database, ".git", "refs","remotes","origin", "master")
        path_head = os.path.join(database, ".git", "refs","heads","master")
        
        status = porcelain.status(repo)
        repo.stage(status.unstaged + status.untracked)

        if status.unstaged==[] and status.untracked == []:
            # information_window("Es wurden keine Änderungen gefunden.")
            return False
        
        try:
            ui.label.setText("Datenbank hochladen ... (1%)")

            status = porcelain.status(repo)
            ui.label.setText("Datenbank hochladen ... (21%)")

            copy_all_changed_files(status.staged)
            ui.label.setText("Datenbank hochladen ... (22%)")

            git_reset_repo_to_origin()
            ui.label.setText("Datenbank hochladen ... (53%)")

            restore_all_changes()
            shutil.copyfile(path_origin, path_head)
            ui.label.setText("Datenbank hochladen ... (54%)")


            status = porcelain.status(repo)
            repo.stage(status.unstaged + status.untracked)
            ui.label.setText("Datenbank hochladen ... (84%)")


            time_tag = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")
            porcelain.commit(repo, message="New LaMA Upload {}".format(time_tag))

            ui.label.setText("Datenbank hochladen ... (85%)")

            porcelain.push(repo,"https://lama-contributor:{}@github.com/chrisiweb/lama_latest_update.git".format(access_token),"master")
            ui.label.setText("Datenbank hochladen ... (100%)")
            repo.close()

            sleep(1)
        
        except Exception as e:
            return "error"

        return True


def check_for_changes(database):
    repo = porcelain.open_repo(database)
    status = porcelain.status(repo)
    return status.unstaged, status.untracked
