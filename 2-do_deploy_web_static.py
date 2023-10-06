#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""

from fabric.api import *
import os

env.hosts = ["3.235.198.120", "3.239.50.204"]


def do_deploy(archive_path):
    """Deploy the archive to web servers"""
    if not os.path.exists(archive_path):
        print("Error: The archive file does not exist.")
        return False

    try:
        # Extract archive filename and folder name
        archive_filename = os.path.basename(archive_path)
        folder_name = archive_filename.split(".")[0]

        # Define remote paths
        remote_tmp_path = "/tmp/{}".format(archive_filename)
        remote_static_path = "/data/web_static/releases/{}".format(folder_name)
        remote_current_path = "/data/web_static/current"

        # Upload the archive to the server
        put(archive_path, remote_tmp_path)

        # Create directory for the new release
        run("mkdir -p {}".format(remote_static_path))

        # Extract the archive
        run("tar -xzf {} -C {}".format(remote_tmp_path, remote_static_path))

        # Delete the uploaded archive
        run("rm {}".format(remote_tmp_path))

        # Move contents to the proper location
        run("mv {}/web_static/* {}".format(remote_static_path, remote_static_path))

        # Remove the old symbolic link
        run("rm -rf {}".format(remote_current_path))

        # Create a new symbolic link
        run("ln -s {} {}".format(remote_static_path, remote_current_path))

        # Restart Nginx
        run("sudo service nginx restart")

        print("New version deployed successfully.")
        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False


if __name__ == "__main__":
    do_deploy("your_archive_path.tar.gz")
