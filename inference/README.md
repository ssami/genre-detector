`cortex deploy`

Deploy wraps up all the information in the directory of cortex.yaml and deploys a 
cortex Docker container as a Python service. 

`cortex logs genre-detection`


`cortex get genre-detection`
 
Gives you info about the API. 

Sample Request: 

```
curl http://localhost:8888 -X POST -H "Content-Type: application/json" -d '{"data": "Sherlock Holmes was a very private man"}'
{"prediction": {"mystery___detective": 0.995183527469635, "thrillers": 0.00437257532030344, "crime": 0.00046282517723739147}}
```
