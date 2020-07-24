This docker context is a patch from the
[3dcitydb-importer-exporter-docker](https://github.com/tum-gis/3dcitydb-importer-exporter-docker),
sha1 [c232ebd750944136e6380ff7cee1330c42bd3cd4](https://github.com/tum-gis/3dcitydb-importer-exporter-docker/tree/c232ebd750944136e6380ff7cee1330c42bd3cd4).


### Technical details:

It seems that since version 4.2.2, 
[3DcityDB-Importer-Exporter](https://github.com/3dcitydb/importer-exporter) 
does not support the `-shell` CLI option anymore (which allows to run it without
the GUI, and which we need in our pipelines). In addition, version 4.2.2
cannot be installed anymore due to unsatisfied dependencies (osgeotools lib
in this case). Therefore, we modified the 
[3dcitydb-importer-exporter-docker](https://github.com/tum-gis/3dcitydb-importer-exporter-docker)
 to checkout a specific version of the 3DcityDB-Importer-Exporter  
(in this case, the current master version, sha1 
[8fddd30edbe2e21b37114182af33edc1379bc945](https://github.com/3dcitydb/importer-exporter/tree/8fddd30edbe2e21b37114182af33edc1379bc945)).

We made the following modification to the DockerFile (git diff output):

````
@@ -26,7 +26,8 @@ RUN set -x && \
 # Clone 3DCityDB
 RUN set -x && \
   mkdir -p build_tmp && \
-  git clone -b "${IMPEXP_VERSION}" --depth 1 https://github.com/3dcitydb/importer-exporter.git build_tmp
+  git clone -b "${IMPEXP_VERSION}" --depth 1 https://github.com/3dcitydb/importer-exporter.git build_tmp && \
+  git checkout 8fddd30edbe2e21b37114182af33edc1379bc945
 
 # Build ImpExp
 RUN set -x && \

````

We also updated the `impexp.sh` script to call the `impexp` binary with the
 instead of the `3DCityDB-Importer-Exporter` which does not
 support the `-shell` option (see the git diff bellow):

````
@@ -25,7 +25,7 @@ cat <<EOF
 EOF
 
 # Print version info
-./bin/3DCityDB-Importer-Exporter -shell -version
+./bin/impexp  -shell -version
  
 # Print cmd line passed to container
 printf "Following command line parameters are passed to the 3DCityDB ImporterExporter:\n"
@@ -33,4 +33,4 @@ printf "\n\t"
 echo "-shell $@"
 echo
 
-./bin/3DCityDB-Importer-Exporter -shell "$@"
+./bin/impexp  -shell "$@"
````
