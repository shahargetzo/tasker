# tasker

runs tasks per requests.
accepts 3 types of requests:
1. sum2- sum 2 numbers
2. mult3- muliply 3 numbers
3. surprise- (see if you identify the song...)

how to run:
1. cd to tasker dir
2. copy the cred file (if you have it ;)) to tasker/secret dir
3. run docker-compose up

supported requests:
1. docker-compose exec api curl -i -X GET -H "Accept: application/json" -H "Content-Type: application/json"  http://localhost:5000/get_processes_status
2. docker-compose exec api curl -i -X GET -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"client_name\":\"sh\"}' http://localhost:5000/get_requests_status
3. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"task\":\"mult3\", \"client_name\":\"sh\", \"params\": {\"first\":1, \"second\":2, \"third\":-1}}' http://localhost:5000/process
4. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"task\":\"sum2\", \"client_name\":\"sh\", \"params\": {\"first\":1, \"second\":2}}' http://localhost:5000/process
5. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"task\":\"surprise\", \"client_name\":\"sg\", \"params\": {\"first\":1}}' http://localhost:5000/process


