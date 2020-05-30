import fasttext as ft
import streamlit as st

model = ft.load_model('../training/genre_class_1590300901.bin')

st.title('Genre Predictor!')
user_input = st.text_input(label='Input the text whose genre you want to predict')
if user_input:
    pred_labels, confids = model.predict(user_input, k=5)
    label_prefix = "__label__"
    for label,confidence in zip(pred_labels, confids):
        l = label.split(label_prefix)[1]
        st.text(f"Label: {l}\t\tConfidence: {confidence}")




