# Importing libraries
import pandas as pd
import numpy as np
import math
import operator


data = pd.read_csv('home/projectTuneIn/projectTuneIn/depression_detection/training_data.csv')

# Defining a function which calculates euclidean distance between two data points
def euclideanDistance(data1, data2, length): # individually weighting the chosen parameters
    distance = 0
    distance += (1.5*(np.square(data1.iloc[0] - data2.iloc[0])))  #danceability
    distance += np.square(data1.iloc[1] - data2.iloc[1])  #acousticness
    distance += (1.5*(np.square(data1.iloc[2] - data2.iloc[2])))  #energy
    distance += np.square(data1.iloc[3] - data2.iloc[3])  #instrumentalness
    distance += (0.5*(np.square(data1.iloc[4] - data2.iloc[4])))  #liveness
    distance += (2*(np.square(data1.iloc[5] - data2.iloc[5])))  #valence
    distance += (1.5*(np.square(data1.iloc[6] - data2.iloc[6])))  #loudness
    distance += np.square(data1.iloc[7] - data2.iloc[7])  #speechiness
    distance += (1.5*(np.square(data1.iloc[8] - data2.iloc[8])))  #tempo
    return np.sqrt(distance)

# Defining the KNN model
def knn(trainingSet, testInstance, k):
    distances = {}
    sort = {}
    length = testInstance.shape[0]
    
    # Calculating euclidean distance between each row of training data and test data
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet.iloc[x], length)
        distances[x] = dist
 
    # Sorting them on the basis of distance
    sorted_d = sorted(distances.items(), key=operator.itemgetter(1))
 
    neighbors = []
    
    # Extracting top k neighbors
    for x in range(k):
        neighbors.append(sorted_d[x][0])

    classVotes = {}
    
    # Calculating the most freq class in the neighbors
    for x in range(len(neighbors)):
        response = trainingSet.iloc[neighbors[x]][-1]
 
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1

    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return(sortedVotes[0][0], neighbors)
