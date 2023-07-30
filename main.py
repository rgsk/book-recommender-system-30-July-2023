import pickle

from fastapi import FastAPI
from pandas import DataFrame

popular_df: DataFrame = pickle.load(open('./model_exports/popular.pkl', 'rb'))


app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Server is running"}


@app.get("/popular-books")
def popular_books():
    # Convert DataFrame to list of dictionaries
    renamed_popular_df = popular_df.rename(columns={
        "Book-Title": 'book_name',
        "Book-Author": 'author',
        'Image-URL-M': "image",
        'num_ratings': 'votes',
        'avg_rating': 'rating'
    })
    records = renamed_popular_df.to_dict(orient='records')
    return records
