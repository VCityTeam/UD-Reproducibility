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
kept_args = sys.argv[1:]  # The leading element is 'entrypoint.sh'

if len(kept_args) == 0:
    # This was a request for the documentation (since no arguments).
    print("CityTiler (docker) expects at least two arguments :")
    print("  1. the Tiler to be applied: either Tiler or TemporalTiler")
    print("  2. the database server configuration file")
    print("When requesting the TemporalTiler ")
    print("  third to nth args: additionnal database servers configuration files,")
    print("  from n+1 to 2n+1 args: a time stamp (vintage) for each database.")
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
    DBConfigFile = kept_args.pop(0)
    if '/Input/' not in DBConfigFile:
       # The configuration file was not given through the mounted directory
       # and thus we assume it was copied in a "well-known" place (in the 
       # same directory as the Tiler python script). We must thus prefix
       # the configuration filename with the "well-known" path:
       DBConfigFile = 'Tilers/CityTiler/' + DBConfigFile
    else:
       # The configuration file was passed within a mounted directory and
       # its path should be already properly set (thus nothing to do): 
       print("Database configuration file passed through mounted /Input")
    command.append(DBConfigFile)
elif TilerMode == "TemporalTiler":
    # Deal with the database configuration files
    config_path_flag = kept_args.pop(0)
    if not config_path_flag == "--db_config_path":
        print("The second argument should have been the --db_config_path flag.")
        print("The given argument was ", config_path_flag)
        print("Exiting.")
        sys.exit()
    command.append(config_path_flag)
    # While there are arguments and while we do not encounter the --time_stamp
    # flag
    arg = kept_args.pop(0)
    while kept_args and arg != "--time_stamp":
        DBConfigFile = arg
        if '/Input/' not in arg:
           # The configuration file was not given through the mounted directory
           # and thus we assume it was copied in a "well-known" place (in the 
           # same directory as the Tiler python script). We must thus prefix
           # the configuration filename with the "well-known" path:
           DBConfigFile = 'Tilers/CityTiler/' + DBConfigFile
        command.append(DBConfigFile)
        arg = kept_args.pop(0)

    # Deal with the time stamps
    if not kept_args or arg != "--time_stamp":
        print("There should have been a --time_stamp flag. Exiting.")
        sys.exit()

    time_stamp_flag = arg
    command.append(time_stamp_flag)
    while kept_args:
        time_stamp = kept_args.pop(0)
        command.append(time_stamp)
    # Hardwiring the differences files
    command.append("--temporal_graph")
    difference_files = glob.glob(pathname='/Input/**/*DifferencesAsGraph.json',
                                 recursive=True)
    print('difference_files:')
    print(difference_files)
    command.extend(difference_files)
    print("Final command :", command)

print("Launching command :", command)
subprocess.call(command)

if os.path.isdir('junk_buildings'):
    shutil.copytree('junk_buildings', '/Output/BuildingsTileset')

if os.path.isdir('junk'):
    shutil.copytree('junk', '/Output/TemporalTileset')

print("Exiting ", TilerMode, " with success.")
