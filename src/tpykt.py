import configparser, requests, json


def main(): 
    config_reader = configparser.ConfigParser(allow_no_value=True)
    config_reader.read('src/config.ini')

    client_id = config_reader['MAIN']['client_id']
    client_secret = config_reader['MAIN']['client_secret']

    # No need to get device_code if there's already one.
    if (not config_reader['AUTOMATIC']['code']):
        print("Looks like you haven't got a device code yet! Let me generate one for you.....")
        
        auth_code = get_device_code(client_id)
        config_reader.set(section='AUTOMATIC', option='code', value=auth_code['device_code'])

        # Writes changes to the file.
        with open('src/config.ini', "w") as config_file:
            config_reader.write(config_file)

    if (not config_reader['AUTOMATIC']['access_token']):
        get_access_token(client_id, client_secret, config_reader['AUTOMATIC']['code'])

    
def get_device_code(client_id : str) -> json:
    """Retrives device_code and other useful information."""

    values = """
      {{ 
        "client_id": "{0}"
      }}
      """.format(client_id)

    headers = {
      'Content-Type': 'application/json'
    }
        
    request = requests.post('https://api.trakt.tv/oauth/device/code', data=values, headers=headers)      
    return request.json()
        

def get_access_token(client_id : str, client_secret : str, device_code : str) -> json:
    """Retrieves access_token, refresh_token and other useful information necessary for authentication."""

    values = """
      {{
        "code": "{0}",
        "client_id": "{1}",
        "client_secret": "{2}"
      }}
      """.format(device_code, client_id, client_secret)
      
    headers = {
      'Content-Type': 'application/json'
    }

    # TODO: Figure out why this request retrieves a 410.
    request = requests.post('https://api.trakt.tv/oauth/device/token', data=values, headers=headers)

    print(request.status_code)



if __name__ == '__main__':
    main()