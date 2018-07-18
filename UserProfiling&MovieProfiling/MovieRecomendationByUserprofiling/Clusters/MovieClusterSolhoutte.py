
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans  # KMeans clustering
import matplotlib.pyplot as plt
import sys
import json
import pypyodbc
from sklearn.metrics import silhouette_score

con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
cursor = con.cursor()
data = pd.read_csv("E:\MovieRecomendationByUserprofiling\Clusters\MovieInfoF.csv")

data_use = data.ix[:,
           ['Tbl_ID','Genre', 'keywords', 'title', 'director', 'imdb_rating','imdb_votes','releasedYear','PolarityConfidence','actors','writter']]

data_use['title'] = [i.replace("\xa0", "") for i in list(data_use['title'])]

# --------------------------------
# print(data_use.shape)
# clean_data = data_use.dropna(axis=0)
# print(clean_data.shape)
#
# clean_data = clean_data.reset_index(drop=True)
# print(clean_data.shape)
# data_use=clean_data

dataArray = data_use.as_matrix(columns=None)
# print(dataArray)
tempArray = []

i = 0
for m in dataArray:
    i += 1
    n = m.tolist()
    # print(n[0])
    tempArray.append(n[0])


# --------------------------------
people_list = []
for i in range(data_use.shape[0]):
    # print("jj",i)
    name1 = data_use.ix[i, 'releasedYear']
    name2 = data_use.ix[i, 'director']
    name3 = str(data_use.ix[i, 'imdb_rating'])
    name4 = str(data_use.ix[i, 'imdb_votes'])
    name5 = str(data_use.ix[i, 'PolarityConfidence'])
    name6 = str(data_use.ix[i, 'actors'])
    name7 = str(data_use.ix[i, 'writter'])

    people_list.append("|".join([
        str(name1),
        str(name2),
        str(name3),
        str(name4),
        str(name5),
        str(name6),
        str(name7)
    ]))
data_use['movie'] = people_list

# saveClusters = ("UPDATE tbl_movie SET cluster = %s WHERE imdb_id = %s")
# findIdFromTitle = ('SELECT id FROM tbl_movie WHERE title = %s')
# saveUserPrefs = ('UPDATE tbl_user SET recommonded_non_p = %s WHERE username = %s')

# cnx = pymysql.connect(host='localhost', user='root', password='', db='movia',
#                       charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
# cursor = cnx.cursor()

# --------------------------------
from sklearn.feature_extraction.text import CountVectorizer


def token(text):
    return (text.split(","))
def tokenn(text):
    return (text.split(" "))


cv_kw = CountVectorizer(max_features=100, tokenizer=token)
keywords = cv_kw.fit_transform(data_use["keywords"].values.astype('U'))
keywords_list = ["kw_" + i for i in cv_kw.get_feature_names()]

cv_ge = CountVectorizer(tokenizer=tokenn)
genres = cv_ge.fit_transform(data_use["Genre"].values.astype('U'))
genres_list = ["genres_" + i for i in cv_ge.get_feature_names()]

cv_pp = CountVectorizer(max_features=100, tokenizer=token)
people = cv_pp.fit_transform(data_use["movie"])
people_list = ["pp_" + i for i in cv_pp.get_feature_names()]

cluster_data = np.hstack([keywords.todense() * 6
                             , genres.todense() * 5
                             , people.todense() * 4
                          ])

criterion_list = keywords_list \
                 + genres_list \
                 + people_list

cluster_range = range( 1, 30 )
cluster_errors = []
# for num_clusters in cluster_range:
#   clusters = KMeans( num_clusters )
#   clusters.fit( cluster_data )
#   cluster_errors.append( clusters.inertia_ )
# clusters_df = pd.DataFrame( { "num_clusters":cluster_range, "cluster_errors": cluster_errors } )
# print(clusters_df[0:30])
# plt.figure(figsize=(20,20))
# plt.plot( clusters_df.num_clusters, clusters_df.cluster_errors, marker = "o" )
# plt.show()


mod = KMeans(n_clusters=12, n_init=12, init='k-means++')

category = mod.fit_predict(cluster_data)


# find center of clusters
centers = mod.cluster_centers_

plt.figure(figsize=(10, 10))
plt.scatter(centers[:, 0], centers[:, 1], marker='x', s=169, linewidths=3,
            color='r', zorder=10)


category_dataframe = pd.DataFrame({"category": category}, index=data_use['title'])
numpyMatrix = category_dataframe.as_matrix()
data_use.ix[list(category_dataframe['category'] == 0),['title']]
mm = category_dataframe['category'].values.tolist()

results = [] # this is a dictionary

# plt.show()

i = 0

for n in range(2, 30):
    mod = KMeans(n_clusters=n)

    category = mod.fit_predict(cluster_data)
    label = mod.labels_
    sil_coeff = silhouette_score(cluster_data, label, metric='euclidean')
    # print(sil_coeff)
    print("For n_clusters={}, The Silhouette Coefficient is {}".format(n, sil_coeff))

# for x in tempArray:
#     # print("ggggggggg",mm[i])
#     # print("hhhhhhhhhhhhhhh",x)
#     # cursor.execute("UPDATE Movieinfos SET cluster='" + str(mm[i]) + "' WHERE Tbl_ID =" + str(x))
#     # cursor.commit()
#
#     results.append({x:mm[i]})
#     i += 1

    # print("ffffffffffff",results)
# plt.show()




    #
    #
