#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

cp rict2.liris.cnrs.fr.conf /etc/apache2/sites-available/

# Remove the default server (to avoid collisions):
rm -f /etc/apache2/sites-enabled/000-default.conf ## which is a symlink anyhow

a2ensite rict2.liris.cnrs.fr.conf              ## To enable the virtual site
systemctl reload apache2                       ## Relaunch the service
