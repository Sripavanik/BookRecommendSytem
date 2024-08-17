from flask import Flask,render_template,request
import numpy as np
import pickle
import pandas.core.indexes.numeric

with open('popular.pkl', 'rb') as file:
    popular_df = pickle.load(file)
with open('pt.pkl', 'rb') as file:
    pt = pickle.load(file)
with open('books.pkl', 'rb') as file:
    books = pickle.load(file)
with open('similarity_scores.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                          votes=list(popular_df['num-ratings'].values),
                           rating=list(popular_df['avg-ratings'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index=np.where(pt.index==user_input)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
    data=[]
    for i in similar_items:
        item=[]
        print(pt.index[i[0]])
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author']))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M']))
        data.append(item)
    return render_template('recommend.html',data=data)
if __name__=='__main__':
    app.run(debug=True)