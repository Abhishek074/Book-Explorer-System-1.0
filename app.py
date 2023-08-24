from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the data from pickle files
popular_df = pickle.load(
    open('C:\\Users\\ASUS\\Desktop\\Book Explorer system\\book-recommender-system-master\\popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].tolist(),
                           author=popular_df['Book-Author'].tolist(),
                           image=popular_df['Image-URL-M'].tolist(),
                           votes=popular_df['num_ratings'].tolist(),
                           rating=popular_df['avg_rating'].tolist()
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    # Handle the case when user_input is not found in pt.index
    if user_input not in pt.index:
        return render_template('recommend.html', data=[])

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:5]
    print('Hello')
    print(similar_items)
    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = [
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ]
        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
