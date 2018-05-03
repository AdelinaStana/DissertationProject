import os, shutil
from git import Repo

EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

class GitWrapper:
    def __init__(self, directory):
        self.workingDir = directory

    def parseFilesTree(self, tree):
        try:
            for item in tree.traverse():
                if item.type == 'blob':
                    print(item.name)
                else:
                    self.parseFilesTree(item)
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

    def getRepo(self):
        repo_path = self.workingDir
        repo = Repo(repo_path)
        current_dir = os.getcwd()
        os.chdir(repo_path)
        try:
            os.mkdir(repo_path+"\~diffs")
            if not repo.bare:
                print('Repo at '+repo_path+' successfully loaded.')
                # self.print_repository(repo)
                commits = list(repo.iter_commits('master'))[:2500]
                print('Number of commits : {}'.format(len(commits)))
                nr = 0
                printNr = 0
                for commit in commits:
                    parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
                    changedFiles = [item.a_path for item in commit.diff(parent)]
                    nrOfFilesChanged = 0
                    for file in changedFiles:
                        if file.endswith('.h') or file.endswith('.cc') or file.endswith('.cpp'):
                            nrOfFilesChanged += 1
                    if nrOfFilesChanged >= 1:
                        os.system("git diff "+parent.hexsha+" "+commit.hexsha+" > "+repo_path+"\~diffs\diff"+str(nr)+"_FilesChanged_"+str(nrOfFilesChanged)+".txt")
                        nr += 1
                    printNr += 1
                    print(printNr)
        except BaseException as e:
            print(e)
        else:
            print('Could not load repository at '+repo_path+' successfully loaded.')

        os.chdir(current_dir)