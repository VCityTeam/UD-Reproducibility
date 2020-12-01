This directory holds old shell-script based versions of demo
installers (together with their configuration files) for an
Ubuntu server.

The general usage was component oriented and would go
```
   sudo ./install-packages.sh               # general set-up
   sudo ./install-apache2.sh                # for the http server component
   sudo ./install-limonest-temporal.sh      # for a burough specific demo
```

Yet such an above based shell-script method carried the following
limitations:
 * lack of modularity: all the demos share a sme http server (or an 
   UD-Viz component) which doesn't accomodate multiple demos opposed
   by conflicting component versions (think of two versions)
 * has a big footprint: the considered installation host (bet it
   a desktop for DEV or a server for PROD) will be impacted 
   at the package level (with imposed/new software packages installed)
   or see some of its services (e.g. configuration files of the http
   server) modified
 * impose an Ubuntu server: this could be aleviated with tools like
   [ansible](https://www.ansible.com/) which is low level IT oriented
   (rarely known by scientific developers). 
 * impose an OS version (of Ubuntu): this can require some quite cumbersome
   deployment adaptation for a more recent/old OS version (even with the
   help of shell-scripts doing a part of the job)

