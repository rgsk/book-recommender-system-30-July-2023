import pickle

popular_df = pickle.load(open('./model_exports/popular.pkl', 'rb'))

print(popular_df) 