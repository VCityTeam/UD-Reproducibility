import os
from docker_helper import DockerHelperBuild, DockerHelperTask


class DockerPy3dtiles(DockerHelperBuild, DockerHelperTask):

    def __init__(self):
        super().__init__('liris', 'Py3dTilesTiler')
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   'CityTiler-DockerContext')
        self.build(context_dir)
