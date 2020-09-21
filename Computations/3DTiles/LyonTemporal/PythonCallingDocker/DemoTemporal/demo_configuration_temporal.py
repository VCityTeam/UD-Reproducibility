# This is an example of configuration file that must be customized to
# suit your specific needs.
output_dir = 'junk'
vintages = [2009, 2012, 2015]
city = 'LYON'
boroughs = [
           'LYON_1ER',
#          'LYON_2EME',
#          'LYON_3EME',
#          'LYON_4EME',
#          'LYON_5EME',
#          'LYON_6EME',
#          'LYON_7EME',
#          'LYON_8EME',
#          'LYON_9EME'
]

databases = {
    2009: {
        'PG_HOST': '134.214.143.170',
        'PG_PORT': '5432',
        'PG_NAME': 'citydb-full_lyon-2009',
        'PG_USER': 'postgres',
        'PG_PASSWORD': 'postgres'
    },
    2012: {
        'PG_HOST': '134.214.143.170',
        'PG_PORT': '5433',
        'PG_NAME': 'citydb-full_lyon-2012',
        'PG_USER': 'postgres',
        'PG_PASSWORD': 'postgres'
    },
    2015: {
        'PG_HOST': '134.214.143.170',
        'PG_PORT': '5434',
        'PG_NAME': 'citydb-full_lyon-2015',
        'PG_USER': 'postgres',
        'PG_PASSWORD': 'postgres'
    }
}
