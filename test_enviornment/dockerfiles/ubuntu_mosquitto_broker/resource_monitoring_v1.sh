#!/bin/bash
SERVICE="mosquitto"
while true ; do
    mosquitto_cpu_usage=$(top -b -n 1 | grep mosquitto | awk '{print $9}')		
    int_cpu=${mosquitto_cpu_usage%%.*}
    if [ "$int_cpu" -gt 90 ]
        then
            echo "Borker uses to much CPU killing process"
            pkill $SERVICE
        else
            echo "current cpu usage $int_cpu" 
    fi
done

