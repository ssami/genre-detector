#!/bin/bash

# Builds Docker image after some modifications to current directory

# copy the shared Python library into the inference image
cp -r ../../../lib .

# copy the model into Docker context to build it into the inference image
cp ../../genre_class_1590302222.bin .

# build the image
docker build -t base-infer -f Dockerfile --env-file ./.env .

# cleanup
rm -rf lib/
rm genre_class_1590302222.bin
