import os
import platform

# --shm-size=512m

def docker_image(id, volumn=[], name=None, shm_size=None):
    """
    A helper function for create the docker argument

    Parameters:
    id (string): required, the docker image id to run the application.
    volumn (string[]): optional, a list of the volumn names to mapping from the physical file system to
        the docker internal file system.
    name (string): optional, the name that specific to the running container,
        default value none means no name was specific.
    shm_size (string): optional, tweaks of the ``/dev/shm`` size, example as ``512m`` for set ``/dev/shm`` 
        in container from the default 64MB to 512MB.  

    Returns:
    object: a tuple list object that contains arguments for build commandline for ``docker run`` command.
    """

    return {"image": id, "volumn": volumn, "name": name,
            "shm_size": shm_size}


def mount_volumn(docker_run, argv, workdir, docker_config):
    """Create the docker volumn mount argument

    + argv -- the target R# function parameters
    + docker -- the docker argument object for create docker run, this argument
        value should be generated via the ``docker_image`` helper function.
    + docker_run -- the commandline argument collection list for run the docker
        command
    """

    docker = "docker"

    # config for run commandline test on windows
    if platform.system() != "Windows":
        docker = os.popen("which docker").read().strip()

    workspace = os.path.abspath(workdir)

    docker_run.append("-v /var/run/docker.sock:/run/docker.sock")
    docker_run.append('-v "{0}:/bin/docker"'.format(docker))
    docker_run.append('-v "/tmp:/tmp"')

    if not docker_config["volumn"] is None:
        for arg in docker_config["volumn"]:
            if arg in argv:
                # mount volumn from the function argument
                vol = os.path.abspath(argv[arg])
                print("[mount] argv.{} -> {}".format(arg, vol))
            else:
                # mount volumn from the docker volumn property
                vol = os.path.abspath(arg)
                print("[mount] {} -> {}".format(arg, vol))

            docker_run.append('-v "{0}:{0}"'.format(vol))

    docker_run.append('-w "{0}"'.format(workspace))

    return docker_run
