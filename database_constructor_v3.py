import pandas as pd
import datetime as dt
import github as gh
import subprocess
import json
import os
import argparse

def createArgs():
    parser = argparse.ArgumentParser(description='Must enter username, token/password, and the path to the base csv for views and clones. You can also include a master table of both views and clones. End result is a table of views and clones. Previous database constructors create two tables.')
    parser.add_argument('-u', '--user', type=str)
    parser.add_argument('-p', '--password', type=str)
    parser.add_argument('-oc', '--old_ref_path_clones', type=str)
    parser.add_argument('-ov', '--old_ref_path_views', type=str)
    parser.add_argument('-ovc', '--old_ref_path_views_clones', type=str)
    return parser.parse_args()

def grabNewDataAndStoreCSV(user, token, kind):
    g = gh.Github(user, token)
    repo = g.get_repo('movidius/ncappzoo')
    contents = repo.get_clones_traffic()
    if kind == 'views':
        contents = repo.get_views_traffic()
    
    today_dt = dt.datetime.today()
    today = '_'.join(str(today_dt).split(' '))
    today = '-'.join(str(today.split('.')[0]).split(':'))
    folder_name = 'past_collected_data/ncappzoo_' + kind + '_' + today
    file_name = folder_name + '/' + 'ncappzoo_' + kind + '_' + today

    os.mkdir(folder_name)
    data = {
        'count': contents['count'],
        'uniques': contents['uniques'],
        kind: [{
            'uniques': str(x.uniques), 
            'count': str(x.count), 
            'timestamp': str(x.timestamp.isoformat()) + 'Z'}
        for x in contents[kind]]
    }
    
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
    return new_master

def combine_new_sets(views_path, clones_path):
    views = pd.read_csv(views_path)
    clones = pd.read_csv(clones_path)
    
    if 'yr_mo_day' not in views.columns:
        yrs = [x for x in views['yr'].values]
        mos = [x for x in views['mo'].values]
        dys = [x for x in views['day'].values]
        views['yr_mo_day'] = [dt.datetime(yrs[i], mos[i], dys[i]) for i in range(len(yrs))]
    
    if 'yr_mo_day' not in clones.columns:
        yrs = [x for x in clones['yr'].values]
        mos = [x for x in clones['mo'].values]
        dys = [x for x in clones['day'].values]
        clones['yr_mo_day'] = [dt.datetime(yrs[i], mos[i], dys[i]) for i in range(len(yrs))]
    
    views_and_clones = views.merge(clones, how='outer', left_on='timestamp', right_on='timestamp', suffixes=['_views', '_clones'])
    views_and_clones = views_and_clones.drop(columns=['mo_views', 'yr_views', 'day_views', 'collection_timestamp_views', 'yr_mo_day_views'])
    drop_dict = {'mo_clones': 'mo', 'yr_clones': 'yr', 'day_clones': 'day', 'collection_timestamp_clones': 'collection_timestamp', 'yr_mo_day_clones': 'yr_mo_day'}
    views_and_clones = views_and_clones.rename(columns=drop_dict)
    df3_columns = ['timestamp', 'count_views', 'uniques_views', 'count_clones', 'uniques_clones', 'day', 'mo', 'yr', 'collection_timestamp', 'yr_mo_day']
    return views_and_clones[df3_columns]
    
if __name__ == "__main__":
    args = createArgs()
    
    new_file_views = grabNewDataAndStoreCSV(args.user, args.password,'views')
    old_ref_views = args.old_ref_path_views
    new_file_clones = grabNewDataAndStoreCSV(args.user, args.password,'clones')
    old_ref_clones = args.old_ref_path_clones
    new_ref = None
    new_ref_path = "No file created. Error in creation of table. Check inputs. Need clones table and views table paths or one clones-views table path"
    
    if args.old_ref_path_views and args.old_ref_path_clones:
        new_ref_views = construct_new_ref(old_ref_views, new_file_views, 'views')
        new_ref_clones = construct_new_ref(old_ref_clones, new_file_clones, 'clones')
        new_ref = combine_new_stats(new_ref_views, new_ref_clones)
    elif args.old_ref_path_views_clones::
        old_ref_df = pd.read_csv(args.old_ref_path_views_clones)
        new_addition = combine_new_sets(new_file_views, new_file_clones)
        new_ref = old_ref_path.append(new_addition)
        
    kind = 'views_and_clones"
    today_dt = dt.datetime.today()
    today = '_'.join(str(today_dt).split(' '))
    today = '-'.join(str(today.split('.')[0]).split(':'))
    file_name = 'master_tables/updated_' + kind + '_' + today
    new_ref.to_csv(filename + '.csv', index=False)
    new_ref_path = file_name + '.csv'
    print('New Views and Clones Reference File:', new_ref)   
