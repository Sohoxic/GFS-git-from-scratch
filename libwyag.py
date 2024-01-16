import argparse           # Git is a CLI application, so we’ll need something to parse command-line arguments
import collections        # We’ll need a few more container types than the base lib provides, most notably an OrderedDict
import configparser       # Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files.
from datetime import datetime
import grp, pwd           # We’ll need, just once, to read the users/group database on Unix (grp is for groups, pwd for users). This is because git saves the numerical owner/group ID of files, and we’ll want to display that nicely (as text)
from fnmatch import fnmatch          # To support .gitignore, we’ll need to match filenames against patterns like *.txt. Filename matching is in… fnmatch
import hashlib            # Git uses the SHA-1 function quite extensively. In Python, it’s in hashlib.
from math import ceil
import os                 # os and os.path provide some nice filesystem abstraction routines
import re                 # for regular expressions
import sys                # We also need sys to access the actual command-line arguments (in sys.argv)
import zlib               # Git compresses everything using zlib. Python has that, too

argparser = argparse.ArgumentParser(description="The stupidest content tracker")

# We’ll need to handle subcommands (as in git: init, commit, etc.) In argparse slang, these are called “subparsers”. Invocation of subcommands: The statement emphasizes that, in the argparse setup, all invocations of the command-line program should specify a subcommand. In other words, you don't just call the main program; instead, you call the main program followed by a specific subcommand. For instance, you don't just call git, but rather git COMMAND.
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")

# The Repository Object
# the basic approach of worktree/.git. Our repository object will then just hold two paths: the worktree and the gitdir(the worktree contains contains a subdirectory called .git).
# We read its configuration in .git/config (it’s just an INI file) and control that core.repositoryformatversion is 0.

class GitRepository (object):
    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)
        
        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config") # determines the path of the config file

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)

# Compute path under repo's gitdir.
def repo_path(repo, *path):
    return os.path.join(repo.gitdir, *path)

def repo_file(repo, *path, mkdir=False):
    """Same as repo_path, but create dirname(*path) if absent.  For example, repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD\") will create .git/refs/remotes/origin."""
    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)
    
def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""

    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a directory %s" % path)

    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None
    
def repo_create(path):
    """Create a new repository at path."""

    repo = GitRepository(path, True)

    # First, we make sure the path either doesn't exist or is an
    # empty dir.

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception ("%s is not a directory!" % path)
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception("%s is not empty!" % path)
    else:
        os.makedirs(repo.worktree)

    assert repo_dir(repo, "branches", mkdir=True)
    assert repo_dir(repo, "objects", mkdir=True)
    assert repo_dir(repo, "refs", "tags", mkdir=True)
    assert repo_dir(repo, "refs", "heads", mkdir=True)

    # .git/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")