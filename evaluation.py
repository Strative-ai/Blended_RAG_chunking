import os
import re
from datetime import date
import pandas as pd
import json
from datetime import datetime
import requests
from pathlib import Path
import warnings
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import concurrent.futures

warnings.filterwarnings('ignore')

# Elasticsearch instance
# ES_CLOUD_ID = "cfe0bcaa729d4702bbd84e5becdb08f7:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGQxZDE0MTZkNzIzMjQ0YWZiNDY0ZGJkNjEwYTAwZTIzJGFmNzNjYThhZTEyZTQ3ODliYjEyZjdlNGQ4ODNlMjAz"
# ES_API_KEY = "VWo4cjY0OEIyYUpJZzFTa09DbzM6YUpVOHl2TE5SZW1DaXJKajZtVzdBdw=="
ES_CLOUD_ID="9ceb45cca61b4ab1abcb2dc0b6132e7f:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGUzNTZiMTk2NDJiMzRiMTg5NmQ4NTIxODAzY2M3NzNlJGU2MzQ0NzhkN2M5YTRmZWY4ZWM5OGYzNmE4NDM4MDVh"
ES_API_KEY="ZmtZY1VKQUJDdjUzXzZ2bzVMTUE6T0lHUHZnUWRUb3ExYzJpSDk2TTdiUQ=="

client = Elasticsearch(
cloud_id=ES_CLOUD_ID,
api_key=ES_API_KEY, timeout=30, max_retries=10, retry_on_timeout=True)

# Load dataset
sample_nq_path = "nq-train-sample-250.jsonl"
sample_nq_corpus = pd.read_json(sample_nq_path, lines=True)

k = 10

# Function to perform searches
def search_documents(ind):
    print (ind)

    question = sample_nq_corpus.iloc[ind]['question_text']
    
    with open('se_best.txt', 'r') as file:
        template_best = file.read().rstrip()
        search_query_best = template_best.replace("question", question)
        search_query_best = json.loads(search_query_best)

    with open('se_cross.txt', 'r') as file:
        template_cross = file.read().rstrip()
        search_query_cross = template_cross.replace("question", question)
        search_query_cross = json.loads(search_query_cross)

    with open('se_most.txt', 'r') as file:
        template_most = file.read().rstrip()
        search_query_most = template_most.replace("question", question)
        search_query_most = json.loads(search_query_most)

    with open('se_bool.txt', 'r') as file:
        template_bool = file.read().rstrip()
        search_query_bool = template_bool.replace("question", question)
        search_query_bool = json.loads(search_query_bool)


    es_index = "elser_simplified_splitrc_nq_train"

    response_best = client.search(
            index=es_index,
            size=k,
            query=search_query_best)
    # print(search_query_best)
    # if ind == 38:
    #     print(response_best)
    response_cross = client.search(
            index=es_index,
            size=k,
            query=search_query_cross)

    response_most = client.search(
            index=es_index,
            size=k,
            query=search_query_most)

    response_bool = client.search(
            index=es_index,
            size=k,
            query=search_query_bool)


    all_hits_best = response_best["hits"]["hits"]
    all_hits_cross = response_cross["hits"]["hits"]
    all_hits_most = response_most["hits"]["hits"]
    all_hits_bool = response_bool["hits"]["hits"]
    
    flag_best = False
    flag_cross = False
    flag_most = False
    flag_bool = False
    
    for doc in all_hits_best:
        if sample_nq_corpus.iloc[ind]['document_url'] == doc["_source"]["document_url"]:
            flag_best = True
            break

    for doc in all_hits_cross:
        if sample_nq_corpus.iloc[ind]['document_url'] == doc["_source"]["document_url"]:
            flag_cross = True
            break

    for doc in all_hits_most:
        if sample_nq_corpus.iloc[ind]['document_url'] == doc["_source"]["document_url"]:
            flag_most = True
            break

    for doc in all_hits_bool:
        if sample_nq_corpus.iloc[ind]['document_url'] == doc["_source"]["document_url"]:
            flag_bool = True
            break

    return flag_best, flag_cross, flag_most, flag_bool

def main():
    num_docs = len(sample_nq_corpus) #len(sample_nq_corpus)
    best_results = []
    cross_results = []
    most_results = []
    bool_results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(search_documents, range(100)))
    
    for i,result in enumerate(results):
        best_results.append(result[0])
        cross_results.append(result[1])
        most_results.append(result[2])
        bool_results.append(result[3])
        if result[0] != True:
            print(f'{i} {result}')
        
    accuracy_best = best_results.count(True)/len(best_results) * 100
    accuracy_cross = cross_results.count(True)/len(cross_results) * 100
    accuracy_most = most_results.count(True)/len(most_results) * 100
    accuracy_bool = bool_results.count(True)/len(bool_results) * 100


    # Save results to Excel
    data = {
        "Search Type": ["best", "cross", "most", "bool"],
        "Accuracy (%)": [accuracy_best, accuracy_cross, accuracy_most, accuracy_bool]
    }
    
    df = pd.DataFrame(data)
    # df.to_excel("search_accuracies.xlsx", index=False)
    # print("Results saved to search_accuracies.xlsx")
    print(data)

if __name__ == "__main__":
    main()