import pandas as pd
import numpy as np
from pandas import DataFrame
from pymongo import MongoClient
from zipfile import ZipFile
#import tensorflow as tf
#from tensorflow import keras
#from tensorflow.keras import layers
from pathlib import Path
import matplotlib.pyplot as plt
import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId


def model(option,id_):
    #df1=pd.read_csv("summaries.csv",encoding = 'utf-8')
    #df2=pd.read_csv("Source_Address.csv")
    client = MongoClient("mongodb+srv://jpl-recommendation-content-user:CH4XwwixACf7hOxb@pie-dev.7azsc.mongodb.net/pie-development")
    db = client["pie-development"]
    

    if option=='headlines':
        client = MongoClient("mongodb+srv://jpl-recommendation-content-user:CH4XwwixACf7hOxb@pie-dev.7azsc.mongodb.net/pie-development")
        db = client["pie-development"]
        id_ = '62c25a0996b820ee4b9cbf12'
        col = db["headlines"] 
        check= col.find_one({'_id':ObjectId(id_)})
        language =str(check['languageId'])
        category= check['categoryIds']
        data = col.find({
            "$and" : [{
                        'categoryIds':category
                    }]        })
        headlines = DataFrame(data)
        headlines['languageId']=headlines['languageId'].astype('string')
        #create at last three days data
        headlines['createdAt'] = headlines['createdAt'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
        headlines['createdAt'] = headlines['createdAt'].astype('string')
        headlines1 = headlines[headlines['languageId']==language]
        p_dates=[]
        for i in range(1,4):
            Previous_Date = datetime.datetime.today() - datetime.timedelta(days=i)
            p_dates.append(Previous_Date.strftime('%Y-%m-%d'))
        final_data=headlines1[headlines1['createdAt'].isin(p_dates)]
    elif option=='summary':
        client = MongoClient("mongodb+srv://jpl-recommendation-content-user:CH4XwwixACf7hOxb@pie-dev.7azsc.mongodb.net/pie-development")
        db = client["pie-development"]
        id_ = '62c25a0996b820ee4b9cbf12'
        col = db["summaries"] 
        check= col.find_one({'_id':ObjectId(id_)})
        language =str(check['languageId'])
        category= check['categoryIds']
        data = col.find({
            "$and" : [{
                        'categoryIds':category
                    }]        })
        summary = DataFrame(data)
        summary['languageId']=summary['languageId'].astype('string')
        #create at last three days data
        summary['createdAt'] = summary['createdAt'].apply(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
        summary['createdAt'] = summary['createdAt'].astype('string')
        summary1 = summary[summary['languageId']==language]
        p_dates=[]
        for i in range(1,4):
            Previous_Date = datetime.datetime.today() - datetime.timedelta(days=i)
            p_dates.append(Previous_Date.strftime('%Y-%m-%d'))
        final_data=summary1[summary1['createdAt'].isin(p_dates)]
        
    lang_dictionary={"English":"ba118bf7fc9c1aedc1edb28a","Hindi":"9ddb12af8457d635ec15773f"}
    if language==lang_dictionary['English']:
        titles_list=final_data['title'].values.tolist()
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        new_list_embeddings = model.encode(titles_list)
        new_list_embeddings.shape
        f=cosine_similarity([new_list_embeddings[0]],new_list_embeddings[0:])
        final_data['similar']=f[0]
        return final_data[final_data['similar']>0.7]['title'].values.tolist()
    elif language==lang_dictionary['Hindi']:
        titles_list=final_data['title'].values.tolist()
        model = SentenceTransformer('hiiamsid/sentence_similarity_hindi')
        new_list_embeddings = model.encode(titles_list)
        new_list_embeddings.shape
        f=cosine_similarity([new_list_embeddings[0]],new_list_embeddings[0:])
        final_data['similar']=f[0]
        return final_data[final_data['similar']>0.7]['title'].values.tolist()
    else:
        return "Error: Not support Language"


