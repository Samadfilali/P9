#!/usr/bin/env python
# coding: utf-8

# # Projet 9 : Partie 1
# Cette partie permet de charger les données et produire le fichier pour la génération de la matrice de recommandation
# le 23/02/2021

# In[3]:


#request.urlretrieve("https://s3-eu-west-1.amazonaws.com/static.oc-static.com/prod/courses/files/AI+Engineer/Project+9+-+R%C3%A9alisez+une+application+mobile+de+recommandation+de+contenu/news-portal-user-interactions-by-globocom.zip","archive.zip")
#import zipfile
#zip_ref = zipfile.ZipFile("archive.zip", 'r') 
#zip_ref.extractall("./input") 
#zip_ref.close() 


# In[4]:


import warnings
warnings.filterwarnings('ignore')

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from random import seed
from random import randint
seed(42)
from datetime import datetime
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import _pickle as cPickle
import pickle 


# # I) Chargement des données

# # II) Préparation des données
# En entrée : frame 
# - Calcul de la variable RatingArticle pour évaluer chaque article par chaque lecteur
# - Suppression des couples (lecteur,article) dont le temps de lecture dépasse 4s par mot
# - Suppression des articles les plus populaires dont le nombre de lecteurs dépasse 4945
# - Suppression des articles les moins populaires dont le nombre de lecteurs est au dessous de 1051
# 
# En sortie : DF_csv.csv

# In[8]:


def load_prepare_data(): 
    # chargement des fichiers
    li = []
    for dirname, _, filenames in os.walk('./input/clicks/clicks'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            df = pd.read_csv(os.path.join(dirname, filename), index_col=None, header=0)
            li.append(df)
            
    frame = pd.concat(li, axis=0, ignore_index=True)
    df_articles = pd.read_csv('./input/articles_metadata.csv', index_col=None, header=0)
    # Concaténation des deux tables
    frame=frame.merge(df_articles, left_on='click_article_id', right_on='article_id', how='left')
    # drop columns
    columns_deleted=["click_article_id","created_at_ts","publisher_id"]
    frame.drop(columns_deleted, axis='columns', inplace=True)
    
    # fonction de calcul du temps écoulé par article
    frame['RatingArticle']=0
    session_id=-1
    for index, row in frame.iterrows():
        words_count= row['words_count']
        if words_count==0 : 
            words_count=1
        if session_id == row['session_id'] :
            date_end = row['click_timestamp']//1000 
            frame['RatingArticle'].loc[index]=int(((date_end - date_beg)/words_count)*10)
        else :
            date_beg = row['session_start']//1000
            date_end = row['click_timestamp']//1000
            frame['RatingArticle'].loc[index]=int(((date_end - date_beg)/words_count)*10)
            
        session_id = row['session_id']    
        date_beg=date_end
        
    # sauvegarde du dataframe complet
    frame.to_csv("./output/frame.csv",index=False)
    
    ## II-2) Suppression des couples (lecteur,article) ayant un RatingArticle très élevé
    columns=["user_id","article_id","RatingArticle"]
    DF=frame[columns]
    rating_threshold=DF["RatingArticle"].quantile(0.9)
    DF.drop(DF.loc[DF['RatingArticle'] > rating_threshold].index, inplace=True)
    
    ## II-3) Suppression des articles les plus populaires : concerne les articles les plus populaires dont le nombre de lecteurs dépasse 4945
    X=frame["article_id"].value_counts().keys()
    Y=frame["article_id"].value_counts().values
    temp=pd.DataFrame({'article_id' :X, 'TotalRatingCount': Y})
    DF = DF.merge(temp, left_on = 'article_id', right_on = 'article_id', how = 'left')
    popularity_threshold=DF['TotalRatingCount'].quantile(0.6)
    DF.drop(DF.loc[DF['TotalRatingCount'] > popularity_threshold].index, inplace=True)
    
    ## II-4) Suppression des articles les moins populaires : Ceci concerne les articles dont les lecteurs ne dépassent pas 1051
    unpopularity_threshold=DF['TotalRatingCount'].quantile(0.5)
    DF.drop(DF.loc[DF['TotalRatingCount'] < unpopularity_threshold].index, inplace=True)
    
    ## II-5) Sauvegarde des DataFrame DF
    DF.to_csv('./output/DF_csv.csv',index=False)
    
    #preparation de la matrice
    # suppression des doublons
    DF = DF.drop_duplicates(['user_id', 'article_id'])
    DF_pivot = DF.pivot(index = 'user_id', columns = 'article_id', values = 'RatingArticle').fillna(0)
    user_rating_matrix = csr_matrix(DF_pivot.values)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(user_rating_matrix)
    
    # Sauvegarde du modelèe en binaire 
    knnPickle = open('./output/knnpickle_file', 'wb') 
    # source, destination 
    pickle.dump(model_knn, knnPickle)   
    


# In[ ]:


if __name__ == "__main__":
    load_prepare_data()


# In[ ]:




