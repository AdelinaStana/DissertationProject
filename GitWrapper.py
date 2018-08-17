import os, shutil
from git import Repo

EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

class GitWrapper:
    def __init__(self, directory):
        self.repo_path = directory

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

    def getNrOfChangedFiles(self, commit, parent):
        acceptedSuffix = ['.cpp', '.h', '.cc', '.c++', '.java']

        changedFiles = [item.a_path for item in commit.diff(parent)]
        nrOfFilesChanged = 0
        for file in changedFiles:
            fileName, fileExtension = os.path.splitext(file)
            if fileExtension in acceptedSuffix:
                nrOfFilesChanged += 1

        return nrOfFilesChanged

    def findFile(self, file):
        for path, subdirs, files in os.walk(self.repo_path):
            for name in files:
                if name == file:
                    return True
        return False

    def getFileFromGit(self, commit, path):

        try:
            os.system("git --work-tree=" + self.repo_path + "\~deleted checkout "+commit.hexsha+" "+path)
        except BaseException as e:
            print(e)

    def getDeletedFiles(self, commit, parent):
        acceptedSuffix = ['.cpp', '.h', '.cc', '.c++', '.java']

        for diff_added in commit.diff(parent).iter_change_type('D'):
            other, file = os.path.split(diff_added.b_path)
            fileName, fileExtension = os.path.splitext(file)
            if fileExtension in acceptedSuffix and not self.findFile(file):
                self.getFileFromGit(commit, diff_added.b_path)

    def createFolders(self):
        try:
            os.mkdir(self.repo_path + "\~deleted")
        except BaseException:
            shutil.rmtree(self.repo_path + "\~deleted")
            os.mkdir(self.repo_path + "\~deleted")

        try:
            os.mkdir(self.repo_path+"\~diffs")
        except BaseException :
            shutil.rmtree(self.repo_path+"\~diffs")
            os.mkdir(self.repo_path + "\~diffs")

    def getRepo(self):
        repo = Repo(self.repo_path)
        current_dir = os.getcwd()
        os.chdir(self.repo_path)

        self.createFolders()
        try :
            if not repo.bare:
                print('Repo at '+self.repo_path+' successfully loaded.')
                # self.print_repository(repo)
                commits = list(repo.iter_commits(repo.active_branch))[:4000]
                print('Number of commits : {}'.format(len(commits)))
                nr = 0
                printNr = 0
                for commit in commits:
                    parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
                    #self.getDeletedFiles(commit, parent)
                    nrOfFilesChanged = self.getNrOfChangedFiles(commit, parent)
                    if nrOfFilesChanged >= 1:
                        os.system("git diff "+parent.hexsha+" "+commit.hexsha+" > "+self.repo_path+"\~diffs\diff"+str(nr)+"_FilesChanged_"+str(nrOfFilesChanged)+".txt")
                        nr += 1
                    printNr += 1
                    print(printNr)
            else:
                print('Could not load repository at ' + self.repo_path + '.')
        except BaseException as e :
            print(e)

        os.chdir(current_dir)