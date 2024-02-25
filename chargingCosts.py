import pandas as pd
import numpy as np

class ChargingCosts:
    def __init__(self):
        
        price_data = pd.read_csv('price_data.csv', usecols=['Date', 'Hour Ending', 'Day Ahead'])
        price_data['Date'] = pd.to_datetime(price_data['Date'])
        price_data = price_data.pivot(index='Date', columns='Hour Ending', values='Day Ahead')
        
        # Change from hour ending to hour starting
        price_data = price_data.rename(columns={i: i-1 for i in range(1, 25)}) 
        
        # Change from price per MWh to kWh
        price_data = price_data/1000
        
        price_data['weekend'] = np.where(price_data.index.weekday.isin([5, 6]), 1, 0)
        self.data = price_data
        self.mean = price_data.drop(columns=['weekend']).mean().values
        self.cov_matrix = price_data.drop(columns=['weekend']).cov().values
          
    def simulate(self, num_samples : int = 1):
        return np.random.multivariate_normal(self.mean, self.cov_matrix, size=num_samples)
