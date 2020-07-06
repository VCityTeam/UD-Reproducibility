import os
import sys
import docker
import logging


class DockerHelper:

    def __init__(self, context_dir, tag_name):
        self.context_dir = context_dir
        self.tag_name = tag_name
        # Assert a docker server is active
        self.client = docker.from_env()
        try:
            self.client.ping()
        except (requests.exceptions.ConnectionError, docker.errors.APIError):
            logging.error('Unable to connect to a docker server:')
            logging.error('   is a docker server running this host ?')
            sys.exit(1)

        # Assert that the context directory exists
        if not os.path.exists(self.context_dir):
            logging.error(f'Unfound context directory: {self.context_dir} ')
            sys.exit(1)
        self.build()

    def build(self):
        try:
            result = self.client.images.build(
                path=self.context_dir,
                tag=self.tag_name)
            logging.info(f'Docker building image: {self.tag_name}')
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


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='DockerHelper.log',
                        filemode='w')
    docker_image_context_dir = os.path.join(os.getcwd(),
                                            '..',
                                            'Docker',
                                            'Collect-DockerContext')
    tag_name = 'liris:collect_lyon_data'
    d = DockerHelper(docker_image_context_dir, tag_name)