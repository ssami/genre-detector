# genre-detector
Using Kaggle data from Google books to detect genre of some text. 

# Project structure

This repo is divided into 3 parts: `streamlit-explore`, `training` and `inference`.

## Streamlit explore

`streamlit-explore` uses the very cool Streamlit library to both explore the dataset, as well as load and explore the model ultimately trained from the data. Enjoyed is a strong word for how I feel about using front-end React/Javascript (though I learned a lot) so having something like Streamlit to do the heavy lifting while I refine the model is amazing. 

Other things I want to do: 
1. Training models with different parameters and seeing how they do with inputs. 
2. Collecting feedback from users who give input and can correct the labels. It would be great to build in a feedback loop. 

   
## Training 

Here is where all the ugly training work happens. I'm not a researcher by trade, but I know my way roughly around fastText and Pandas. I chose fastText because I've worked with it before and I wanted a pretty good classification model focused on text. 

Other things I want to do: 
1. Monitoring the model performance; have an option to build a bad model and have it go through CI/CD and see how it messes up the inference metrics 
1. doc2vec and calculate document cosine similarity so I finally gain enough experience working with it. 
1. Clustering -- how does that work/help here and how accurate would that be? Would be fun to work on unsupervised learning. 


## Inference (Code WIP)

Building a simple inference pipeline isn't necessarily challenging, but hosting the prediction service securely can be. Now you're looking at things like re-deployment with updated models and/or updated code, exposing APIs securely, logging, and figuring out model performance in production.  

Built with Cortex, to get a feel for an inference engine. Not convinced any project needs an engine off the bat... 

## Feedback (Code WIP)

Building a feedback service to store feedback objects into a SQL DB so that they can be added to the training data set. 
Can be started from this parent directory by doing: 
` uvicorn feedback.feedback:app`
