#!/usr/bin/python3

import os.path
import sys
import shutil
import subprocess
import glob

# The CityTilers command doesn't offer a parameter flag in order to 
# specify an output directory. We thus have to collect the outputs
# and to move them to the /Output dir (that is by convention a
# docker mounted directory/volume).

command = ['python3']
kept_args = sys.argv[1:]    # The leading element is 'entrypoint.sh'

if len(kept_args) == 0 :
  # This was a request for the documentation (since no arguments).
  print("CityTiler (docker) expects at least two arguments :")
  print("  1. the Tiler to be applied: either Tiler or TemporalTiler")
  print("  2. the database server configuration file")
  print("When requesting the TemporalTiler ")
  print("  4-6 two additionnal database server configuration files ")
  print("  8-10 time stamps ")
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
kept_args = kept_args[1:]

if TilerMode == "Tiler":
  DBConfigFile = 'Tilers/CityTiler/'+kept_args[0]
  command.append(DBConfigFile)
elif TilerMode == "TemporalTiler":
  ### Deal with the database configuration files
  config_path_flag = kept_args[0]
  if not config_path_flag == "--db_config_path":
    print("The second argument should have been the --db_config_path flag.")
    print("The given argumen was ", config_path_flag)
    print("Exiting.")
    sys.exit()
  command.append(config_path_flag)
  for config_file in kept_args[1:4]:
    DBConfigFile = 'Tilers/CityTiler/'+config_file
    command.append(DBConfigFile)
  kept_args = kept_args[4:]

  ### Deal with the time stamps
  time_stamp_flag = kept_args[0]
  if not time_stamp_flag == "--time_stamp":
    print("The fifth argument should have been the --time_stamp flag.")
    print("The given argumen was ", time_stamp_flag)
    print("Exiting.")
    sys.exit()
  command.append(time_stamp_flag)
  for time_stamp in kept_args[1:4]:
    command.append(time_stamp)

  ### Hardwiring the differences files 
  command.append("--temporal_graph")
  difference_files = glob.glob('/Input/*DifferencesAsGraph.json')
  command.extend(difference_files)
  print("Final command :", command)


print("Launching command :", command)
subprocess.call(command)

if os.path.isdir('junk_buildings'):
  shutil.copytree('junk_buildings', '/Output/BuildingsTileset')

if os.path.isdir('junk'):
  shutil.copytree('junk', '/Output/TemporalTileset')

print( "Exiting ", TilerMode, " with success.")
