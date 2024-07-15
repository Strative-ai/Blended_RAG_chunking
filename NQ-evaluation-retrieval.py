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
# import ray
import argparse

warnings.filterwarnings('ignore')

# Elasticsearch instance
# ES_CLOUD_ID = "cfe0bcaa729d4702bbd84e5becdb08f7:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGQxZDE0MTZkNzIzMjQ0YWZiNDY0ZGJkNjEwYTAwZTIzJGFmNzNjYThhZTEyZTQ3ODliYjEyZjdlNGQ4ODNlMjAz"
# ES_API_KEY = "VWo4cjY0OEIyYUpJZzFTa09DbzM6YUpVOHl2TE5SZW1DaXJKajZtVzdBdw=="
ES_CLOUD_ID="9ceb45cca61b4ab1abcb2dc0b6132e7f:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJGUzNTZiMTk2NDJiMzRiMTg5NmQ4NTIxODAzY2M3NzNlJGU2MzQ0NzhkN2M5YTRmZWY4ZWM5OGYzNmE4NDM4MDVh"
ES_API_KEY="ZmtZY1VKQUJDdjUzXzZ2bzVMTUE6T0lHUHZnUWRUb3ExYzJpSDk2TTdiUQ=="

client = Elasticsearch(
cloud_id=ES_CLOUD_ID,
api_key=ES_API_KEY, timeout=30, max_retries=10, retry_on_timeout=True)

def create_query(question, template):
    query = template.copy()
    query["bool"]["should"][0]["text_expansion"]["document_text_embedding"]["model_text"] = question
    query["bool"]["must"]["multi_match"]["query"] = question
    return query

# Function to perform searches
# @ray.remote(num_cpus=1)
def search_documents(batch, template):
    query = map(lambda x: create_query(x, template), batch["question_text"])
    query = list(query)
    return True


def main(data_path, batch_size, k, template_path):
    with open(template_path, "r") as f:
        template = f.read()
    template = json.loads(template)
    data = pd.read_json(data_path)
    executions = []
    for batch in data.iter_batches(batch_size=batch_size):
        exec_future = search_documents.remote(batch, template)
        executions.append(exec_future)
    ray.get(executions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--data-path", type=str, default="./nq-train-sample-250.jsonl")
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--template-path", type=str, default="./search_query/BM25/bm25_best.txt")
    args = parser.parse_args()
    main(args.data_path, args.batch_size, args.k, args.template_path)
