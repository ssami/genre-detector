# Stage 1: Simple Docker image and model

Get into the inference directory

`cd ../` 

Add the model binary into the base directory. 

`cp genre_model.bin base/`

Build the Docker image -- a simple FastAPI server that includes the model binary. 

```
cd base/
docker build -t base-infer -f Dockerfile .
```

Run the Docker image. 

`docker run -p 80:80 base-infer`





