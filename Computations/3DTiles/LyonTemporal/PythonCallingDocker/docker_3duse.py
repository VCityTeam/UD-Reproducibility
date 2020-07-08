import os
import sys
import logging
from docker_helper import DockerHelper


class Docker3DUse(DockerHelper):

    def __init__(self):
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   '3DUse-DockerContext')
        tag_name = 'liris:3DUse'
        super().__init__(context_dir, tag_name)
