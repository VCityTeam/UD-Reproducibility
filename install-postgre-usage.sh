#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

## This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Refer to https://github.com/MEPP-team/UD-Serv/blob/master/API_Enhanced_City/INSTALL.md#manual-install

##### Configure the postgresql database
# Reference: https://stackoverflow.com/questions/8546759/how-to-check-if-a-postgres-user-exists
if sudo -u postgres -H sh -c "psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='citydb_user'" | grep -q 1"; then
  echo "Warning: user citydb_user already existed."
else
  sudo -u postgres -H sh -c "createuser citydb_user"
fi

# Refer to
if sudo -u postgres -H sh -c "psql postgres -lqt | cut -d \| -f 1 | grep -qw extendedDoc"; then
  echo "Warning: extenDoc database already existed."
else
  sudo -u postgres -H sh -c "createdb -O citydb_user extendedDoc"
fi
