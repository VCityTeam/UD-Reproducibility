# output_dir = 'junk'
# vintages = [2009, 2012, 2015]
# boroughs = [
#             'LYON_1ER',
#             'LYON_2EME',
#             'LYON_3EME',
#             'LYON_4EME',
#             'LYON_5EME',
#             'LYON_6EME',
#             'LYON_7EME',
#             'LYON_8EME',
#             'LYON_9EME'
# ]
# databases = {
#     2009: {
#         'PG_HOST': '192.168.1.51',
#         'PG_PORT': '5432',
#         'PG_NAME': 'citydb-full_lyon-2009',
#         'PG_USER': 'postgres',
#         'PG_PASSWORD': 'postgres'
#     },
#     2012: {
#         'PG_HOST': '192.168.1.51',
#         'PG_PORT': '5433',
#         'PG_NAME': 'citydb-full_lyon-2012',
#         'PG_USER': 'postgres',
#         'PG_PASSWORD': 'postgres'
#     },
#     2015: {
#         'PG_HOST': '192.168.1.51',
#         'PG_PORT': '5434',
#         'PG_NAME': 'citydb-full_lyon-2015',
#         'PG_USER': 'postgres',
#         'PG_PASSWORD': 'postgres'
#     }
# }

output_dir = 'junk'
vintages = [2009, 2012]
boroughs = ['LYON_1ER']
db_config_files = ['CityTilerDBConfig2009.yml', 'CityTilerDBConfig2012.yml']
databases = {
    2009: {
        'PG_HOST': '192.168.1.51',
        'PG_PORT': '5432',
        'PG_NAME': 'citydb-full_lyon-2009',
        'PG_USER': 'postgres',
        'PG_PASSWORD': 'postgres'
    },
    2012: {
        'PG_HOST': '192.168.1.51',
        'PG_PORT': '5433',
        'PG_NAME': 'citydb-full_lyon-2012',
        'PG_USER': 'postgres',
        'PG_PASSWORD': 'postgres'
    }
}
