import os, shutil
from git import Repo

EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class GitWrapper:
    def __init__(self, directory):
        self.repo_path = directory

    def parse_files_tree(self, tree):
        try:
            for item in tree.traverse():
                if item.type == 'blob':
                    print(item.name)
                else:
                    self.parse_files_tree(item)
        except BaseException as e:
            print(e)

    def print_commit(self, commit):
        print('----')
        print(str(commit.hexsha))
        print("\"{}\" by {} ({})".format(commit.summary,
                                         commit.author.name,
                                         commit.author.email))
        print(str(commit.authored_datetime))
        print(str("count: {} and size: {}".format(commit.count(),
                                                  commit.size)))

        print("Size of files changed: {}".format(len(commit.diff())))
        for diff_added in commit.diff():
            print(diff_added.b_path)

    def print_repository(self, repo):
        print('Repo description: '.format(repo.description))
        print('Repo active branch is {}'.format(repo.active_branch))
        branches = repo.remotes.origin.refs
        print('Number of branches : {}'.format(len(branches)))
        for branch in branches:
            commits = list(repo.iter_commits(branch))
            print('Branch named {} - commits number: {}'.format(branch, len(commits)))

        print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))

    def get_changed_files_number(self, commit, parent):
        accepted_suffix = ['.cpp', '.h', '.cc', '.c++', '.java', '.cs']

        changed_files = [item.a_path for item in commit.diff(parent)]
        nr_of_files_changed = 0
        for file in changed_files:
            file_name, file_extension = os.path.splitext(file)
            if file_extension in accepted_suffix:
                nr_of_files_changed += 1

        return nr_of_files_changed

    def find_file(self, file):
        for path, subdirs, files in os.walk(self.repo_path):
            for name in files:
                if name == file:
                    return True
        return False

    def get_file_from_git(self, commit, path):

        try:
            os.system("git --work-tree=" + self.repo_path + "\~deleted checkout "+commit.hexsha+" "+path)
        except BaseException as e:
            print(e)

    def get_deleted_files(self, commit, parent):
        accepted_suffix = ['.cpp', '.h', '.cc', '.c++', '.java']

        for diff_added in commit.diff(parent).iter_change_type('D'):
            other, file = os.path.split(diff_added.b_path)
            file_name, file_extension = os.path.splitext(file)
            if file_extension in accepted_suffix and not self.find_file(file):
                self.get_file_from_git(commit, diff_added.b_path)

    def create_folders(self, path):
        try:
            os.mkdir(path)
        except:
            print("Error in making dir: " + path)

    def get_repo(self):
        repo = Repo(self.repo_path)
        os.chdir(self.repo_path)
        return repo

    def get_logs(self, files_list):
        repo = self.get_repo()
        paths_dict = {}

        try:
            if not repo.bare:
                for file in files_list:
                    rel_path = file.replace(self.repo_path, 'a')
                    rel_path = rel_path.replace("\\", '/')
                    paths_dict[rel_path] = set()
                    old_paths = os.popen("git log --format='%n' --name-only --follow "+file).read()
                    old_paths = old_paths.replace('\n', '')
                    old_paths = old_paths.split('\'\'')
                    for path in old_paths:
                        if path != '':
                            paths_dict[rel_path].add("a/"+path.replace('\'', ''))
        except BaseException as e:
            print(e)
        return paths_dict

    def get_commits(self):
        current_dir = os.getcwd()
        repo = self.get_repo()

        self.create_folders(self.repo_path+"\~diffs")
        try:
            if not repo.bare:
                print('Repo at '+self.repo_path+' successfully loaded.')
                # self.print_repository(repo)
                commits = list(repo.iter_commits(repo.active_branch))[:6000]
                print('Number of commits : {}'.format(len(commits)))
                nr = 0
                print_nr = 0
                for commit in commits:
                    parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
                    # self.getDeletedFiles(commit, parent)
                    nr_of_files_changed = self.get_changed_files_number(commit, parent)
                    if nr_of_files_changed >= 1:
                        os.system("git diff "+parent.hexsha+" "+commit.hexsha+" > "+self.repo_path+"\~diffs\diff" + str(nr) + "_FilesChanged_"+str(nr_of_files_changed)+".txt")
                        nr += 1
                    print_nr += 1
                    print(print_nr)
            else:
                print('Could not load repository at ' + self.repo_path + '.')
        except BaseException as e:
            print(e)

        os.chdir(current_dir)

