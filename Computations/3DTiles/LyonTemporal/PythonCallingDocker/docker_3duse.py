import os
import sys
import logging
from docker_helper import DockerHelper


class Docker3DUse(DockerHelper):

    def __init__(self):
        super().__init__('liris:3DUse')
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   '3DUse-DockerContext')
        self.build(context_dir)
