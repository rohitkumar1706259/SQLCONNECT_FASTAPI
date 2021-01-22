
'''


import configparser
#file='config.ini'
config=configparser.ConfigParser()
config.read(r'config.ini')
database_type=config.get('mount','database_type')
print(database_type)
'''

