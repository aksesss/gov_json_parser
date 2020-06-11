import urllib
import json
import math
import time
import argparse
import urllib.request
import os
import os.path
import sys

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

def fileRowsCount(file_path, enc='utf8'):
    return (sum([1 for line in open(file_path, encoding=enc)]))
    


DATA_PATH = 'data'
MAX_PAGE_SIZE = 1000


ap = argparse.ArgumentParser()

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
ap.add_argument('-s', '--startpage',
                help='from what page download data',
                required=False,
                nargs='?', 
                default=1, 
                type=int)
ap.add_argument('-e', '--encoding',
                help='Data encoding: urf8, 1251 (cp1251)',
                required=False,
                nargs='?', 
                default='utf8', 
                type=str)



try:
    args = vars(ap.parse_args())
except ():
    print('Error in args parsing')

if (args['filename'] == ''):
    FILE_NAME = args['datacode'] + '.json'
        
encoding = args['encoding']

URL = 'http://budget.gov.ru/epbs/registry/%s/data'%(args['datacode'])
FILE_PATH = args['path'] + '/' + FILE_NAME
start_page = args['startpage']

if (args['limit'] < 1):
    recordCount = getRecordCount(URL)
else:
    recordCount = min(args['limit'], getRecordCount(URL)) 

record_count_in_url = getRecordCount(URL)
    
print('Using URL : {}'.format(URL))
print('\tN rows from url : {}'.format(record_count_in_url))
print('\tn pages from url: {}'.format(math.ceil(record_count_in_url/MAX_PAGE_SIZE)))
    
    
    
if (os.path.isfile(FILE_PATH) and (start_page == 1)):
    
    print('The file {} exists\n\tN records in file : {}'.format(FILE_NAME, fileRowsCount(FILE_PATH, encoding)))
    pages_in_file = math.ceil(fileRowsCount(FILE_PATH, encoding)/1000)
    print('\tn pages in file   : {}'.format(pages_in_file))
    while True:
        update_question = input('Append data? [y, n]: ')
        if (update_question=='y'):
            start_page = int(input('From what page from what u want download: '))
            
            if (start_page <= pages_in_file):
                warning = input('WARNING!: are u shure? Data may be doubled [y, n]: ')
                if (warning != 'y'):
                    sys.exit()

            break
        elif (update_question=='n'):
            delete_question = input('Do you want rewrite to file[y, n]: ')
            if (delete_question == 'y'):
                os.remove(FILE_PATH)
                break
            else:
                sys.exit()
        else:
            sys.exit()

            





'''    
if ('datacode' in args.keys()):
    URL = 'http://budget.gov.ru/epbs/registry/%s/data'%(args['datacode'])
else:
    URL = None
if ('path' in args.keys()):
    FILE_PATH = args['path']
'''

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
    print('\nLoading ended')
    print('\tLoaded records        : {}'.format(i))
    print('\tTotal records in url  : {}'.format(record_count_in_url))
    print('\tTotal records in file : {}'.format(fileRowsCount(FILE_PATH, encoding)))

except KeyboardInterrupt:
    print('\nLoading stopped')
    print('\tLoaded records        : {}\n'.format(i))
    print('\tTotal records in url  : {}'.format(record_count_in_url))
    print('\tTotal records in file : {}'.format(fileRowsCount(FILE_PATH, encoding)))

except Exception as e:
    print(str(e))

finally:
    with open(FILE_PATH, 'rb+') as the_file:
        the_file.seek(-3, os.SEEK_END)
        the_file.truncate()
    with open(FILE_PATH, 'a', encoding=encoding) as the_file:
        the_file.write(']}')