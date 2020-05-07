import pandas as pd
import streamlit as st

DATA_LOCATION = 'google_books_1299.csv'

st.title('Genre data analyzer')


def load_data(numrows):
    df = pd.read_csv(DATA_LOCATION, nrows=numrows)\
        .drop(['Unnamed: 0', 'voters', 'ISBN', 'language', 'published_date', 'publisher', 'price', 'currency'],
              axis=1)
    df = df.rename(columns={'generes': 'genres'})
    return df


data_load_state = st.text('Loading 1000 lines of data...')
data = load_data(1000)
data_load_state.text('Loading data... done')

st.subheader('Filter by ratings')
ratings_select = st.slider('rating', 0.0, 5.0)
filtered_data = data[data['rating'] >= ratings_select]
st.write(filtered_data)

st.subheader('Filter by pages')
page_select = st.slider('pages', 0, 10000)
filtered_pages = data[data['page_count'] >= page_select]
st.write(filtered_pages)