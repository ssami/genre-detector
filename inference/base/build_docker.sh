#!/bin/bash

# Builds Docker image after some modifications to current directory

# copy the shared Python library into the inference image
cp -r ../../lib ./app/

# copy the model into the current context
cp ../genre_class_1590302222.bin ./model.bin

# build the image
docker build -t base-infer -f Dockerfile .

# cleanup
rm -rf lib/
