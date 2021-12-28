#!/bin/bash
cron && tail -f /var/log/cron.log &
mosquitto -c /var/lib/mosquitto/mosquitto.conf &

# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?





