import os
from docker_helper import DockerHelperBuild, DockerHelperTask


class Docker3DUse(DockerHelperBuild, DockerHelperTask):

    def __init__(self):
        super().__init__('liris', '3DUse')
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   '3DUse-DockerContext')
        self.build(context_dir)

    def run(self):
        # Set input and output volumes
        self.add_volume(self.mounted_input_dir, '/Input', 'rw')
        if not self.mounted_input_dir == self.mounted_output_dir:
            # When mounting the same directory twice (which is the case when
            # the input and output directory are the same) then containers.run()
            # raises a docker.errors.ContainerError. Hence we only mount the
            # /Output volume when they both differ. Note that when this
            # happens the command in the derived class must be altered in order
            # to place its output in the /Input mounted point (because in this
            # /Output is (equal to) /Input.
            self.add_volume(self.mounted_output_dir, '/Output', 'rw')
        super().run()
