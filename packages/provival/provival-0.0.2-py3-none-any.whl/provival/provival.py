from scipy.stats import zscore
import decoupler as dc
import pandas as pd
import pickle
from importlib.resources import files


# Import Reference Signature Database
def load_pickle_file(file_name):
    # Resolve the path to the pickle file relative to the package
    file_path = files('provival.data').joinpath(file_name)
    with open(file_path, 'rb') as handle:
        return pickle.load(handle)

db_gs_human = load_pickle_file('SC_DB_Human.pickle')
db_gs_mouse = load_pickle_file('SC_DB_Mouse.pickle')
db_metadata = load_pickle_file('SC_DB_Metadata.pickle')

# Generate Mouse-specific Signature Database
db_gs_mouse_net = []
for x in db_gs_mouse.keys():
    db_gs_mouse_signature = pd.DataFrame(columns = ['source', 'target', 'weight'])
    db_gs_mouse_signature['target'] = db_gs_mouse[x]
    db_gs_mouse_signature['source'] = x
    db_gs_mouse_signature['weight'] = 1

    db_gs_mouse_net.append(db_gs_mouse_signature)

db_gs_mouse_net = pd.concat(db_gs_mouse_net)
db_gs_mouse_net.reset_index(drop=True, inplace=True)
db_gs_mouse_net.drop_duplicates(inplace=True)

# Generate Human-specific Signature Database
db_gs_human_net = []
for x in db_gs_human.keys():
    db_gs_human_signature = pd.DataFrame(columns = ['source', 'target', 'weight'])
    db_gs_human_signature['target'] = db_gs_human[x]
    db_gs_human_signature['source'] = x
    db_gs_human_signature['weight'] = 1

    db_gs_human_net.append(db_gs_human_signature)

db_gs_human_net = pd.concat(db_gs_human_net)
db_gs_human_net.reset_index(drop=True, inplace=True)
db_gs_human_net.drop_duplicates(inplace=True)

# Provival Score
def provival_score(input_data, input_model='Human', group1_signature='proCSC', group2_signature='revCSC', group1_model='Human', group2_model='Human', method='MLM', use_raw=False):
    # Input Model
    if input_model == 'Mouse':
        db_net = db_gs_mouse_net
    elif input_model == 'Human':
        db_net = db_gs_human_net
    else:
        raise ValueError("Parameter 'input_model' must be one of ['Mouse', 'Human'].")
    
    # Group 1 Signature
    if group1_signature not in ['CSC', 'proCSC', 'revCSC']:
        raise ValueError("Parameter 'group1_signature' must be one of ['CSC', 'proCSC', 'revCSC'].")
    
    # Group 2 Signature
    if group2_signature not in ['CSC', 'proCSC', 'revCSC']:
        raise ValueError("Parameter 'group2_signature' must be one of ['CSC', 'proCSC', 'revCSC'].")
    
    # Group 1 Model
    if group1_model == 'Mouse':
        group1_metadata = db_metadata[(db_metadata['Signature Category'] == group1_signature) & (db_metadata['Model'] == group1_model)]
    elif group1_model == 'Human':
        group1_metadata = db_metadata[(db_metadata['Signature Category'] == group1_signature) & (db_metadata['Model'] == group1_model)]
    elif group1_model == 'All':
        group1_metadata = db_metadata[(db_metadata['Signature Category'] == group1_signature)]
    else:
        raise ValueError("Parameter 'group1_model' must be one of ['Mouse', 'Human', 'All'].")
    
    # Group 2 Model
    if group2_model == 'Mouse':
        group2_metadata = db_metadata[(db_metadata['Signature Category'] == group2_signature) & (db_metadata['Model'] == group2_model)]
    elif group2_model == 'Human':
        group2_metadata = db_metadata[(db_metadata['Signature Category'] == group2_signature) & (db_metadata['Model'] == group2_model)]
    elif group2_model == 'All':
        group2_metadata = db_metadata[(db_metadata['Signature Category'] == group2_signature)]
    else:
        raise ValueError("Parameter 'group2_model' must be one of ['Mouse', 'Human', 'All'].")
    
    # Method
    if method == 'MLM':
        est, p = dc.run_mlm(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'ULM':
        est, p = dc.run_ulm(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'VIPER':
        est, p = dc.run_viper(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'WMEAN':
        est, p = dc.run_wmean(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'WSUM':
        est, p = dc.run_wsum(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'UDT':
        est, p = dc.run_udt(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'MDT':
        est, p = dc.run_mdt(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            weight='weight',
            verbose=True,
            use_raw=use_raw)
    elif method == 'AUCELL':
        est, p = dc.run_mdt(
            mat=input_data,
            net=db_net,
            source='source',
            target='target',
            verbose=True,
            use_raw=use_raw)
    else:
        raise ValueError("Parameter 'method' must be one of ['MLM', 'ULM', 'VIPER', 'WMEAN', 'WSUM', 'UDT', 'MDT', 'AUCELL'].")
    
    # Score Estimate
    group1_est = zscore(est)[list(set(group1_metadata.index) & set(est.columns))]
    group2_est = zscore(est)[list(set(group2_metadata.index) & set(est.columns))]
    
    est[group2_signature] = group2_est.mean(axis=1)
    est[group1_signature] = group1_est.mean(axis=1)
    
    est['Provival_Score'] = est[group2_signature] - est[group1_signature]
    
    return est, p