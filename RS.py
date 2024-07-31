# Import everything needed
import numpy as np
import pandas as pd

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from pprint import pprint

# Importing dataset needed and prepreprocessing data
dataset = pd.read_csv("./ml-latest-small/movies.csv")
dataset2 = pd.read_csv("./ml-latest-small/ratings.csv")

dataset = dataset.drop_duplicates(subset="title")
datasetN = dataset.drop("genres", axis="columns")
datasetN2 = dataset2.drop("timestamp", axis="columns")
df = pd.merge(datasetN2, datasetN, how="inner", on="movieId")

#Personalised function
def similarUser(user, recAmount):
    knn = np.asarray([newPivotDf.values[user-1]])
    distance, index = knnModel.kneighbors(knn, n_neighbors=recAmount+1)
    return index.flatten()[1:] + 1, distance.flatten()[1:]

def recommendMovies(n):
  n = min(len(meanRating),n)
  pprint(list(movieListId[np.argsort(meanRating)[::-1][:n]]))

# Create Pivot Table
pivotDf = df.pivot(index='userId', columns='title', values='rating')
newPivotDf = pivotDf.fillna(0)
sparsePivotDf = csr_matrix(newPivotDf.values)

# Create knn model
knnModel = NearestNeighbors(metric='cosine', algorithm='brute')
knnModel.fit(sparsePivotDf)

#Non PS function
def createMovieRank(data, N):
    trainDataGrouped = data.groupby(['title']).agg({'userId': 'count'}).reset_index()
    trainDataGrouped.rename(columns = {'userId': 'score'}, inplace=True)
    
    trainDataSort = trainDataGrouped.sort_values(['score', 'title'], ascending = [0,1])
    trainDataSort['Rank'] = trainDataSort['score'].rank(ascending = False, method = 'first')
    
    topNMovies = trainDataSort.head(N)
    
    return topNMovies

def recommend(data):
    topNMovies = data
    cols = topNMovies.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    topNMovies = topNMovies[cols]

    #Nice output
    topMoviesReturn = topNMovies.title.to_string(index=False)

    return print(topMoviesReturn)


# Main running of Code
while True:
    choice = int(input("Type 1 for Personalised Recommended System, Type 2 for Non Personalised RS, 3 to Exit: "))
    if choice == 1:
        userInput = int(input("Input your user Id(0-610): "))
        userInput2 = int(input("Input the amount of users you want to recommend against(5-610): "))

        similarUserList, distanceList = similarUser(userInput, userInput2)

        tempVal = np.sum(distanceList)
        weightingList = distanceList/tempVal

        movieSimilar = newPivotDf.values[similarUserList]

        movieListId = newPivotDf.columns

        weightingList = weightingList[:,np.newaxis] + np.zeros(len(movieListId))

        ratingMatrix = weightingList*movieSimilar
        meanRating = ratingMatrix.sum(axis=0)

        recAm = int(input("How many movies would you like Recommended(3-20): "))
        recommendMovies(recAm)
    elif choice == 2:
        userInput = int(input("Input your user Id(0-610): "))
        recAm = int(input("How many movies would you like Recommended(3-20): "))
        topNMovies = createMovieRank(df, recAm)

        recommend(topNMovies)
    elif choice == 3:
        break