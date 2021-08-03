# tasker

This exercise is meant to demonstrate a simple (and somehow naive) design. Please feel free to leave comments and ask anything :)

runs tasks per requests.
accepts the following types of requests:
1. sum2- sum 2 numbers
2. mult3- multiply 3 numbers
3. surprise- (get the result with get_requests_status query and see if you identify the song...)
4. get requests status per client
5. get processes status
6. set processes status

how to run:
1. clone the project
2. cd to tasker dir
3. create dir named secret in tasker and copy the cred file (if you have it ;)) to tasker/secret dir
4. run docker-compose up

supported requests- cd to tasker dir and run: 

1. docker-compose exec api curl -i -X GET -H "Accept: application/json" -H "Content-Type: application/json"  http://localhost:5000/get_processes_status
2. docker-compose exec api curl -i -X GET -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"client_name\":\"sh\"}' http://localhost:5000/get_requests_status
3. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"task\":\"mult3\", \"client_name\":\"sh\", \"params\": {\"first\":1, \"second\":2, \"third\":-1}}' http://localhost:5000/process
4. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"task\":\"sum2\", \"client_name\":\"sh\", \"params\": {\"first\":1, \"second\":2}}' http://localhost:5000/process
5. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"task\":\"surprise\", \"client_name\":\"sg\", \"params\": {\"first\":1}}' http://localhost:5000/process
6. docker-compose exec api curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" -d '{\"mult3\":\"suspended\"}' http://localhost:5000/set_processes_status


design:
* simple controller-handler design, using sqs and centered db to execute tasks and monitor tasks status and system behaviour.
* unit tests included, cover only a minor part of the code
* when an image is built, a simple validator runs to make sure database_struct files match the init.sql file (in terms of existing keys).


troubleshoot and comments:
* client_name is mandatory is tasks queries, use it on order to get the related requests with get_requests_status query
* processes status can be active (ok), error (got internal error), queue (failed to send/receive messages from sqs) or suspended (inserted only by client in set_processes_status request)
* 400 Bad Request: The browser (or proxy) sent a request that this server could not understand: add slash before quotes in json value (provided with -d param)
* when a request is properly calculated, it's inserted to cache table. primary key- task_name + task_params. an answer will be taken from cache (if exists) in api stage and won't be sent to tasker queue. example for cached request response for methis "process": {"cached":true,"rid":"ec0fded4ca0047c2a0bf04491c0f1ec8","success":true}.

open issues:
* scaling (probably requires some more docker-related work)
* logs are not properly shared to running host
* get_requests_status method should use client_name index

additional thoughts:
* the design is simplified and meant to provide a solution to more complex tasks (sum 2 numbers does not really requires queues and multiservices :))
* future- add more controllers for each service to share load (docker running configurations)
* future- add images that can perform multiple tasks and are able to listen to specific queues upon request.
* future- add more available tasks
* future- connect to kibana





