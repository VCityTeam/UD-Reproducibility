import os
import sys
import docker
import requests
import logging
from abc import ABC, abstractmethod


class DockerHelperBase(ABC):

    def __init__(self, image_name):
        # The name of the image to build or to pull
        self.image_name = image_name
        self.container_name = None
        self.container_name = None
        self.mounted_input_dir = os.getcwd()
        self.mounted_output_dir = os.getcwd()
        # Some containers (like 3DUse) provide multiple commands each of
        # which might require its proper working directory (i.e. the WORKDIR
        # variable of the Dockerfile)
        self.working_dir = None
        self.environment = None   # Docker run environment variables

        self.ports = None  # Specific to derived class DockerHelperService

        self.__client = None  # The name for the docker client (read server)
        self.__container = None
        self.__run_arguments = None  # The arguments handled over to the run()

        self.assert_server_is_active()

    def assert_server_is_active(self):
        """
        Assert that a docker server is up and available
        :return: None, sys.exit() on failure
        """
        self.__client = docker.from_env()
        try:
            self.__client.ping()
        except (requests.exceptions.ConnectionError, docker.errors.APIError):
            logging.error('Unable to connect to a docker server:')
            logging.error('   is a docker server running this host ?')
            sys.exit(1)

    def get_container(self):
        if not self.__container:
            logging.info('Warning: requesting an unset container.')
        return self.__container

    # FIXME: build and pull should be in different classes (DockerBuild and DockerPull)
    def build(self, context_dir):
        """
        Provision the docker image by building it.
        """
        if not os.path.exists(context_dir):
            logging.error(f'Unfound context directory: {context_dir} ')
            sys.exit(1)

        try:
            result = self.__client.images.build(
                path=context_dir,
                tag=self.image_name)
            logging.info(f'Docker building image: {self.image_name}')
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

    def pull(self, tag):
        """
        Provision the docker image by pulling it from some well know docker
        registry (stored in self.image_name).
        """
        try:
            self.__client.images.pull(repository=self.image_name, tag=tag)
            logging.info(f'Docker pulling image: {self.image_name}:{tag}')
            logging.info(f'Docker pulling image done.')
            # FIXME: this concatenation is a hack since the run method does not
            # have a tag argument, but the tag should be an attribute of the class
            # and be concatenated when docker.run is invoked.
            self.image_name += ':' + tag
        except docker.errors.APIError as err:
            logging.error('Unable to build the docker image: with error')
            logging.error(f'   {err}')
            sys.exit(1)

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

    @abstractmethod
    def get_command(self):
        print("WTF")

    def run(self):
        """
        Prepare the information required to launch the container and run it
        (always in a detached mode, for technical reasons)
        """
        volumes = {self.mounted_input_dir: {'bind': '/Input', 'mode': 'rw'}}
        if not self.mounted_input_dir == self.mounted_output_dir:
            # When mounting the same directory twice (which is the case when
            # the input and output directory are the same) then containers.run()
            # raises a docker.errors.ContainerError. Hence we only mount the
            # /Output volume when they both differ. Note that when this
            # happens the command in the derived class must be altered in order
            # to place its output in the /Input mounted point (because in this
            # /Output is (equal to) /Input.
            volumes[self.mounted_output_dir] = {'bind': '/Output', 'mode': 'rw'}

        arguments = dict(
            # command=["/bin/sh", "-c", "ls /Input /Output"],      # for debug
            command=self.get_command(),
            volumes=volumes,
            working_dir=self.working_dir,
            stdin_open=True,
            stderr=True,
            detach=True,
            tty=True
        )

        if self.container_name:
            containers = self.__client.containers.list(
                filters={'name': self.container_name})
            if containers:
                logging.error(f'A container named {self.container_name} '
                              'already exists. Exiting.')
                sys.exit(1)
            arguments['name'] = self.container_name

        arguments['environment'] = self.environment
        if self.working_dir:
            arguments['working_dir'] = self.working_dir
        if self.ports:
            arguments['ports'] = self.ports
        self.__run_arguments = arguments

        self.__container = self.__client.containers.run(
            self.image_name,
            **self.__run_arguments)

    def retrieve_output_and_errors(self):
        out = self.__container.logs(stdout=True, stderr=False)
        if out:
            logging.info('Docker run standard output follows:')
            logging.info(f'docker-stdout> {out}')
        err = self.__container.logs(stdout=False, stderr=True)
        if err:
            logging.info('Docker run standard error follows:')
            logging.info(f'docker-stderr> {err}')


class DockerHelperService(DockerHelperBase):
    """
    Have the container run a server and serve until explicit termination
    is required.
    """
    def halt_service(self):
        self.get_container().stop()
        self.retrieve_output_and_errors()
        self.get_container().remove()


class DockerHelperTask(DockerHelperBase):
    """
    Have the container execute some (computational) task and, when
    computation is done, terminate the container.
    """

    def run(self):
        super().run()
        self.get_container().wait()
        self.retrieve_output_and_errors()
        self.get_container().remove()
