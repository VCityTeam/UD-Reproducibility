#Download base image 
ARG UBUNTU_VERSION=20.04
FROM ubuntu:${UBUNTU_VERSION} as base
# Reference of the original Dockerfile
# https://github.com/DGtal-team/DGtal/blob/master/Dockerfile

### Update 
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update

### Install tools
RUN apt -y install curl
RUN apt -y install clang-9
RUN apt -y install build-essential
RUN apt -y install g++
RUN apt -y install git 
RUN apt -y install cmake
RUN apt -y install doxygen

#### Install gl libraries
# FIXME RUN apt -y update --fix-missing
RUN apt -y install mesa-common-dev libglm-dev mesa-utils

### Install libraries
RUN apt -y install libboost-all-dev
RUN apt -y install libcgal*
RUN apt -y install libcgal-dev
RUN apt -y install libmagick++-dev
RUN apt -y install graphicsmagick*
RUN apt -y install libinsighttoolkit4-dev
RUN apt -y install libqglviewer-dev-qt5
RUN apt -y install libgmp-dev
RUN apt -y install libeigen3-dev
RUN apt -y install libfftw3-dev
RUN apt-get clean

#### User to install 
RUN groupadd -g 1000 digital
RUN useradd -d /home/digital -s /bin/bash -m digital -u 1000 -g 1000
RUN usermod -aG sudo digital

#### Install DGtal basic package 
RUN git clone https://github.com/DGtal-team/DGtal.git                     \
  /home/digital/git/DGtal                                               &&\
  cd /home/digital/git/DGtal                                            &&\
  git checkout 77bd36304
RUN mkdir /home/digital/git/DGtal/build                                 &&\ 
  cd /home/digital/git/DGtal/build                                      &&\
  cmake .. -DWITH_GMP=true -DWITH_EIGEN=true -DWITH_FFTW3=true            \
  -DWITH_CGAL=true -DWITH_ITK=true -DWITH_OPENMP=true                     \
  -DWITH_CAIRO=true -DWITH_QGLVIEWER=true -DWITH_MAGICK=true            &&\
  make install

#### DGtalTools is an extension of DGtal required by GRIM:
RUN git clone https://github.com/DGtal-team/DGtalTools.git                \
  /home/digital/git/DGtalTools                                          &&\
  cd /home/digital/git/DGtalTools                                       &&\
  git checkout ad8e3c8
RUN mkdir -p /home/digital/git/DGtalTools/build                         &&\
  cd /home/digital/git/DGtalTools/build                                 &&\
  cmake .. -DWITH_ITK=true                                              &&\ 
  make install

#### added for GRIM : pc2vol
RUN apt update                                                          &&\
  apt install -y xorg-dev libglu1-mesa-dev                              &&\
  apt install -y wget
RUN mkdir /home/pc2vol                                                  &&\
  cd /home/pc2vol                                                       &&\
  wget https://cmake.org/files/v3.19/cmake-3.19.8-Linux-x86_64.tar.gz   &&\
  tar -xzf cmake-3.19.8-Linux-x86_64.tar.gz                             &&\
  wget https://github.com/libigl/libigl/archive/refs/tags/v2.5.0.tar.gz &&\
  tar -xzf v2.5.0.tar.gz
RUN cd /home/pc2vol                                                     &&\
  git clone https://github.com/dcoeurjo/pc2vol                          &&\
  cd pc2vol && git checkout 410717f                                     &&\
  mkdir build && cd build                                               &&\
  /home/pc2vol/cmake-3.19.8-Linux-x86_64/bin/cmake                        \
  -DWITH_LIBIGL=ON  -DWITH_CGAL=ON  -DWITH_GMP=ON                         \ 
  -DLIBIGL_DIR=/home/pc2vol/libigl-2.5.0 ..                             &&\
  # cmake must be called a second time because of a bug in cmake
  /home/pc2vol/cmake-3.19.8-Linux-x86_64/bin/cmake                        \
  -DWITH_LIBIGL=ON  -DWITH_CGAL=ON  -DWITH_GMP=ON                         \
  -DLIBIGL_DIR=/home/pc2vol/libigl-2.5.0 ..                             &&\
  make                                                                  &&\
  # Brutal "install" command required because make install fails
  cp pc2vol /usr/local/bin


# DEBUG NOTS
#CMD vol2obj  /home/digital/git/DGtal/examples/samples/bunny-32.vol  /datademo/bunny.obj
