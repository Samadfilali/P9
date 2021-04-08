#!/usr/bin/env python
# coding: utf-8

# # Projet 9  : Partie II 
# Cette partie permet de charger les données et produire le fichier pour la génération de la matrice de recommandation

# In[1]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from random import seed
from random import randint
seed(42)
from datetime import datetime

import _pickle as cPickle
import pickle 


# # I) Chargement des données

# In[2]:


def getFiveArticles_CF(DF,DF_pivot,frame,model_knn,userId) :
    if not(userId in DF_pivot.index) :
        return "CB"
    else :
        distances, users = model_knn.kneighbors(DF_pivot.iloc[userId,:].values.reshape(1, -1), n_neighbors = 6)
        df1= DF[DF.user_id.isin(users[0])].sort_values(by = 'RatingArticle',ascending = False).reset_index()
        ind=0
        nbre=0
        resultat=[]
        while nbre!= 5 :
            if not(df1["article_id"].iloc[ind] in frame["article_id"][frame["user_id"]==users[0][0]].values) :
                resultat.append(df1["article_id"].iloc[ind])
                nbre+=1
            ind+=1
        return resultat


# In[3]:


def getFiveArticles_CB(e, userId):
    ee=e
    #get all articles read by user
    var= frame.loc[frame['user_id']==userId]['article_id'].tolist()
    #chose randomly one
    value = randint(0, len(var))
    #delete all read articles except the selected one( we do not want to offer user to read something he already read)
    for i in range(0, len(var)):
        if i != value:
            ee=np.delete(ee,[i],0)
    arr=[]
    
    #delecte selected article in the new matrix
    f=np.delete(ee,[value],0)
    #get 5 articles the most similar to the selected one
    for i in range(0,5):
        distances = distance.cdist([ee[value]], f, "cosine")[0]
        min_index = np.argmin(distances)
        f=np.delete(f,[min_index],0)
        #find corresponding matrix in original martix
        result = np.where(e == f[min_index])
        arr.append(result[0][0])
        
    return arr


# In[4]:


def getFiveArticles(DF_arg,DF_pivot_arg,frame_arg,model_knn_arg,e_arg,userId) :
    if userId in DF_pivot_arg.index :
        articles = getFiveArticles_CF(DF_arg,DF_pivot_arg,frame_arg,model_knn_arg,userId) 
    else :
        articles=getFiveArticles_CB(e_arg, userId)
    
    return articles


# In[5]:


def main():
    pass 


# In[6]:


if __name__ == "__main__":
    main()
 


# In[ ]:




