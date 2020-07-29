#!/usr/bin/env bash

# Print commands and their arguments as they are executed
set -e;

# echo version info and maintainer
cat <<EOF


# 3DCityDB ImporterExporter Docker #############################################
################################################################################
#
#   3DCityDB ImporterExporter version $IMPEXP_VERSION
#     version info    https://github.com/3dcitydb/3dcitydb/tree/${IMPEXP_VERSION}
#
# Maintainer -------------------------------------------------------------------
#   Bruno Willenborg
#   Chair of Geoinformatics
#   Department of Civil, Geo and Environmental Engineering
#   Technical University of Munich (TUM)
#   b.willenborg(at)tum.de
#
################################################################################

EOF

# Print version info
./bin/impexp -shell -version
 
# Print cmd line passed to container
printf "Following command line parameters are passed to the 3DCityDB ImporterExporter:\n"
printf "\n\t"
echo "-shell $@"
echo

./bin/impexp -shell "$@"
