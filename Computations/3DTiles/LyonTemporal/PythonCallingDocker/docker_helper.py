import os
import sys
import docker
import logging
from abc import ABC, abstractmethod


class DockerHelper(ABC):

    def __init__(self, image_name):
        # The name of the image to build or to pull
        self.image_name = image_name
        self.client = None  # The name for the docker client (read server)
        self.mounted_input_dir = os.getcwd()
        self.mounted_output_dir = os.getcwd()
        # Some containers (like 3DUse) provide multiple commands each of
        # which might require its proper working directory (i.e. the WORKDIR
        # variable of the Dockerfile)
        self.working_dir = '.'
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
            logging.error('   is a docker server running this host ?')
            sys.exit(1)

    def build(self, context_dir):
        """
        Provision the docker image.
        """
        if not os.path.exists(context_dir):
            logging.error(f'Unfound context directory: {context_dir} ')
            sys.exit(1)

        try:
            result = self.client.images.build(
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

    def pull(self):
        """
        Pulls an image (set in self.image_name) from the docker registry.
        """
        try:
            images = self.client.images.pull(repository=self.image_name)
            logging.info(f'Docker pulling image: {self.image_name}')
            for line in images:
                logging.info(f'    {line}')
            logging.info(f'Docker pulling image done.')
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

        container = self.client.containers.run(
            self.image_name,
            # command=["/bin/sh", "-c", "ls /Input /Output"],      # for debug
            command=self.get_command(),
            volumes=volumes,
            working_dir=self.working_dir,
            stdin_open=True,
            stderr=True,
            detach=True,
            tty=True)
        container.wait()

        out = container.logs(stdout=True, stderr=False)
        if out:
            logging.info('Docker run standard output follows:')
            logging.info(f'docker-stdout> {out}')
        err = container.logs(stdout=False, stderr=True)
        if err:
            logging.info('Docker run standard error follows:')
            logging.info(f'docker-stderr> {err}')
