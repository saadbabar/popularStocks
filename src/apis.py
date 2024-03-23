import requests
import json

def get_top_wsb_stocks():
    url = 'https://tradestie.com/api/v1/apps/reddit'

    try:
        # making get request to api
        response = requests.get(url)

        # check request success
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: failed to fetch data. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error:{e}")
        return None
    
top50stocks = get_top_wsb_stocks()
if top50stocks:
    result = top50stocks

    output_file = 'db.json'
    with open (output_file, 'w') as f:
        json.dump(result, f, indent=4)

    print(f"Output written to {output_file}")
else:
    print("Unable to fetch data")