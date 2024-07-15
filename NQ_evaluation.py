import os
import re
from datetime import date
import pandas as pd
import json
from datetime import datetime
import requests

from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import warnings
warnings.filterwarnings('ignore')

# ## Replace elastic instance here
# es_client = Elasticsearch("https://esuser:espassword8@eshost:port",  ca_certs=False,
#                    verify_certs=False)
# es_client.info()

ES_CLOUD_ID="9ceb45cca61b4ab1abcb2dc0b6132e7f:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGUzNTZiMTk2NDJiMzRiMTg5NmQ4NTIxODAzY2M3NzNlJGU2MzQ0NzhkN2M5YTRmZWY4ZWM5OGYzNmE4NDM4MDVh"
ES_API_KEY="ZmtZY1VKQUJDdjUzXzZ2bzVMTUE6T0lHUHZnUWRUb3ExYzJpSDk2TTdiUQ=="

## Replace elastic instance here
# es_client = Elasticsearch("https://esuser:espassword8@eshost:port",  ca_certs=False, verify_certs=False)
es_client = Elasticsearch(
    cloud_id=ES_CLOUD_ID,
    api_key=ES_API_KEY,
)

print (es_client.info())

## Download model for KNN
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


## get the files from specific folder
def get_all_files(folder_name):
    # Change the directory
    os.chdir(folder_name)
    # iterate through all file
    file_path_list =[]
    for file in os.listdir():
        print(file)
        file_path = f"{folder_name}/{file}"
        file_path_list.append(file_path)
    return file_path_list


## Search in BM25 index and ELSER index
def processESIndex(df_questions,search_query,index_name):
    for ind in df_questions.index:
        print("Processsing -----",ind)
        question =df_questions['question'][ind]
        search_query["bool"]["should"][0]["text_expansion"]["document_text_embedding"]["model_text"] = question
        search_query["bool"]["must"]["multi_match"]["query"] = question
        response = es_client.search(
        index=index_name,
        body=search_query,
        scroll='5m',  # Set the scroll timeout (e.g., 5 minutes)
        size=10  # Set the number of documents to retrieve per scroll
        )
        all_hits = response['hits']['hits']
        print(len(all_hits))
        flag = False
        for num, doc in enumerate(all_hits):
            if df_questions['answers'][ind] in  doc["_source"]['document_text']:
               # print("helooo",doc["_source"]['content_para'])
                #print ("DOC ID:", doc["_id"], "--->", doc, type(doc), "\n")
                flag = True
                break
        print ("DOC Score:", flag)
        df_questions['model_op1'][ind] = flag
            
    return df_questions


## search in KNN index
def processESIndex_Knn(df_questions,search_query,index_name):
    i =0
    count =0
    for ind in df_questions.index:
        print("Processsing -----",ind)
        question =df_questions['text'][ind]
        content_embedding =model.encode(question)
        ## content_embedding will be add into your query according the question
        response = es_client.search(
        index=index_name,
        body=search_query,
        scroll='5m',  # Set the scroll timeout (e.g., 5 minutes)
        size=10  # Set the number of documents to retrieve per scroll
        )
        all_hits = response['hits']['hits']
        print(len(all_hits))
        flag = False
        for num, doc in enumerate(all_hits):
            if df_questions['answers'][ind] in  doc["_source"]['document_text']:
                flag = True
                break
        print ("DOC Score:", flag)
        df_questions['model_op_kNN'][ind] = flag
    return df_questions


## Read the file
search_query=""
with open('./search_query/BM25/bm25_best.txt', 'r') as file:
    search_query = file.read().rstrip()

## If you need to replace any file or  other query basis of Your index you can use the respective folders
index_name ="knn_simplified_nq_train"
df_questions =pd.read_json("./NQ-open.dev.jsonl", lines=True)

## BM25 and ELSER
processESIndex(df_questions,search_query,index_name)

## KNN
# processESIndex_Knn(df_questions,search_query,index_name)
