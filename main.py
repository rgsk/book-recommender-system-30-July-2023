import pickle

from fastapi import FastAPI

popular_df = pickle.load(open('./model_exports/popular.pkl', 'rb'))


app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Server is running"}


@app.get("/popular-books")
def popular_books():
    # Convert DataFrame to list of dictionaries
    records = popular_df.to_dict(orient='records')
    return records
