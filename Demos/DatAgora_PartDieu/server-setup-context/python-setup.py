import os
import time
import socket

from geoserver.catalog import Catalog

def main():
  cat = Catalog("http://geoserver:8080/geoserver/rest",username = os.getenv('GEOSERVER_ADMIN_USER'),password = os.getenv('GEOSERVER_ADMIN_PASSWORD')) # add port with env var (os.getenv())
  s = socket.socket()

  connectionAttempts = 0
  maxConnectionAttempts = int(os.getenv('MAX_CONNECTION_ATTEMPTS')) 
  timeBetweenAttempts = int(os.getenv('TIME_CONNECTION_ATTEMPTS')) 

  imp_dir = os.getenv('DATA_IMPORT_DIR')
  cite = cat.get_workspace(os.getenv('WORKSPACE'))
  files = ["A=Difference_EVA_Artificialise-Routes","B=A-Voies_ferree","C=B-Batiments","EVA2015_Artif_Sols_Extent","EVA2015_Vegetation3STR_Extent","fpcvoieferree_Extent","Voirie_Extent"]

# Connection to Geoserver
  print("begin Geoserver connection attempts")

  while connectionAttempts < maxConnectionAttempts : 
    try:
      s.connect((socket.gethostbyname('geoserver'),8080))
    except socket.error :
      connectionAttempts += 1
      print("Geoserver not yet online, "+str(maxConnectionAttempts-connectionAttempts)+" connection attempts remaining")
      time.sleep(timeBetweenAttempts)
    else:
      break
  if connectionAttempts >= maxConnectionAttempts :
    print("server took too much time to respond. Aborting connection attempts")
    quit()

  print("Geoserver connection established")

# Geoserver shp import
  for f in files:
    shapefile_plus_sidecars = {
      'shp': os.path.join(imp_dir , f )+'.shp',
      'shx': os.path.join(imp_dir , f )+ '.shx',
      'prj': os.path.join(imp_dir , f )+'.prj',
      'dbf': os.path.join(imp_dir , f )+ '.dbf',
    }
    for g in shapefile_plus_sidecars.values() :
      open(g)
    ft = cat.create_featurestore(f, workspace=cite, data=shapefile_plus_sidecars)

if __name__ == "__main__":
  main()