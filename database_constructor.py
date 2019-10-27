import pandas as pd
import datetime as dt
import subprocess
import json
import os
import argparse

def createArgs():
    parser = argparse.ArgumentParser(description='Must enter username, token/password, and the path to the base csv for views and clones')
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('-p', '--password', type=str)
    parser.add_argument('-oc', '--old_ref_path_clones', type=str)
    parser.add_argument('-ov', '--old_ref_path_views', type=str)
    return parser.parse_args()

def grabNewDataAndStoreCSV(user, token, kind):
    auth = user + ':' + token
    url = 'https://api.github.com/repos/movidius/ncappzoo/traffic/' + kind
    today_dt = dt.datetime.today()
    today = '_'.join(str(today_dt).split(' '))
    today = '-'.join(str(today.split('.')[0]).split(':'))
    folder_name = 'ncappzoo_' + kind + '_' + today
    file_name = folder_name + '/' + 'ncappzoo_' + kind + '_' + today

    os.mkdir(folder_name)
    test = subprocess.Popen(["curl", "-u", auth, url, ">", file_name], stdout=subprocess.PIPE)
    out, err = test.communicate()
    decoded_string = out.decode("utf-8").replace("'", '""').replace('\n', '')
    data = json.loads(decoded_string)
    
    counts = data['count']
    uniques = data['uniques']
    timestamp_data = data[kind]
    df = pd.DataFrame(timestamp_data)
    
    timestamps = [x.split('T')[0] for x in df['timestamp'].values]
    df['day'] = [x.split('-')[2] for x in timestamps]
    df['mo'] = [x.split('-')[1] for x in timestamps]
    df['yr'] = [x.split('-')[0] for x in timestamps]
    df['collection_timestamp'] = [today_dt for x in range(len(timestamps))]
    
    json_string = json.dumps(data, indent=4, sort_keys=True)
    f = open(file_name + '.json', 'a')
    f.write(json_string)
    f.close()
    csv_string = df.to_csv(file_name + '.csv', index=False)
    return file_name + '.csv'

def construct_new_ref(old_file_path, new_file_path, kind):
    old_master_df = pd.read_csv(old_file_path)
    new_df = pd.read_csv(new_file_path)
    yrs = [x for x in new_df['yr'].values]
    mos = [x for x in new_df['mo'].values]
    dys = [x for x in new_df['day'].values]
    new_df['yr_mo_day'] = [dt.datetime(yrs[i], mos[i], dys[i]) for i in range(len(yrs))]
    
    # Reorder columsn for both dfs for alignment
    new_df = new_df[old_master_df.columns.values]
    
    # Construction of new ref
    new_master = old_master_df.append(new_df).groupby('timestamp').max().reset_index()
    yrs = [x for x in new_master['yr'].values]
    mos = [x for x in new_master['mo'].values]
    dys = [x for x in new_master['day'].values]
    new_master['yr_mo_day'] = [dt.datetime(yrs[i], mos[i], dys[i]) for i in range(len(yrs))]
    
    today_dt = dt.datetime.today()
    today = '_'.join(str(today_dt).split(' '))
    today = '-'.join(str(today.split('.')[0]).split(':'))
    file_name = 'temp/updated_' + kind + '_' + today
    csv_string = new_master.to_csv(file_name + '.csv', index=False)
    return file_name + '.csv'
    
if __name__ == "__main__":
    args = createArgs()
    
    new_file = grabNewDataAndStoreCSV(args.user, args.password,'views')
    old_ref = args.old_ref_path_views
    new_ref_views = construct_new_ref(old_ref, new_file, 'views')
    
    new_file = grabNewDataAndStoreCSV(args.user, args.password,'clones')
    old_ref = args.old_ref_path_clones
    new_ref_clones = construct_new_ref(old_ref, new_file, 'clones')
    
    print('New Clones Reference File:', new_ref_clones)
    print('New Views Reference File:', new_ref_views)
    
