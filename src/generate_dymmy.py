import pandas as pd
import numpy as np
from faker import Factory 

# create some fake data
fake = Factory.create('ja_JP')

# function to create a dataframe with fake values for our workers
def make_workers(num):
    
    # lists to randomly assign to workers
    status_list = ['Full Time', 'Part Time', 'Per Diem']
    team_list = [fake.color_name() for x in range(4)]
    

    fake_workers = [{'Worker ID':x+1000,
                  'Worker Name':fake.name(), 
                  'Hire Date':fake.date_between(start_date='-30y', end_date='today'),
                  'Worker Status':np.random.choice(status_list, p=[0.50, 0.30, 0.20]), # assign items from list with different probabilities
                  'Team':np.random.choice(team_list)} for x in range(num)]
        
    return fake_workers

worker_df = pd.DataFrame(make_workers(num=5000))
print(worker_df.head())