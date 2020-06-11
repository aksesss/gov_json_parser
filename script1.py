import urllib
import json
import math
import time
import argparse
import urllib.request
import os


def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
        jsonData = json.loads(data)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData


def getRecordCount(url):
    js_data = getResponse(url + '?Pagenum={}&PageSize={}'.format(1, 1))
    return(js_data['recordCount'])


encoding = 'utf8'
DATA_PATH = 'data'
MAX_PAGE_SIZE = 1000


ap = argparse.ArgumentParser()
'''
ap.add_argument('-u', '--url',
                help='url of json load data API using Pagenum and PageSize url arguments', 
                nargs='?', 
                default=URL, 
                type=str)
'''

ap.add_argument('-c', '--datacode',
                help='Specificates open source data code\nYou shouldn\'t specificate URL [-u][-url]', 
                required=True,
                nargs='?', 
                type=str)
ap.add_argument('-p', '--path',
                help='Specificates file path',
                required=False,
                nargs='?', 
                default=DATA_PATH, 
                type=str)
ap.add_argument('-f', '--filename',
                help='Specificates file name',
                required=False,
                nargs='?',  
                type=str,
                default='')
ap.add_argument('-l', '--limit',
                help='Count of records to download',
                required=False,
                nargs='?', 
                default=-1, 
                type=int)
ap.add_argument('-P', '--frompage',
                help='from what page download data',
                required=False,
                nargs='?', 
                default=1, 
                type=int)


try:
    args = vars(ap.parse_args())
except ():
    print('Error in args parsing')

if (args['filename'] == ''):
    FILE_NAME = args['datacode'] + '.json'
        

start_page = args['frompage']
URL = 'http://budget.gov.ru/epbs/registry/%s/data'%(args['datacode'])
FILE_PATH = args['path']
FILE_PATH = FILE_PATH + '/' + FILE_NAME

if ('limit' in args.keys()):
    if (args['limit'] < 1):
        recordCount = getRecordCount(URL)
    else:
        recordCount = min(args['limit'], getRecordCount(URL)) 

'''    
if ('datacode' in args.keys()):
    URL = 'http://budget.gov.ru/epbs/registry/%s/data'%(args['datacode'])
else:
    URL = None
if ('path' in args.keys()):
    FILE_PATH = args['path']
'''

print('Using URL : {}'.format(URL))        
print('Turget file path: {}'.format(FILE_PATH))
        
start_time = time.time()
print("Start loading...")
i = 0


    
n_pages = math.ceil(recordCount/MAX_PAGE_SIZE)


try:
    if (start_page == 1):
        with open(FILE_PATH, 'a', encoding=encoding) as the_file:
            the_file.write('{"data": [')
    else:
        with open(FILE_PATH, 'rb+') as the_file:
            the_file.seek(-2, os.SEEK_END)
            the_file.truncate()
        with open(FILE_PATH, 'a', encoding=encoding) as the_file:
            the_file.write(',\n')

        
    for page_num in range(start_page, n_pages+1):
        print('Step {} of {}:\t'.format(page_num, n_pages), end='\t')
        js_data = getResponse(URL + '?Pagenum={}&PageSize={}'.format(page_num, MAX_PAGE_SIZE))
        data = js_data['data']    
        with open(FILE_PATH, 'a', encoding=encoding) as the_file:
        #with open(FILE_PATH, 'a', encoding='utf-8') as the_file:
            for record in data:
                i = i + 1 
                if (i == recordCount+1):
                    break
                json.dump(record, the_file, ensure_ascii=False)
                the_file.write(',\n')
        print('{} items loaded\t Time: {}'.format(i, time.time() - start_time))
except Exception as e:
    print(str(e))
finally:
    with open(FILE_PATH, 'rb+') as the_file:
        the_file.seek(-3, os.SEEK_END)
        the_file.truncate()
    with open(FILE_PATH, 'a', encoding=encoding) as the_file:
        the_file.write(']}')
