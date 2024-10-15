# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
from Product import Product
import numpy as np
import pickle
from scipy.sparse import hstack
import pandas as pd


# 2. Create the app object
app = FastAPI()
pickle_in = open("model.pkl", "rb")
regressor = pickle.load(pickle_in)


# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}


# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Checkout Price Suggestor ': f'{name}'}


@app.post('/predict')
def predict(data: Product):
    data = data.dict()
    brands_label = data['brands_label']
    category_label = data['category_label']
    item_category_1 = data['item_category_1']
    item_category_2 = data['item_category_2']
    item_category_3 = data['item_category_3']
    item_category_4 = data['item_category_4']
    item_category_5 = data['item_category_5']
    shipping_by_buyer = data['shipping_by_buyer']
    shipping_by_seller = data['shipping_by_seller']
    main_category = data['main_category']
    sub_category_1 = data['sub_category_1']
    sub_category_2 = data['sub_category_2']

    name = data['name']
    item_description = data['item_description']
    name_vect , item_description_vect = dataProcessing(name,item_description)
    values = hstack([brands_label, category_label, item_category_1 , item_category_2 , item_category_3 , item_category_4 ,item_category_5,shipping_by_buyer,shipping_by_seller,main_category,sub_category_1,sub_category_2,name_vect,item_description_vect])
    prediction = regressor.predict(values)

    return {
        'prediction': prediction
    }

def dataProcessing(name , item_description):
    count_vectorizer = open("count_vect.pkl",'rb')
    count_vectorizer = pickle.load(count_vectorizer)
    name = count_vectorizer.transform([name])
    tfidf_vectorizer = open("tfidf_vect.pkl", 'rb')
    tfidf_vectorizer = pickle.load(tfidf_vectorizer)
    item_description = tfidf_vectorizer.transform([item_description])
    return name , item_description
# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

# uvicorn app:app --reload