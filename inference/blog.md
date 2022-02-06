# Step 1: Docker container with FastAPI predictor

The simplest form of inferencing is just having a Python REST API that loads the model and serves it. 

For this case, we use FastAPI, which is a straightforward API without the bells and whistles of something larger like Django but is also more semantically intuitive compared to Flask. 

For now, the API loads the model on startup based on a simple setting/configuration, and the exposed prediction API allows a user to submit a chunk of text and ask to predict what genre it is.  


Options to run ML model through Docker containers: 
- Build an image with the model. This creates a one-to-one relationship between images and model versions, which has its advantages and disadvantages. One advantage is that the model and code and any settings are correlated precisely. But the major disadvantage is that larger models can create very large images, and if the code or settings haven't changed much, you can have a plethora of large, redundant images. 
- Use an .env file to specify where to download and load the model (e.g. from Minio, to approximate S3)in a Docker-compose set up  
- Use env in image to specify a project, and use something like MLFlow (or NeptuneML or something, still using Minio to approximate S3) to download the latest model for a project 
