import fasttext as ft
import streamlit as st


label_prefix = "__label__"

def get_label(raw_label_str, prefix):
    return raw_label_str.split(prefix)[1]


model = ft.load_model('/Users/sumi/gitrepos/genre-detector/inference/genre_class_1590302222.bin')

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
            st.success('Thank you for your feedback!')





