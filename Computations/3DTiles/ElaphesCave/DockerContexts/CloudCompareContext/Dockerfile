# This is a slightly modified copy of
# https://github.com/dockerstuff/docker-cloudcompare/blob/master/dockerfile/Dockerfile
# enabling to execute CloudeCompare without display.
FROM ubuntu:xenial

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update                                        &&\
  apt-get install -y git-core vim binutils                &&\
  apt-get install -y cmake g++ gcc                        &&\
  apt-get install -y                                        \
  libgdal-dev libfreenect-dev                               \
  libeigen3-dev libtbb-dev                                  \
  libavcodec-dev libavformat-dev                            \
  libavutil-dev libboost-thread-dev                         \
  libboost-program-options-dev                              \
  libcgal-dev libcgal-qt5-dev                               \
  libdlib-dev libswscale-dev                                \
  libtbb-dev libqt5opengl5-dev                              \
  qt5-default qttools5-dev                                  \
  qttools5-dev-tools libqt5svg5-dev                         \
  libproj-dev libdlib-dev
# Because we wish to run CC without the GUI
RUN apt-get install -y xvfb
RUN apt-get clean

RUN git clone --branch v2.10.2 --single-branch --recursive  \
  https://github.com/CloudCompare/CloudCompare.git

RUN mkdir -p /CloudCompare/build
RUN cd /CloudCompare/build               &&\
  cmake -DCMAKE_BUILD_TYPE=Release         \
  -DEIGEN_ROOT_DIR=/usr/include/eigen3     \
  -DCOMPILE_CC_CORE_LIB_WITH_TBB=ON        \
  -DOPTION_USE_DXF_LIB=ON                  \
  -DOPTION_USE_SHAPE_LIB=ON                \
  -DINSTALL_EXAMPLE_PLUGIN=ON              \
  -DINSTALL_EXAMPLE_GL_PLUGIN=ON           \
  -DINSTALL_EXAMPLE_IO_PLUGIN=ON           \
  -DINSTALL_QADDITIONAL_IO_PLUGIN=ON       \
  -DINSTALL_QANIMATION_PLUGIN=ON           \
  -DINSTALL_QBROOM_PLUGIN=ON               \
  -DINSTALL_QCOMPASS_PLUGIN=ON             \
  -DINSTALL_QCANUPO_PLUGIN=ON              \
  -DDLIB_ROOT=/usr/include                 \
  -DINSTALL_QCSF_PLUGIN=ON                 \
  -DINSTALL_QEDL_PLUGIN=ON                 \
  -DINSTALL_QFACETS_PLUGIN=ON              \
  -DINSTALL_QHOUGH_NORMALS_PLUGIN=ON       \
  -DINSTALL_QHPR_PLUGIN=ON                 \
  -DINSTALL_QM3C2_PLUGIN=ON                \
  -DINSTALL_QPCV_PLUGIN=ON                 \
  -DINSTALL_QPHOTOSCAN_IO_PLUGIN=ON        \
  -DINSTALL_QPOISSON_RECON_PLUGIN=ON       \
  -DINSTALL_QSRA_PLUGIN=ON                 \
  -DINSTALL_QSSAO_PLUGIN=ON                \
  -DBUILD_TESTING=ON                       \
  ..                                     &&\
  make                                   &&\
  make install                           &&\
  make clean

# Add our special entrypoint
#
# RUN git clone -b stable https://github.com/chbrandt/docker_entrypoint.git && \
#  ln -sf docker_entrypoint/entrypoint.sh /.
#
# ENTRYPOINT ["/entrypoint.sh"]
CMD ["xvfb-run", "/usr/local/bin/CloudCompare", "-SILENT"]
