import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# load the geocode data into a Pandas dataframe
df = pd.read_csv('Metro Connect Trips October 2019_Zoning.csv')

# extract the latitude and longitude coordinates into a NumPy array
coordinates = df[['PickUp Lat', 'PickUp Lng']].values

# standardize the data using StandardScaler
scaler = StandardScaler()
coordinates_standardized = scaler.fit_transform(coordinates)

# apply K-Means clustering with 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(coordinates_standardized)

# add the cluster labels as a new column to the dataframe
df['Zone'] = kmeans.labels_

# save the updated dataframe to a new CSV file
df.to_csv('Metro Connect Trips October 2019_Zoned.csv', index=False)
