#!/usr/bin/python3

import os.path
import sys
import shutil
import subprocess

# The CityTilers command doesn't offer a parameter flag in order to 
# specify an output directory. We thus have to collect the outputs
# and to move them to the /Output dir (that is by convention a
# docker mounted directory/volume).

command = ['python3']
kept_args = sys.argv[1:]    # The leading element is 'entrypoint.sh'

if not len(kept_args) == 2 :
  # This was a request for the documentation (since no arguments).
  print("CityTiler (docker) expects two arguments :")
  print("  1. the Tiler to be applied: either Tiler or TemporalTiler")
  print("  2. the database server configuration file")
  print("Exiting.")
  sys.exit()

TilerMode = kept_args[0]
if TilerMode == "Tiler":
  command.append("Tilers/CityTiler/CityTiler.py")
elif TilerMode == "TemporalTiler":
  command.append("Tilers/CityTiler/CityTemporalTiler.py")
else:
  print("Tiler argument must either be Tiler or TemporalTiler but got: ",
        TilerMode)
  print("Exiting.")
  sys.exit()

if TilerMode == "Tiler":
  DBConfigFile = 'Tilers/CityTiler/'+kept_args[1]
  command.append(DBConfigFile)
elif TilerMode == "TemporalTiler":
  for config_file in kept_args[1:]:
    DBConfigFile = 'Tilers/CityTiler/'+config_file
  command.append(DBConfigFiles)

log_filename = 'TilerRun.log'
with open(log_filename, 'w') as out_file:
  subprocess.call(command, stderr=sys.stdout.buffer, stdout=out_file)

if os.path.isdir('junk_buildings'):
  shutil.copytree('junk_buildings', '/Output/BuildingsTileset')

if os.path.isfile(log_filename):
  shutil.move(log_filename, '/Output/'+log_filename)

print( "Exiting ", TilerMode, " with success.")
