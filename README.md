# tasker

runs tasks per requests.
accepts the following types of requests:
1. sum2- sum 2 numbers
2. mult3- multiply 3 numbers
3. surprise- (get the result with get_requests_status query and see if you identify the song...)
4. get requests status per client
5. get processes status

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

troubleshoot and comments:
* client_name is mandatory is tasks queries, use it on order to get the related requests with get_requests_status query
* processes status can be active (ok), error (got internal error) or queue (failed to send/receive messages from sqs)
* 400 Bad Request: The browser (or proxy) sent a request that this server could not understand: add slash before quotes in json value (provided with -d param)

open issues:
* scalling (probably requires some more docker-related work)
* logs are not properly shared to runnig host
* indexes in db- index jobs by client_name/rid (depends on product requirements), job_events by rid and process_config by process name
* services dockerfiles are identical and differ from each other by env var. Need to be united to a single dockerfile that gets arg from docker-compose. 

additional thoughts:
* the design is simplified and meant to provide a solution to more complex tasks (sum 2 numbers does not really requires queues and multiservices :))
* future- add cache db in order to avoid processing (can be used in api stage, no need to send to queue)
* future- add more controlles for each service to share load (docker running configurations)
* future- add more available tasks
* future- connect to kibana
* future- create db builder script that updates sql ini file automatically with db_struct files




