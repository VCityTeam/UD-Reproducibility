# This is an example of configuration file that must be customized to
# suit your specific needs. For the documentation of meaning of the
# various parameters refer to the documentation of the static version
# i.e. `DemoStatic/demo_configuration_static.py`

output_dir = 'junk'
vintages = [2009, 2012, 2015]
city = 'LYON'
boroughs = [
           'LYON_1ER',
           'LYON_2EME',
           'LYON_3EME',
           'LYON_4EME',
           'LYON_5EME',
           'LYON_6EME',
           'LYON_7EME',
           'LYON_8EME',
           'LYON_9EME'
]

# Caveat emptor: although the `PG_HOST` parameter is present in each vintage
# entry, its value must be the same shared IP number value for the three
# values. This is because the three (3dCityDB) databases used by the workflow
# will run on the same host...
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
