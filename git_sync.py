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
