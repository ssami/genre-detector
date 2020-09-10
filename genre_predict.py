import fasttext as ft
import streamlit as st
import requests


label_prefix = "__label__"
model_id = '1590302222'
model_path = '/Users/sumi/gitrepos/genre-detector/inference/genre_class_1590302222.bin'
feedback_api = 'http://127.0.0.1:8000/feedback/'


def get_label(raw_label_str, prefix):
    return raw_label_str.split(prefix)[1]


def submit_feedback(model_id, text, label):
    body = {
        'model_id': model_id,
        'text': text,
        'label': label
    }
    resp = requests.post(url=feedback_api, json=body)
    return resp


model = ft.load_model(model_path)

st.title('Genre Predictor!')
user_input = st.text_input(label='Input the text whose genre you want to predict')
if user_input:
    pred_labels, confids = model.predict(user_input, k=5)

    for label,confidence in zip(pred_labels, confids):
        l = get_label(label, label_prefix)
        st.text(f"Label: {l}\t\tConfidence: {confidence}")

    # now ask for feedback
    labels = [get_label(l, label_prefix) for l in model.labels]
    st.title('Feedback')
    feedback_genre = st.radio('Which of the following labels best describes the text above?', options=labels)
    b = st.button('Submit feedback')

    if feedback_genre:
        st.text(f'You selected {feedback_genre}')
        if b:
            resp = submit_feedback(model_id, user_input, feedback_genre)
            if resp.status_code == 200:
                st.success('Thank you for your feedback!')
            else:
                st.error(f'Something went wrong while submitting feedback...{resp.json()}')




