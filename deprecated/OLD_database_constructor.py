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

    today_dt = dt.datetime.today()
    today = '_'.join(str(today_dt).split(' '))
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
    
    # Creating New Master Files
    old_file = 'master_tables/master_' + type_of_req + '_table.csv'
    old_master = pd.read_csv(old_file)
    new_master = old_master.append(df).groupby('timestamp', sort=True).agg('first')
    master_csv_name = 'master_tables/master_' + type_of_req + '_table'
    new_master.reset_index().to_csv(master_csv_name + '.csv', index=False)
    
    counts = data['count']
    uniques = data['uniques']
    old_master_sum = pd.read_csv('master_tables/master_' + type_of_req + '_summary.csv')
    new_master_sum_dict = [{'collection_timestamp': str(today_dt), 'counts': counts, 'uniques': uniques}]
    new_master_sum = pd.DataFrame(new_master_sum_dict)
    new_master_sum = old_master_sum.append(new_master_sum).groupby('collection_timestamp').agg('first')
    master_csv_summary_name = 'master_tables/master_' + type_of_req + '_summary'
    new_master_sum.reset_index().to_csv(master_csv_summary_name + '.csv', index=False)
    
if __name__ == "__main__":
    args = createArgs()
    main(args.user, args.password, 'views')
    main(args.user, args.password, 'clones')
    
