import pandas as pd
import pandas as pd
import numpy as np


def marketing_measure(data,prob,ID,target, i_percent,bins):
    data = pd.DataFrame(data)
    data['quantile_bins'] = pd.qcut(data[prob], q=bins, labels=False)
    data = data.groupby('quantile_bins').agg({prob:['min','max'],ID:'count',target :'sum'}).reset_index()
    
    data.columns = data.columns.map("_".join)
    min_col = prob+'_min'
    max_col = prob+'_max'
    id_col = ID +'_count'
    target_col = target+'_sum'
    data.rename(columns = {'quantile_bins_':'bin',	min_col :'min_score',	max_col:'max_score',	id_col:'count',	target_col:'target'}, inplace = True)
    df = data
    df['events'] = df['target'] 
    df['nonevents'] = df['count']- df['target']
    
    df['rand_events']= df['target'].sum()/bins
    df['total_events'] = df['target'].sum()
    df['total_nonevents'] = df['nonevents'].sum()
    df['event_rate'] = df.events / df['total_events']
    df['non_event_rate'] = df.nonevents / df['total_nonevents']
    df['cumulative_eventrate'] = (df['target']/df['total_events']).cumsum()
    df['cumulative_non_event_rate'] = (df['nonevents']/df['total_nonevents']).cumsum()
    df['cumulative_random_rate'] = df['rand_events'].cumsum() / df['target'].sum()
    
    df['KS'] = np.round(df['cumulative_eventrate'] - df['cumulative_non_event_rate'], 3) * 100
    df['lift'] = df['cumulative_eventrate'] / df['cumulative_random_rate']
    df['Max_KS'] = max(df['KS'])
    df['a_percent']= df['count']/df['count'].sum()
    df['i_percent']= i_percent
    df['Decile_PSI']= (df['a_percent']-df['i_percent'])*(np.log(df['a_percent']/df['i_percent']))
    df['PSI'] = df['Decile_PSI'].sum()
    
    return (df[['bin','min_score','max_score','count','events','nonevents','rand_events','total_events','total_nonevents','event_rate'
              ,'non_event_rate','cumulative_eventrate','cumulative_non_event_rate','cumulative_random_rate','KS','lift','Max_KS','a_percent','i_percent','Decile_PSI','PSI']])

def generate_propensity_score_dataset():

    n_rows = 10000
    
    # Generate customer_id (1 to 1000)
    customer_id = np.arange(1, n_rows + 1)
    
    # Generate random propensity scores between 0 and 1
    propensity_score = np.random.rand(n_rows)
    
    # Generate random target values (binary 0 or 1)
    target = np.random.randint(0, 2, n_rows)
    
    # Combine the data into a DataFrame
    data = {
        'customer_id': customer_id,
        'propensity_score': propensity_score,
        'target': target
    }
    
    data = pd.DataFrame(data)
    
    return data
    

