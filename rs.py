# Content based filtering : Eg is Netflix ( like genre, actor, etc)
# Collaberative filtering : Eg is Amazon (Buy a phone, it recommends headphone, screen guard, case, etc)

# Here, we are gonna code a movie recommender system . Explain the tables. 

#1
import numpy as np #numpy for multidimensional arrays
import pandas as pd #pandas for working on the datasets

#5
import matplotlib.pyplot as plt  # 2D plotting library
import seaborn as sns # statistical data visualization library. High level interfacing for statistical graphs.

# get the data

#2
columnNames = ['userId', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep = '\t', names = columnNames)
df.head()

# Explain table

#3
movieTitles = pd.read_csv("Movie_Id_Titles")
movieTitles.head()

# Merging both the tables

#4
df = pd.merge(df, movieTitles, on='item_id')
df.head()

# Now we are gonna perform some exploratory data analysis to find out more about or data frame

# Create ratings dataframe with avg and number of ratings
#6
df.groupby('title')['rating'].mean().sort_values(ascending=False).head()

#7
#How many ratings given

df.groupby('title')['rating'].count().sort_values(ascending=False).head()

#8 putting the mean value in the df
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings.head()
# print(ratings)

#9 Integrate the count one
ratings['number of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
ratings.head()
# print(ratings)

#10 Histogram with respect to ratings

plt.figure(figsize=(10,4))
ratings['rating'].hist(bins=70)
# plt.show()
# Follows normal guassian distribution. Follow the curve with mouse. 
# If we draw a probablity distribution function, it wopuld be following the curve

# Recommending similar movies

#11
moviemat  = df.pivot_table(index='userId', columns='title', values='rating')
moviemat.head()
# print(moviemat)

#12
#Now, suppose I watch Starwars, which movie am I going to get recommended based on the ratings 
#given by those who have watched starwars as well. 
# This is the problem statement.

# I have already created ratings dataframe. 
# Now am going to sort it based on the number of ratings
# Based on a selected movies, i try to find the correlation with the pivot table we have just created 
# and try to see which movie I'll get recommended

ratings.sort_values('number of ratings', ascending=True).head(10)
ratings.head()

#13
# Now, I watch Young Frankenstein . 
# Let's grab the user ratings of that particular movie and see what movie we get recommended.

youngFrankensteinRatings = moviemat['Young Frankenstein (1974)']
youngFrankensteinRatings.head()
# print(youngFrankensteinRatings)

#14
# WRT to this data, IO am goin to correlate with the pivot table as well as the user rating

similarToyoungFrankenstein = moviemat.corrwith(youngFrankensteinRatings)
# similarToyoungFrankenstein
# print(similarToyoungFrankenstein)

#15
# We dont need the NaN values. Lets remove that

corrYoungFrankenstein = pd.DataFrame(similarToyoungFrankenstein, columns=['Correlation'])
corrYoungFrankenstein.dropna(inplace=True)
# corrYoungFrankenstein.head()
# print(corrYoungFrankenstein)

#16
# Higher correlation , more is the chance for the movie to be recommended. 
# Some movies may have very few people giving ratings to it. So, what we do is, only if the movie is 
# rated by more than 100 people , I am going to recommend it.

# corrYoungFrankenstein.sort_values('Correlation', ascending=False)
# corrYoungFrankenstein.head(10)
# # print(corrYoungFrankenstein)

corrYoungFrankenstein = corrYoungFrankenstein.join(ratings['number of ratings'])
corrYoungFrankenstein.head()
# print(corrYoungFrankenstein)

# Only if time permits
corrYoungFrankenstein = corrYoungFrankenstein[corrYoungFrankenstein['number of ratings']>100]
corrYoungFrankenstein.head()
# print(corrYoungFrankenstein)

corrYoungFrankenstein = corrYoungFrankenstein.sort_values('Correlation', ascending=False)
corrYoungFrankenstein.head()
print(corrYoungFrankenstein)