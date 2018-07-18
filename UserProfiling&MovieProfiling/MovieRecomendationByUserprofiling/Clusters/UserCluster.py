
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
data = pd.read_csv("E:\MovieRecomendationByUserprofiling\Clusters\\UserInfoNew.csv")

data_use = data.ix[:,
           ['Id','Name','MovieCategory', 'Movies', 'gender', 'age', 'keywords','AvLikesCount','AvHeartCount','AvReviewPolarity','AvThreadpolarity']]

data_use['Name'] = [i.replace("\xa0", "") for i in list(data_use['Name'])]

# --------------------------------
print(data_use.shape)
# clean_data = data_use.dropna(axis=0)
# print(clean_data.shape)



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
count_list = []
for i in range(data_use.shape[0]):
    print("jj",i)
    name1 = str(data_use.ix[i, 'AvLikesCount'])
    name2 = str(data_use.ix[i, 'AvHeartCount'])
    name3 = str(data_use.ix[i, 'AvReviewPolarity'])
    name4 = str(data_use.ix[i, 'AvThreadpolarity'])
    name5 = str(data_use.ix[i, 'gender'])
    name6 = str(data_use.ix[i, 'age'])


    count_list.append("|".join([
        str(name1),
        str(name2),
        str(name3),
        str(name4),
        str(name5),
        str(name6)
    ]))
data_use['count'] = count_list



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


cv_kw = CountVectorizer(max_features=100, tokenizer=token)
keywords = cv_kw.fit_transform(data_use["keywords"].values.astype('U'))
keywords_list = ["kw_" + i for i in cv_kw.get_feature_names()]

cv_ge = CountVectorizer(tokenizer=token)
genres = cv_ge.fit_transform(data_use["MovieCategory"])
genres_list = ["genres_" + i for i in cv_ge.get_feature_names()]

cv_pp = CountVectorizer(max_features=100, tokenizer=token)
movie = cv_pp.fit_transform(data_use["Movies"])
movie_list = ["pp_" + i for i in cv_pp.get_feature_names()]

cv_pp = CountVectorizer(max_features=100, tokenizer=token)
count = cv_pp.fit_transform(data_use["count"])
count_list = ["pp_" + i for i in cv_pp.get_feature_names()]

cluster_data = np.hstack([keywords.todense() * 5
                             , genres.todense() * 5
                             , movie.todense() * 4
                             ,count.todense()*2
                          ])

criterion_list = keywords_list \
                 + genres_list \
                 + movie_list \
                 + count_list
cluster_range = range( 1, 30 )
cluster_errors = []
for num_clusters in cluster_range:
  print(num_clusters,"kkkkkkkkkkkkkkkkkkkkkkkkkk")
  clusters = KMeans( num_clusters )
  clusters.fit( cluster_data )
  cluster_errors.append( clusters.inertia_ )
clusters_df = pd.DataFrame( { "num_clusters":cluster_range, "cluster_errors": cluster_errors } )
print(clusters_df[0:30])
plt.figure(figsize=(20,20))
plt.plot( clusters_df.num_clusters, clusters_df.cluster_errors, marker = "o" )
plt.show()


mod = KMeans(n_clusters=4, n_init=4, init='k-means++')

category = mod.fit_predict(cluster_data)


# find center of clusters
centers = mod.cluster_centers_

plt.figure(figsize=(10, 10))
plt.scatter(centers[:, 0], centers[:, 1], marker='x', s=169, linewidths=3,
            color='r', zorder=10)


category_dataframe = pd.DataFrame({"category": category}, index=data_use['Name'])
numpyMatrix = category_dataframe.as_matrix()
data_use.ix[list(category_dataframe['category'] == 0),['Name']]
mm = category_dataframe['category'].values.tolist()

results = [] # this is a dictionary

plt.show()
i = 0

for n in range(2, 30):
    mod = KMeans(n_clusters=n)

    category = mod.fit_predict(cluster_data)
    label = mod.labels_
    sil_coeff = silhouette_score(cluster_data, label, metric='euclidean')
    # print(sil_coeff)
    print("For n_clusters={}, The Silhouette Coefficient is {}".format(n, sil_coeff))


for x in tempArray:
    print("ggggggggg",mm[i])
    print("hhhhhhhhhhhhhhh",x)
    cursor.execute("UPDATE UserInfo SET cluster='" + str(mm[i]) + "' WHERE Id =" + str(x))
    cursor.commit()
    #
    results.append({x:mm[i]})
    i += 1

    print("ffffffffffff",results)
plt.show()
    #
    #
