#!/bin/sh
echo starting "$SERVICE_DIR"
rm nohup.out
nohup python3 /home/tasker/task_runners/services/"$SERVICE_DIR"/start.py > nohup.out 2>&1 &
sleep 0.1
tail -f nohup.out