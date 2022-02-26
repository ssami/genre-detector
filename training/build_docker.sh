#!/usr/bin/env bash

cp -r ../lib .

cp /Users/sumi/projects/kaggle-google-books/google-books-dataset/google_books_1299.csv raw.csv

docker build -t train -f Dockerfile .

rm -rf ./lib

rm raw.csv
