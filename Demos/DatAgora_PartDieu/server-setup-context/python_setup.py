'''Importation of a set of data files to a geoserver.'''
import os
import sys
import time
import socket

from geoserver.catalog import Catalog, ConflictingDataError

def main():
  '''Main loop'''
  # ## Asserting that the Geoserver connection is effective
  print("Begin the Geoserver connection attempts")

  connection_attempts = 0
  max_connection_attempts = int(os.getenv('MAX_CONNECTION_ATTEMPTS'))
  delay_between_attempts = int(os.getenv('TIME_CONNECTION_ATTEMPTS'))

  while connection_attempts < max_connection_attempts:
    try:
      socket.socket().connect((socket.gethostbyname(os.getenv('GEOSERVER_SOCKET_HOST')),int(os.getenv('GEOSERVER_SOCKET_PORT'))))
    except socket.error:
      connection_attempts += 1
      print("Geoserver not yet online. Number of remaining attempts: " +
            str(max_connection_attempts-connection_attempts))
      time.sleep(delay_between_attempts)
    else:
      break
  if connection_attempts >= max_connection_attempts :
    print("Geoerver not answering after " +
          max_connection_attempts * delay_between_attempts +
          "seconds.")
    print("Geoserver-setup exiting on failure.")
    sys.exit(1)
  print("Geoserver connection established")

  # ## Proceeding with the data upload
  cat = Catalog(os.getenv('GEOSERVER_CATALOG_ADRESS'),
                username = os.getenv('GEOSERVER_ADMIN_USER'),
                password = os.getenv('GEOSERVER_ADMIN_PASSWORD'))

  # Definition of the filenames (radicals) to be imported:
  imp_dir = os.getenv('DATA_IMPORT_DIR')
  workspace = cat.get_workspace(os.getenv('WORKSPACE'))
  files_to_import = []

  for f in os.listdir(imp_dir) :
    if os.path.splitext(f)[0] not in files_to_import :
      files_to_import.append(os.path.splitext(f)[0])

  # Importation per se:
  for file_name in files_to_import:
    shapefile_plus_sidecars = {
      'shp': os.path.join(imp_dir , file_name )+'.shp',
      'shx': os.path.join(imp_dir , file_name )+ '.shx',
      'prj': os.path.join(imp_dir , file_name )+'.prj',
      'dbf': os.path.join(imp_dir , file_name )+ '.dbf',
    }
    try:
      cat.create_featurestore(file_name,
                              workspace=workspace,
                              data=shapefile_plus_sidecars)
      print(file_name + " successfully uploaded to geoserver.")
    except ConflictingDataError:
      print(file_name + " was already stored within the geoserver.")

  print("Geoserver-setup exiting with success.")

if __name__ == "__main__":
  main()
