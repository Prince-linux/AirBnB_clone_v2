#!/usr/bin/python3
"""Clean all archives based on the number of arguments passed"""

from fabric.api import local


def do_clean(number=0):
    """Cleans all .tgz files"""
    number = int(number)

    # Define the directory where .tgz files are stored
    path = "versions"

    # List all .tgz files, sorted by modification time (newest first)
    files = local('ls -t {}/ | grep ".tgz"'.format(path), capture=True).split()

    # Ensure we keep at least the most recent two files
    files_to_keep = 2

    if number > files_to_keep:
        files_to_remove = files[files_to_keep:number]
        for file in files_to_remove:
            local("rm {}/{}".format(path, file))


if __name__ == "__main__":
    do_clean()
