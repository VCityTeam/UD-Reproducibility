import os
import sys
import docker
import requests
import logging
import time
from abc import ABC, abstractmethod


class DockerHelperBase(ABC):
    """
    Helper class for docker manipulation, built on docker SDK library.
    """
    def __init__(self, image_name, tag):
        """
        :param image_name: image name (e.g. "3DCityDB")
        :param tag: tag of the image (e.g. "v4.0.2")
        """
        # Some methods of docker SDK need the image_name and/or the tag_name
        # independently while others need the full image name which is a
        # concatenation of these.
        self.image_name = image_name
        self.tag = tag
        self.full_image_name = image_name + ':' + tag
        self.client = None  # The name for the docker client (read server)
        self.assert_server_is_active()

    def assert_server_is_active(self):
        """
        Assert that a docker server is up and available
        :return: None, sys.exit() on failure
        """
        self.client = docker.from_env()
        try:
            self.client.ping()
        except (requests.exceptions.ConnectionError, docker.errors.APIError):
            logging.error('Unable to connect to a docker server:')
            logging.error('   is a docker server running on this host ?')
            sys.exit(1)


class DockerHelperBuild(DockerHelperBase):
    """
    Build an image from a local Docker context
    """
    def build(self, context_dir):
        """
        Provision the docker image by building it.
        """
        if not os.path.exists(context_dir):
            logging.error(f'Unfound context directory: {context_dir} ')
            sys.exit(1)

        try:
            # Note: The tag argument is not self.tag since it is not the
            # version of the image that is expected here but the full image
            # name; i.e. here we "tag" the built image with the full image name.
            result = self.client.images.build(
                path=context_dir,
                tag=self.full_image_name)
            logging.info(f'Docker building image: {self.full_image_name}')
            for line in result:
                logging.info(f'    {line}')
            logging.info(f'Docker building image done.')
        except docker.errors.APIError as err:
            logging.error('Unable to build the docker image: with error')
            logging.error(f'   {err}')
            sys.exit(1)
        except TypeError:
            logging.error('Building the docker image requires path or fileobj.')
            sys.exit(1)


class DockerHelperPull(DockerHelperBase):
    """
    Pull an image from a well known docker registry
    """
    def pull(self):
        """
        Provision the docker image by pulling it from some well know docker
        registry (stored in self.repository).
        """
        try:
            self.client.images.pull(repository=self.image_name, tag=self.tag)
            logging.info(f'Docker pulling image: {self.full_image_name}')
            logging.info(f'Docker pulling image done.')
        except docker.errors.APIError as err:
            logging.error('Unable to build the docker image: with error')
            logging.error(f'   {err}')
            sys.exit(1)


class DockerHelperContainer(DockerHelperBase):
    """
    Helper class for docker containers. Helps input / outputs
    management, volumes management and running containers
    """
    def __init__(self, image_name, tag):
        super().__init__(image_name, tag)
        self.container_name = None
        self.mounted_input_dir = os.getcwd()
        self.mounted_output_dir = os.getcwd()
        # Some containers (like 3DUse) provide multiple commands each of
        # which might require its proper working directory (i.e. the WORKDIR
        # variable of the Dockerfile)
        self.working_dir = None
        self.volumes = dict()
        self.environment = None   # Docker run environment variables
        self.run_arguments = None  # The arguments handled over to the run()

        self.__container = None

    def set_mounted_input_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info(f'Input dir to mount {directory} not found. Exiting')
            sys.exit(1)
        self.mounted_input_dir = directory

    def get_mounted_input_directory(self):
        return self.mounted_input_dir

    def set_mounted_output_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info(f'Output dir to mount {directory} not found. Exiting')
            sys.exit(1)
        self.mounted_output_dir = directory

    def get_mounted_output_directory(self):
        return self.mounted_output_dir

    def get_container(self):
        if not self.__container:
            logging.info('Warning: requesting an unset container.')
        return self.__container

    def add_volume(self, host_volume, inside_docker_volume, mode):
        """
        :param host_volume: The host path (must be absolute) or
        the volume name (must have been created earlier with
        docker volume create) to bind the data to.
        :param inside_docker_volume: The path to mount
        the volume inside the container.
        :param mode: Volume access mode which is either
        'rw' for 'read write' or 'ro' for read-only.
        """
        if not os.path.isdir(host_volume):
            logging.error(f'No such host directory {host_volume}. Exiting')
            sys.exit(1)
        if not os.path.isabs(host_volume):
            logging.error(f'Host directory {host_volume} is not absolute.'
                          'Exiting')
            sys.exit(1)
        if not os.path.isabs(inside_docker_volume):
            logging.error(f'Mount point {inside_docker_volume} is not absolute.'
                          ' Exiting')
            sys.exit(1)
        self.volumes[host_volume] = {'bind': inside_docker_volume, 'mode': mode}

    @abstractmethod
    def get_command(self):
        print("WTF")

    def set_run_arguments(self):
        """
        Sets common arguments passed to the run method of the docker SDK lib.
        Other arguments can be set by child classes, e.g. the
        DockerHelperService class sets the 'ports' argument.
        """
        self.run_arguments = dict(
            # command=["/bin/sh", "-c", "ls /Input /Output"],      # for debug
            command=self.get_command(),
            volumes=self.volumes,
            working_dir=self.working_dir,
            stdin_open=True,
            stderr=True,
            detach=True,
            tty=True
        )

        if self.container_name:
            containers = self.client.containers.list(
                filters={'name': self.container_name})
            if containers:
                logging.error(f'A container named {self.container_name} '
                              'already exists. Exiting.')
                sys.exit(1)
            self.run_arguments['name'] = self.container_name

        if self.environment:
            self.run_arguments['environment'] = self.environment
        if self.working_dir:
            self.run_arguments['working_dir'] = self.working_dir

    def run(self):
        """
        Prepare the information required to launch the container and run it
        (always in a detached mode, for technical reasons).
        """
        self.__container = self.client.containers.run(
            self.full_image_name,
            **self.run_arguments)

    def retrieve_output_and_errors(self):
        out = self.__container.logs(stdout=True, stderr=False)
        if out:
            logging.info('Docker run standard output follows:')
            logging.info(f'docker-stdout> {out}')
        err = self.__container.logs(stdout=False, stderr=True)
        if err:
            logging.info('Docker run standard error follows:')
            logging.info(f'docker-stderr> {err}')


class DockerHelperService(DockerHelperContainer):
    def __init__(self, image_name, tag):
        super().__init__(image_name, tag)
        self.ports = None

    """
    Have the container run a server and serve until explicit termination
    is required.
    """
    def halt_service(self):
        self.get_container().stop()
        self.retrieve_output_and_errors()
        self.get_container().remove()

    def run(self):
        self.set_run_arguments()
        if self.ports:
            self.run_arguments['ports'] = self.ports
        super().run()


class DockerHelperTask(DockerHelperContainer):
    """
    Have the container execute some (computational) task and, when
    computation is done, terminate the container.
    """
    def run(self):
        self.set_run_arguments()
        super().run()
        self.get_container().wait()
        self.retrieve_output_and_errors()
        self.get_container().remove()

        # Because of caching issues for bind mounts on OSX, refer e.g. to
        # https://docs.docker.com/docker-for-mac/osxfs-caching/
        # the following check sometimes fails (although the file will
        # eventually "pop up" when the buffers get processed). We thus
        # introduce the following delay kludge:
        time.sleep(10)
