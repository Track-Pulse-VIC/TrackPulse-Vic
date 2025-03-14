import requests
from hashlib import sha1
import hmac
from dotenv import dotenv_values
import os

def getUrlDownloader(request):
    # ENV READING
    parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(parent_folder, '.env')
    config = dotenv_values(env_path)

    
    devId = config['DEV_ID']
    key = bytes(config['KEY'], "utf-8")
    request = request + ('&' if ('?' in request) else '?')
    raw = request + 'devid={0}'.format(devId)
    
    # Encode the raw string
    raw_encoded = raw.encode('utf-8')
    
    hashed = hmac.new(key, raw_encoded, sha1)
    signature = hashed.hexdigest()
    return 'http://timetableapi.ptv.vic.gov.au' + raw + '&signature={1}'.format(devId, signature)

def api_route_list(number):
    try:
        # API endpoint URL
        url = getUrlDownloader(f'/v3/routes?route_types={number}')
        print(f"Search url: {url}")
        
        # Make the GET request
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            formatted = format(data)
            print(formatted)
            return(data)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(e)

def api_stop_list(number, route_id):
    try:
        # API endpoint URL
        url = getUrlDownloader(f'/v3/stops/route/{route_id}/route_type/{number}')
        print(f"Search url: {url}")
        
        # Make the GET request
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            formatted = format(data)
            print(formatted)
            return(data)
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(e)

def downloader_function(type):
    if type == 0:
        type_name = 'metro'
    if type == 1:
        type_name = 'tram'
    if type == 2:
        type_name = 'bus'
    if type == 3:
        type_name = 'vline'
    
    pre_file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','w')
    pre_file.write('')
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','a')

    data1 = api_route_list(type)
    for route in data1['routes']:
        route_id = route['route_id']

        data2 = api_stop_list(type, route_id)
        try:
            for stop in data2['stops']:
                stop_name = stop['stop_name']
                file.write(f'{stop_name}\n')
        except Exception as e:
            print(e)


    #deletes repeated entries
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','r')
    lines = file.readlines()
    print(lines)
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','w')
    file.write(''.join(set(lines)))

    #sorts stops alphabetically
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','r')
    lines = file.readlines()
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','w')
    file.write(''.join(sorted(lines)))

    #removes blank last line
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','r')
    lines = file.readlines()
    last_line = None
    for line in lines:
        last_line = line
    last_line = last_line.rstrip()
    lines[-1] = last_line
    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','w')
    file.write(''.join(lines))

    file = open(f'utils\\datalists\\autogeneratedptvlists\\{type_name}stops.txt','r')
    print(file)