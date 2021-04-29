# This is an example of configuration file that must be customized to
# suit your specific needs.
output_dir = 'junk'
vintage = 2015
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
           'LYON_9EME',
           'FEYZIN',
           'GIVORS',
           'GRIGNY',
           'IRIGNY',
           'PIERRE_BENITE',
           'SOLAIZE',
           'SAINT_FONS',
           'LYON_7EME',
           'VERNAISON'
]

database = {
  'PG_HOST': '192.168.1.14',
  'PG_PORT': '5435',
  'PG_NAME': 'citydb-lyon-chemistry-valley-2015-for_static',
  'PG_USER': 'postgres',
  'PG_PASSWORD': 'postgres'
}
