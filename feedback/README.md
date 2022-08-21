First, ensure Mongo is running on Docker: 
```
docker run --name some-mongo -d mongo:latest
```

Then bring up the feedback container: 
```
docker run -p 8080:8080 feedback
```

