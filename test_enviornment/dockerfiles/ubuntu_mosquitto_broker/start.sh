#!/bin/bash
mosquitto -c /var/lib/mosquitto/mosquitto.conf
SERVICE="mosquitto"
while [ true ]; do
    sleep 1
    mosquitto_cpu_usage=`top -b -n 1 -d 0.2 | grep mosquitto | awk '{print $9}'`
    int_cpu=${mosquitto_cpu_usage%%.*}
    if [ $int_cpu -gt 90 ]
        then
            echo "Borker uses to much CPU killing process"
            pkill $SERVICE
    fi
done

