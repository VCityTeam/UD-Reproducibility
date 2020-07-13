import os
from docker_helper import DockerHelperTask


class Docker3DUse(DockerHelperTask):

    def __init__(self):
        super().__init__('liris:3DUse')
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   '3DUse-DockerContext')
        self.build(context_dir)
