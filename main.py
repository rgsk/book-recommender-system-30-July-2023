import pickle

import numpy as np
from fastapi import FastAPI
from pandas import DataFrame

popular_df: DataFrame = pickle.load(open('./model_exports/popular.pkl', 'rb'))
pt: DataFrame = pickle.load(open('./model_exports/pt.pkl', 'rb'))
books: DataFrame = pickle.load(open('./model_exports/books.pkl', 'rb'))
similarity_score: np.ndarray = pickle.load(
    open('./model_exports/similarity_score.pkl', 'rb'))


def recommend(book_name: str, number_of_recommendations: int):
    if len(np.where(pt.index == book_name)[0]) == 0:
        # book_name not found
        return []
    index = np.where(pt.index == book_name)[0][0]
    distances = similarity_score[index]
    similar_items = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[
        1:1 + number_of_recommendations]
    recommended_books = []
    for i in similar_items:
        books_with_title = books[books['Book-Title'] == pt.index[i[0]]]
        recommended_books.append({
            'book_name': books_with_title['Book-Title'].iloc[0],
            'author': books_with_title['Book-Author'].iloc[0],
            'image': books_with_title['Image-URL-M'].iloc[0],
        })
    return recommended_books


app = FastAPI()


@app.get("/")
def get_root():
    return {"message": 'Server is running visit "http://localhost:8000/docs" to test the api'}


@app.get('/book-names')
def get_book_names(offset: int = 0, limit: int = 100):
    total_count = len(books)
    names = books['Book-Title'].tolist()
    return {
        "total": total_count,
        "names": names[offset: offset + limit]
    }


@app.get("/popular-books")
def get_popular_books():
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


@app.get('/recommendations')
def get_recommendations(book_name: str, count: int = 5):
    return recommend(book_name, number_of_recommendations=count)
