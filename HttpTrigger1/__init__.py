
import logging
import azure.functions as func
import os, uuid
import pandas as pd
import p9_recommandation as pr
import _pickle as cPickle
import pickle
import urllib

logging.info('Python HTTP trigger function processed a request.')  
url ='https://stazur.blob.core.windows.net/contenertest/DF_csv.csv?sp=r&st=2021-04-08T09:46:06Z&se=2021-04-14T17:46:06Z&sv=2020-02-10&sr=b&sig=susLPxsuZ6NN8DMvxdG1zJClq7aL7f56VIcCJgv%2Blfs%3D'
DF = pd.read_csv(url)
DF = DF.drop_duplicates(['user_id', 'article_id'])
DF_pivot = DF.pivot(index = 'user_id', columns = 'article_id', values = 'RatingArticle').fillna(0)

url ='https://stazur.blob.core.windows.net/contenertest/frame.csv?sp=r&st=2021-04-08T09:54:54Z&se=2021-04-14T17:54:54Z&sv=2020-02-10&sr=b&sig=zMBOcR2LaWi5qvmJTHawEIQ55h5ACsKoa89r37fE9Uo%3D'
frame = pd.read_csv(url)   

url ='https://stazur.blob.core.windows.net/contenertest/knnpickle_file?sp=r&st=2021-04-08T10:00:17Z&se=2021-04-14T18:00:17Z&sv=2020-02-10&sr=b&sig=nnMKUiM0DZ8XVtyss9m8%2BTnV4msMLo35MgCTTAAyGqw%3D'
f = urllib.request.urlopen(url)
model_knn = pickle.load(f)
#with open(url, 'rb') as f:
#    model_knn = pickle.load(f)

url ='https://stazur.blob.core.windows.net/contenertest/articles_embeddings.pickle?sp=r&st=2021-04-08T09:56:41Z&se=2021-04-14T17:56:41Z&sv=2020-02-10&sr=b&sig=ZKTVx2Qm9eVqUSZlyVxBRSRlc1LXLrNkqUbMCzn93xE%3D'        
input_file = urllib.request.urlopen(url)
e = cPickle.load(input_file) 


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        articles = pr.getFiveArticles(DF,DF_pivot,frame,model_knn,e,int(name))
        return func.HttpResponse(f"{articles}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

