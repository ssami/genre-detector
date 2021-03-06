import pandas as pd
import requests
import re
import random
import fasttext
from sklearn.utils import resample
from datetime import datetime as dt


def download_feedback_data(model_id):
    """
    Get data from the feedback module per model ID
    and return it in a format that can be used directly in training data.
    TODO: in the future we should check the minimum length of a feedback text,
    and whether it exists in the training or test data.
    """
    feedback = requests.get(f'http://127.0.0.1:8000/feedback/{model_id}').json()
    fb_list = []
    for f in feedback:
        fb_dict = dict()
        fb_dict['description'] = f['text']
        fb_dict['genre'] = '__label__' + f['label']
        fb_list.append(fb_dict)

    df = pd.DataFrame(fb_list)
    return df


def cleanup(df):
    # clean up columns, save only what we need
    df = df.drop(['Unnamed: 0', 'voters', 'ISBN', 'language', 'published_date', 'publisher', 'price', 'currency'],
              axis=1)
    df = df.rename(columns={'generes': 'genres'})
    # use only those entries with genres
    total_length = len(df)
    genre_df = df[df['genres'] != 'none']
    genre_rows = len(genre_df)
    print(f'Total length is {total_length} but genre rows are {genre_rows}')
    return genre_df


def split_genres(df):
    df[['genre_1', 'genre_2', 'genre_3', 'genre_4']] = df.genres.str.split(' , ', expand=True)
    df = df.drop(['genres'], axis=1)
    return df


def genre_choose(df_split):
    """
    # We could try a couple things here:
     we can first assume that genre_1 is the closest genre
     to what's really going on.
     Then we'll see how many unique values are here,
     because lots of things are marked "fiction".
     This was a great place to try streamlit.
    :return:
    """
    genre_split = split_genres(df_split)
    genre_2_split = genre_split.drop(['genre_1', 'genre_3', 'genre_4'], axis=1).rename(columns={'genre_2': 'genre'})

    return genre_2_split


def aggressively_clean_text(t):
    t = t.lower()
    t = re.sub(r"\W", ' ', t)
    return t


def aggressively_clean_label(t):
    t = re.sub(r"&amp,", '&', t)
    t = re.sub(r"[\( | \) | \&]", ' ', t)
    t = re.sub(r"\s", '_', t)

    t = t.lower()
    t = '__label__' + t
    return t


def printout_predictions(model, df):
    test_non_df = pd.read_csv('none_genres.csv')
    # pick some random indexes
    randoms = []
    for _ in range(5):
        randoms.append(random.randint(0, len(test_non_df)))

    for i in range(len(test_non_df)):
        test_descr = df.iloc[i]['description']
        cleaned_test = aggressively_clean_text(test_descr)
        prediction = model.predict(cleaned_test)
        print(f"{i}: {cleaned_test[:100]}, prediction: {prediction}")


def train(csv_file):
    df = pd.read_csv('/Users/sumi/projects/kaggle-google-books/google-books-dataset/google_books_1299.csv')
    genre_df = cleanup(df)
    gen_df = genre_choose(genre_df)

    gen_df['genre'].unique()

    # # Now it's training time, just with the description

    relevant_cols = ['description']
    label_col = 'genre'
    genre_labels = gen_df[label_col].apply(aggressively_clean_label)
    cleaned_descr = gen_df['description'].apply(aggressively_clean_text)

    # now contains the genres and the labels
    cleaned_full_df = pd.DataFrame.merge(gen_df, genre_labels, left_index=True, right_index=True)

    # now contains the genre columns, the labels and the descriptions
    cleaned_df = pd.DataFrame.merge(cleaned_full_df, cleaned_descr, left_index=True, right_index=True)

    # removing additional index
    cleaned_df = cleaned_df.drop(['genre_x', 'description_x'], axis=1).rename(columns={'description_y': 'description', 'genre_y': 'genre'})

    # removing unnecessary columns
    data_labels = cleaned_df[label_col] + ' ' + cleaned_df[relevant_cols]

    # only keep those genres that have >10 samples
    counts = cleaned_df['genre'].value_counts()
    for label, count in counts.items():
        if count >= 10:
            cleaned_df = cleaned_df[cleaned_df['genre'] == label]

    cleaned_df['genre'].value_counts()

    # Upsample anything that has less than 100 samples
    upsampled_dfs = []
    cutoff_counts = cleaned_df['genre'].value_counts().to_dict()
    for label, count in cutoff_counts.items():
        if count < 100:
            df_ = resample(cleaned_df[cleaned_df['genre'] == label],
                            replace=True,
                            n_samples=100,
                            random_state=123
                          )
            upsampled_dfs.append(df_)
    sample_concat_samples = pd.concat(upsampled_dfs)
    # shuffle, reset the index, and drop the new index
    final_training_df = sample_concat_samples.sample(frac=1).reset_index(drop=True)
    train_percentage = 0.8
    test_percentage = 1.0 - train_percentage

    # Make train/test split
    train_ = final_training_df.sample(frac=train_percentage)
    test_ = (final_training_df - train_).sample(frac=test_percentage).to_csv('test_genre.txt', header=False, index=False)
    # train
    train_.to_csv('train_genre.txt', header=False, index=False)
    # test
    test_.to_csv('test_genre.txt', header=False, index=False)

    # train and auto-tune
    model = fasttext.train_supervised('train_genre.txt', autotuneValidationFile='test_genre.txt')
    for i in range(4):
        samples, precision, recall = model.test('test_genre.txt', k=i+1)
        f1_score = 2*precision*recall/(precision+recall)
        print(f"Top n: {i+1} Samples: {samples} Precision: {precision} Recall: {recall} F1: {f1_score}")

    printout_predictions(model, final_training_df)

    timestamp = dt.now().strftime('%s')
    model_name = 'genre_class_' + timestamp + '.bin'
    model.save_model(model_name)
