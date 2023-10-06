#!/usr/bin/python3
""" Creates and distributes an archive to web servers,
using created function deploy and pack"""

from fabric.api import *
import os

env.hosts = ["3.235.198.120", "3.239.50.204"]
env.user = "ubuntu"  # Set the SSH user


def do_pack():
    """Create a compressed archive of web_static directory"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploy the compressed archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        folder_name = os.path.basename(archive_path).split(".")[0]
        remote_path = "/data/web_static/releases/{}".format(folder_name)

        # Upload the archive to the server
        put(archive_path, "/tmp")

        # Create the folder on the server
        run("mkdir -p {}".format(remote_path))

        # Unpack the archive
        run(
            "tar -xzf /tmp/{} -C {}".format(os.path.basename(archive_path), remote_path)
        )

        # Delete the archive file
        run("rm /tmp/{}".format(os.path.basename(archive_path)))

        # Move the contents to the proper location
        run("mv {}/web_static/* {}".format(remote_path, remote_path))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(remote_path))

        print("New version deployed successfully!")
        return True
    except Exception:
        return False


def deploy():
    """Full deployment process"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


#!/usr/bin/python3
""" Creates and distributes an archive to web servers,
using created function deploy and pack"""

from fabric.api import *
import os

env.hosts = ["3.235.198.120", "3.239.50.204"]
env.user = "ubuntu"  # Set the SSH user


def do_pack():
    """Create a compressed archive of web_static directory"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploy the compressed archive to the web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        folder_name = os.path.basename(archive_path).split(".")[0]
        remote_path = "/data/web_static/releases/{}".format(folder_name)

        # Upload the archive to the server
        put(archive_path, "/tmp")

        # Create the folder on the server
        run("mkdir -p {}".format(remote_path))

        # Unpack the archive
        run(
            "tar -xzf /tmp/{} -C {}".format(os.path.basename(archive_path), remote_path)
        )

        # Delete the archive file
        run("rm /tmp/{}".format(os.path.basename(archive_path)))

        # Move the contents to the proper location
        run("mv {}/web_static/* {}".format(remote_path, remote_path))

        # Remove the old symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(remote_path))

        print("New version deployed successfully!")
        return True
    except Exception:
        return False


def deploy():
    """Full deployment process"""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
