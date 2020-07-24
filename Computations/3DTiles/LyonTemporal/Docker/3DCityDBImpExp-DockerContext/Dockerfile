# 3DCityDB Importer/Exporter Dockerfile #######################################
#   Official website    https://www.3dcitydb.net
#   GitHub              https://github.com/3dcitydb/importer-exporter
###############################################################################
# Base image
ARG baseimage_tag='11'
FROM openjdk:${baseimage_tag}

# Labels ######################################################################
LABEL maintainer="Bruno Willenborg"
LABEL maintainer.email="b.willenborg(at)tum.de"
LABEL maintainer.organization="Chair of Geoinformatics, Technical University of Munich (TUM)"
LABEL source.repo="https://github.com/tum-gis/3dcitydb-importer-exporter-docker"

# Setup PostGIS and 3DCityDB ##################################################
ARG impexp_version='master'
ENV IMPEXP_VERSION=${impexp_version}

ARG BUILD_PACKAGES='git'

# Setup build and runtime deps
RUN set -x && \
  apt-get update && \
  apt-get install -y --no-install-recommends $BUILD_PACKAGES

# Clone 3DCityDB
RUN set -x && \
  mkdir -p build_tmp && \
  git clone -b "${IMPEXP_VERSION}" --depth 1 https://github.com/3dcitydb/importer-exporter.git build_tmp && \
  git checkout 8fddd30edbe2e21b37114182af33edc1379bc945

# Build ImpExp
RUN set -x && \
  cd build_tmp && \
  chmod u+x ./gradlew && \
  ./gradlew installDist

# Move dist
RUN set -x && \
  ls -lA . && \
  mv /build_tmp/impexp-client/build/install/3DCityDB-Importer-Exporter/ /impexp && \
  ls -lA /impexp

# create share folder structure
RUN set -x && \
  mkdir -p /share/config /share/data

# Cleanup
RUN set -x && \
  rm -rf build_tmp && \
  ls -lA && \
  apt-get purge -y --auto-remove $BUILD_PACKAGES && \
  rm -rf /var/lib/apt/lists/*

# Copy entrypoint script
COPY impexp.sh /impexp/bin

RUN set -x && \
  chmod -v u+x /impexp/bin/* /impexp/contribs/collada2gltf/COLLADA2GLTF*linux/COLLADA2GLTF*

WORKDIR /impexp
ENTRYPOINT [ "./bin/impexp.sh"]
