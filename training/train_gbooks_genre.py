# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# open up the data and display
import pandas as pd
import re
import random
import requests


def download_feedback_data(model_id): 
    """
    Get data from the feedback module per model ID
    and return it in a format that can be used directly in training data. 
    TODO: in the future we should check the minimum length of a feedback text, 
    and whether it exists in the training or test data. 
    """
    feedback = requests.get(f'http://127.0.0.1/feedback/').json()
    fb_list = []
    for f in feedback: 
        fb_dict = dict()
        fb_dict['description'] = aggressively_clean_text(f['text'])
        fb_dict['genre'] = '__label__' + f['label']
        fb_list.append(fb_dict)

    df = pd.DataFrame(fb_list)
    return df


feedback_df = download_feedback_data(None)
print(feedback_df)

df = pd.read_csv('/Users/sumi/projects/kaggle-google-books/google-books-dataset/google_books_1299.csv')
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


genre_df = cleanup(df)
genre_df.head()


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


gen_df = genre_choose(genre_df)
gen_df.head()

# ### Now we'll have to do some cleanup and sample correctly

gen_df['genre'].unique()

# # Now it's training time, just with the description

relevant_cols = ['description']
label_col = 'genre'


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


genre_labels = gen_df[label_col].apply(aggressively_clean_label)
cleaned_descr = gen_df['description'].apply(aggressively_clean_text)
cleaned_descr.head()

genre_labels.head()

cleaned_full_df = pd.DataFrame.merge(gen_df, genre_labels, left_index=True, right_index=True)
cleaned_full_df.head()

cleaned_df = pd.DataFrame.merge(cleaned_full_df, cleaned_descr, left_index=True, right_index=True)
cleaned_df.head()

cleaned_df = cleaned_df.drop(['genre_x', 'description_x'], axis=1).rename(columns={'description_y': 'description', 'genre_y': 'genre'})
cleaned_df.head()

final_df = pd.concat([cleaned_df, feedback_df], ignore_index=True)
print(final_df)

data_labels = cleaned_df['genre'] + ' ' + cleaned_df['description']
train_percentage = 0.8
test_percentage = 1.0 - train_percentage

# ## Make train/test split

train_data = data_labels.sample(frac=train_percentage).to_csv('train_genre.txt', header=False, index=False)
test_df = data_labels.sample(frac=test_percentage).to_csv('test_genre.txt', header=False, index=False)

# # Train fasttext model

import fasttext
model = fasttext.train_supervised('train_genre.txt')
for i in range(4): 
    samples, precision, recall = model.test('test_genre.txt', k=i+1)
    f1_score = 2*precision*recall/(precision+recall)
    print(f"Top n: {i+1} Samples: {samples} Precision: {precision} Recall: {recall} F1: {f1_score}")

test_none_df = df[df['genres'] == 'none']
test_none_df.to_csv('none_genres.csv')

test_descr = test_none_df.iloc[0]['description']
cleaned_test = aggressively_clean_text(test_descr)
model.predict(cleaned_test)

test_descr = test_none_df.iloc[500]['description']
cleaned_test = aggressively_clean_text(test_descr)
print(cleaned_test)
model.predict(cleaned_test)

# ### Well, so far everything is being recognized as "fantasy".  Let's try more rigorous training. 

model = fasttext.train_supervised('train_genre.txt', epoch=25, lr=0.1)
for i in range(4): 
    samples, precision, recall = model.test('test_genre.txt', k=i+1)
    f1_score = 2*precision*recall/(precision+recall)
    print(f"Top n: {i+1} Samples: {samples} Precision: {precision} Recall: {recall} F1: {f1_score}")

# This is exactly as bad, so we really do have to do some downsampling on fantasy and sci-fi. Let's look at the breakdown. 

counts = cleaned_df['genre'].value_counts()
pd.set_option('display.max_rows', 500)

print(counts)

# Clearly a number of these could be combined, but we're not going to bother predicting the much smaller datasets. Instead, we'll cut off those that have < 10 samples. 
# And anything that's > 50 samples, we'll downsample. 
# In fact, there's a scikit package that does upsampling and downsampling!

count_dict = counts.to_dict()

for label, count in count_dict.items():
    if count < 10:
        cleaned_df = cleaned_df[cleaned_df['genre'] != label] 

cleaned_df['genre'].value_counts()

# # Now for the re-sampling

# +
from sklearn.utils import resample

# let's try a resampling of smaller data first
df_classics = cleaned_df[cleaned_df['genre'] == '__label__classics']
df_classics.head()
# -

df_classics_sampled = resample(df_classics, 
                              replace=True,
                              n_samples=100, 
                              random_state=123)
len(df_classics_sampled)

# Now let's do the same for all the low-sample counts
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

upsampled_dfs[-1].head()

for label, count in cutoff_counts.items(): 
    if count >= 100: 
        big_sample = cleaned_df[cleaned_df['genre'] == label]
        upsampled_dfs.append(big_sample)
print(len(upsampled_dfs))
sample_concat_samples = pd.concat(upsampled_dfs)

len(sample_concat_samples)

# shuffle, reset the index, and drop the new index
final_training_df = sample_concat_samples.sample(frac=1).reset_index(drop=True)
final_training_df.head()

# Just checking that the samples are pretty evenly distributed. 

hist_df = final_training_df.copy()
value_counts = cleaned_df['genre'].value_counts()
genre_map = dict()
i = 0
for index,value in value_counts.items(): 
    genre_map[index] = i
    i += 1
print(genre_map)
hist_df['genre_map'] = hist_df['genre'].apply(lambda x: genre_map[x])
hist_df.hist(column='genre_map', bins=len(genre_map))

# # Part 3, Add feedback 

fb_df = download_feedback_data('1590302222')
train_df = final_training_df[['genre', 'description']]
final_df = pd.concat([fb_df, train_df], ignore_index=True)

final_df.head()

# # Part 2, Make Train Test Split

data_labels = final_df['genre'] + '\t' + final_df['description']
train_percentage = 0.8
test_percentage = 1.0 - train_percentage
train_data = data_labels.sample(frac=train_percentage).to_csv('train_genre.txt', header=False, index=False)
test_df = data_labels.sample(frac=test_percentage).to_csv('test_genre.txt', header=False, index=False)

# # Part 3, Train Model and Test: this time with some hyperparameter tuning

# +
import fasttext

model = fasttext.train_supervised('train_genre.txt')
for i in range(4): 
    samples, precision, recall = model.test('test_genre.txt', k=i+1)
    f1_score = 2*precision*recall/(precision+recall)
    print(f"Top n: {i+1} Samples: {samples} Precision: {precision} Recall: {recall} F1: {f1_score}")


# -

# Now let's do a random prediction of a number of inputs

def printout_predictions(model): 
    test_non_df = pd.read_csv('none_genres.csv')
    # pick some random indexes
    randoms = []
    for _ in range(5): 
        randoms.append(random.randint(0, len(test_non_df)))

    for i in range(len(test_non_df)):     
        test_descr = test_none_df.iloc[i]['description']
        cleaned_test = aggressively_clean_text(test_descr)
        prediction = model.predict(cleaned_test)
        print(f"{i}: {cleaned_test[:100]}, prediction: {prediction}")


# ## Let's go one step further and use fastText's auto hyperparameter tuning with the test file

# +
import fasttext

model = fasttext.train_supervised('train_genre.txt', autotuneValidationFile='test_genre.txt')
for i in range(4): 
    samples, precision, recall = model.test('test_genre.txt', k=i+1)
    f1_score = 2*precision*recall/(precision+recall)
    print(f"Top n: {i+1} Samples: {samples} Precision: {precision} Recall: {recall} F1: {f1_score}")
# -

printout_predictions(model)

# ### This is like... orders of magnitude awesomely better. 

# Let's save this model so that we can use it later! We'll give it a descriptive name. 

from datetime import datetime as dt
timestamp = dt.now().strftime('%s')
model_name = 'genre_class_' + timestamp + '.bin'
model.save_model(model_name)

# But what was this model actually trained with? 'dump' exists as an option for fasttext as a command line option, but what about Python? 

# Other features we could train with: 
# - the title 
# - the author 
# - publisher

pred_labels, confids = model.predict("woot woot thriller", k=5)

zip(pred_labels, confids)

for label,confidence in zip(pred_labels, confids): 
    print(f"Label: {label}, confidence: {confidence}")

model_ = fasttext.load_model('genre_class_1590302222.bin')

model_.predict('help')

print(confids)

print(list(pred_labels))


