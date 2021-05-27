import pandas as pd
import numpy as np
from random import randint
import matplotlib.pyplot as plt


data = pd.read_excel('Sales.xlsx', index_col=0)

no_of_clusters = int(input("Please enter the number of clusters: "))

# Create initial centroids
centroid_index = []
# Create initial centroids
for _ in range(no_of_clusters):
    value = randint(0, 199)
    centroid_index.append(value)

#Check of there are duplicate indices (duplicate indices will generate empty clusters)
while(len(centroid_index) != len(set(centroid_index))):
    centroid_index.clear()
    for _ in range(no_of_clusters):
        value = randint(0, 199)
        centroid_index.append(value)

# centroid_index = [i for i in range (no_of_clusters)]
print("Intitial centroids is rows :", centroid_index)

clusters_dict = {}

# Create Clusters dataframe
for key in range(len(centroid_index)):
    clusters_dict['Cluster ' + str(key)] = [[]]
clusters = pd.DataFrame.from_dict(clusters_dict)
# Contain all the distances calculated by manhatten
distance = []
# Contain the cluster number for each row
which_cluster = []

# Distance calculations (Manhatten)
for label, row in data.iterrows():
    for i in centroid_index:
        distance.append(sum(abs(data.iloc[i, :] - row)))
    which_cluster.append(distance.index(min(distance)))
    distance.clear()

# Put the products in their clusters
for index, cluster in enumerate(which_cluster):
    clusters.iloc[0, cluster].append(index)

# print(clusters)

old_which_cluster = []
flag = True

while (flag):
    which_cluster = []
    new_centroids = []
    # Create new centroids from means
    for cluster in range(len(clusters.columns)):
        inner_list = []
        for column in range(len(data.columns)):
            inner_list.append(data.iloc[clusters.iloc[0, cluster], column].mean())
        new_centroids.append(inner_list)
    # print(new_centroids)

    # Connvert the new_centroid list to np.array to make it ready for calculations
    new_centroids_math = np.array(new_centroids)
    # Distance calculations (Manhatten)
    for label, row in data.iterrows():
        for centroid in new_centroids_math:
            distance.append(sum(abs(centroid - row)))
        which_cluster.append(distance.index(min(distance)))
        distance.clear()

    # Check if the algorithm end or not
    if (old_which_cluster == which_cluster):
        flag = False
        continue

    # Delete the old clusters to update it
    for cluster in range(len(clusters.columns)):
        clusters.iloc[0, cluster] = []
    # Put the products in their clusters
    for index, cluster in enumerate(which_cluster):
        clusters.iloc[0, cluster].append(index)
    # print(clusters)
    old_which_cluster = which_cluster.copy()

counts = []
names = data.index.values

for cluster in range(len(clusters.columns)):
    print('\n' + "-------------Cluster " + str(cluster) + '-------------:' + '\n')
    print(names[clusters.iloc[0, cluster]])
    counts.append(len(names[clusters.iloc[0, cluster]]))

title = [cluster for cluster in clusters.columns]

fig,ax = plt.subplots()
ax.bar(title,counts)
plt.show()