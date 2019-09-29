import pandas as pd
import datetime as dt
import subprocess
import json
import os
import argparse

def createArgs():
    parser = argparse.ArgumentParser(description='Must enter username and token/password')
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('-p', '--password', type=str)
    return parser.parse_args()

def main(user, password, type_of_req):
    auth = user + ':' + password
    url = 'https://api.github.com/repos/movidius/ncappzoo/traffic/' + type_of_req
    
    today = '_'.join(str(dt.datetime.today()).split(' '))
    today = '-'.join(str(today.split('.')[0]).split(':'))
    folder_name = 'ncappzoo_' + type_of_req + '_' + today
    file_name = folder_name + '/' + 'ncappzoo_' + type_of_req + '_' + today
    os.mkdir(folder_name)

    # Curling to get around Github Auth
    test = subprocess.Popen(["curl", "-u", auth, url, file_name], stdout=subprocess.PIPE)
    out, err = test.communicate()
    if err:
        sys.exit(1)
    decoded_string = out.decode("utf-8").replace("'", '""').replace('\n', '')
    data = json.loads(decoded_string)

    # Converting to DataFrame
    timestamp_data = data[type_of_req]
    df = pd.DataFrame(timestamp_data)
    timestamps = [x.split('T')[0] for x in df['timestamp'].values]
    df['day'] = [x.split('-')[2] for x in timestamps]
    df['mo'] = [x.split('-')[1] for x in timestamps]
    df['yr'] = [x.split('-')[0] for x in timestamps]
    
    # Writing JSON
    json_string = json.dumps(data, indent=4, sort_keys=True)
    f = open(file_name + '.json', 'a')
    f.write(json_string)
    f.close()
    
    # Writing CSV
    df.to_csv(file_name + '.csv', index=False)
    
if __name__ == "__main__":
    args = createArgs()
    main(args.user, args.password, 'views')
    main(args.user, args.password, 'clones')
    
