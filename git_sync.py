import shutil
import os
from dulwich import porcelain, index
from dulwich.objectspec import parse_tree
import stat
import posixpath
from urllib3.exceptions import MaxRetryError


def git_clone_repo(database):
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


def git_reset_repo_to_origin(database):
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


def git_push_to_origin(database):
        repo = porcelain.open_repo(database)
        path_origin = os.path.join(database, ".git", "refs","remotes","origin", "master")
        path_head = os.path.join(database, ".git", "refs","heads","master")

        status = porcelain.status(repo)
        repo.stage(status.unstaged + status.untracked)
        if status.unstaged==[] and status.untracked == []:
            print('No changes detected!')
            return
        # repo.stage(status.unstaged + status.untracked)
        status = porcelain.status(repo)
        print(status.staged)

        print('copy files')
        self.copy_all_changed_files(status.staged)
        print('reset to origin/master')
        
        self.pushButton_pull_clicked()
        # porcelain.fetch(repo)
        # porcelain.reset(repo, "hard", treeish=b"refs/remotes/origin/master")
        
        # porcelain.clean(repo=repo, target_dir=database)
        print('restore all changes')

        self.restore_all_changes()

        # porcelain.add(self.repo,paths=database)
        shutil.copyfile(path_origin, path_head)
        print('add --all')
        status = porcelain.status(repo)
        print(status)
        repo.stage(status.unstaged + status.untracked)
        status = porcelain.status(repo)
        print(status)
        print('commit')
        time_tag = datetime.now().strftime("%Y-%m-%d (%H:%M:%S)")
        porcelain.commit(repo, message="New LaMA Upload {}".format(time_tag))
        # shutil.copyfile(path_origin, path_head)
        # porcelain.pull(repo, "https://github.com/chrisiweb/lama_latest_update.git","master")
        # shutil.copyfile(path_origin, path_head)
        # try:
        # status = porcelain.status(repo)
        porcelain.push(repo,"https://chrisiweb:Ewyc&gEwym0@github.com/chrisiweb/lama_latest_update.git","master") #force=True

        # print('pull') 
        # porcelain.pull(repo, "https://github.com/chrisiweb/lama_latest_update.git", "master")
        # except porcelain.DivergedBranches:
        #     print('diverged branches')
        #     porcelain.pull(repo, "https://github.com/chrisiweb/lama_latest_update.git","master")
        #     porcelain.push(repo,"https://chrisiweb:Ewyc&gEwym0@github.com/chrisiweb/lama_latest_update.git","master")
        repo.close()
        # self.repo.git.add(A=True)
        # self.repo.index.commit('new commit')
        # o = self.repo.remotes.origin
        # o.push()
        print('done')

def check_for_changes(database):
    repo = porcelain.open_repo(database)
    status = porcelain.status(repo)
    return status.unstaged, status.untracked
