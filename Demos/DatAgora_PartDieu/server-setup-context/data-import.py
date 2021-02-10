import os
from geoserver.catalog import Catalog

cat = Catalog("http://localhost:"+ os.getenv('GEOSERVER_PORT') + "/geoserver/rest")
imp_dir = os.getenv('GEOSERVER_DATA_IMPORT_DIR')
topp = cat.get_workspace(os.getenv('GEOSERVER_WORKSPACE'))

shapefile_plus_sidecars = {
  'shp': 'prout/A=Difference_EVA_Artificialise-Routes.shp',
  'shx': 'prout/A=Difference_EVA_Artificialise-Routes.shx',
  'prj': 'prout/A=Difference_EVA_Artificialise-Routes.prj',
  'dbf': 'prout/A=Difference_EVA_Artificialise-Routes.dbf',
}
ft = cat.create_featurestore(imp_dir, workspace=topp, data=shapefile_plus_sidecars)