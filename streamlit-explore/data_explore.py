import pandas as pd
import streamlit as st

DATA_LOCATION = '/Users/sumi/projects/kaggle-google-books/google-books-dataset/google_books_1299.csv'
GENRE_DATA_LOCATION = '/Users/sumi/gitrepos/genre-detector/training/split_genres.csv'

st.title('Genre data analyzer')


def load_raw_data(numrows):
    df = pd.read_csv(DATA_LOCATION, nrows=numrows)\
        .drop(['Unnamed: 0', 'voters', 'ISBN', 'language', 'published_date', 'publisher', 'price', 'currency'],
              axis=1)
    df = df.rename(columns={'generes': 'genres'})
    return df


def load_genre_split_data(genre_num):
    df = pd.read_csv(GENRE_DATA_LOCATION)
    return df[['title', 'author', 'rating', 'description', 'page_count', genre_num]]


data_load_state = st.text('Loading 1000 lines of data...')
data = load_raw_data(1000)
data_load_state.text('Loading data... done')

st.subheader('Filter by ratings')
ratings_select = st.slider('rating', 0.0, 5.0)
filtered_data = data[data['rating'] >= ratings_select]
st.write(filtered_data)

st.subheader('Filter by pages')
page_select = st.slider('pages', 0, 10000)
filtered_pages = data[data['page_count'] >= page_select]
st.write(filtered_pages)


st.subheader('Filter by genre_1')
data_genre_1 = load_genre_split_data('genre_1')
st.bar_chart(data_genre_1['genre_1'])
st.text('Forget the x-axis for now -- this shows us how prevalent and useless the "fiction" genre is')

st.subheader('Filter by genre_2')
data_genre_1 = load_genre_split_data('genre_2')
st.bar_chart(data_genre_1['genre_2'])
st.text('Much better, but clearly this data is skewed towards mystery, thriller, fantasy and sci-fi.')
st.text('...was this me in another life? ')

st.subheader('Filter by genre_3')
data_genre_1 = load_genre_split_data('genre_3')
st.bar_chart(data_genre_1['genre_3'])
st.text('Lot of nan, too granular.')

st.subheader('So let\'s try to predict by genre_2!')
