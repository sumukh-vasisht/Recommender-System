import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

# print("Start : ")
# print(time.ctime())

columnNames = ['userId', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep = '\t', names = columnNames)
df.head()

movieTitles = pd.read_csv("Movie_Id_Titles")
movieTitles.head()

df = pd.merge(df, movieTitles, on='item_id')
df.head()

df.groupby('title')['rating'].mean().sort_values(ascending=False).head()
df.groupby('title')['rating'].count().sort_values(ascending=False).head()
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings.head()

ratings['number of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
ratings.head()

plt.figure(figsize=(10,4))
ratings['rating'].hist(bins=70)
# plt.show()

moviemat  = df.pivot_table(index='userId', columns='title', values='rating')
moviemat.head()

ratings.sort_values('number of ratings', ascending=True).head(10)
ratings.head()

youngFrankensteinRatings = moviemat['Young Frankenstein (1974)']
youngFrankensteinRatings.head()

similarToyoungFrankenstein = moviemat.corrwith(youngFrankensteinRatings)
corrYoungFrankenstein = pd.DataFrame(similarToyoungFrankenstein, columns=['Correlation'])
corrYoungFrankenstein.dropna(inplace=True)
corrYoungFrankenstein = corrYoungFrankenstein.join(ratings['number of ratings'])
corrYoungFrankenstein.head()

corrYoungFrankenstein = corrYoungFrankenstein[corrYoungFrankenstein['number of ratings']>100]
corrYoungFrankenstein.head()

corrYoungFrankenstein = corrYoungFrankenstein.sort_values('Correlation', ascending=False)
corrYoungFrankenstein.head()

# print("End : ")
# print(time.ctime())

print(corrYoungFrankenstein[1:5])