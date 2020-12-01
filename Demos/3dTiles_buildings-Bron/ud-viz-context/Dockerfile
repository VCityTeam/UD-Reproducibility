FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker"

RUN apt-get update

######### Install UD-Viz and build it with npm
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN apt-get install -y git

RUN mkdir -p WebDemos
WORKDIR /WebDemos
RUN git clone -b ifc https://github.com/clementcolin/UD-Viz.git
WORKDIR /WebDemos/UD-Viz/UD-Viz-Core
# FIXME: the should be a single configuration file for this demo !
COPY DemoBron examples/
RUN npm install
RUN npm run build 

######### Install apache2
# Although serving the site can be done by running `npm start` when on
# a desktop, it seems that using npm in a containerized context is not
# that simple, refer e.g. to https://github.com/iTowns/itowns/issues/1503.
# Note that a rapid test of the proposed solution of this issue (the one
# using a command of the form `CMD [ "npm", "start", "--", "--host=0.0.0.0" ]`)
# does _not_ seem to be effective in this context.
# The current workaround, that might be a little overkill, consists in
# using an independent httpd server to serve the JS/html code that was 
# build (refer above) with npm. 

# tzdata is an apache2 package dependency that requires some interactive
# configuration. The following is a non interactive workaround, refer to
# https://stackoverflow.com/questions/8671308/non-interactive-method-for-dpkg-reconfigure-tzdata/20693661
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NONINTERACTIVE_SEEN=true
RUN echo "tzdata tzdata/Areas select Europe" > preseed.txt
RUN echo "tzdata tzdata/Zones/Europe select Berlin" >> preseed.txt
RUN debconf-set-selections preseed.txt

RUN apt-get install -y apache2

######### Expose (through http) UD-Viz
# The site definition will expose the content of the above defined
# WebDemos directory
COPY apache2_udv_demo.conf /etc/apache2/sites-available/dockerized_udv_demo.conf

# Remove the default server (which is a symlink anyhow) to avoid collisions:
RUN rm -f /etc/apache2/sites-enabled/000-default.conf 

# Enable the virtual site
RUN a2ensite dockerized_udv_demo.conf

######### Expose (through http) the Tilesets required by UD-Viz demos
# Appache2 configuration defines DocumentRoot as being
# /WebDemos/UD-Viz/UD-Viz-Core. We thus copy content in 
# sub-directory of Document Root.
#
# References concerning the wget ad-hoc flags
# https://askubuntu.com/questions/719410/wget-web-crawler-retrieves-unwanted-index-html-index-files
WORKDIR /WebDemos/UD-Viz/UD-Viz-Core

EXPOSE 80
# Launch httpd. Reference
# - https://stackoverflow.com/questions/44376852/how-to-start-apache2-automatically-in-a-ubuntu-docker-container
CMD [ "apache2ctl", "-D", "FOREGROUND" ]
