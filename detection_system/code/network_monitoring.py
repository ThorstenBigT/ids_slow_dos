"""This module send monitors the network activity by constnatly querying the database.
    Author: Thorsten Steuer
    Licence: Apache 2.0
"""
#from statistics import median, mean, stdev
import time
import threading
import sys

from alarm_notification import AlarmNotification
from neo4j_database_access import Neo4jDatabaseAccess

class NetworkMonitoring:

    def __init__(self, uri: str, user: str, password: str) -> None:
        self.neo4j_driver = Neo4jDatabaseAccess(uri, user, password)
        self.email_notification = AlarmNotification()
        self.monitoring_status = True

    def _start(self):

        while self.monitoring_status is True:

            # Was used for perfromance test
            #all_execution_times = []
            #for i in range(0, 100):

            start_time = time.time() * 1000
            query = (
                    'MATCH (h:Host)-[r:STARTS_CONNECTION]->(c:Connection) '
                    'WHERE c.status = "active" AND h.notification_sent = "False" AND h.is_blocked = "False"'
                    'RETURN h,count(r) as count'
                    )
            result = self.neo4j_driver.execute_and_return_query_result(query)

            # Was used for perfromance test
            #end_time = time.time() * 1000
            #execution_time = end_time - start_time
            #all_execution_times.append(execution_time)
            #i=i+1
            
            if result is not None:
                message = ""
                for row in result:
                    if row['count'] > 50:
                        
                        message = 'Host ' + row['h']['ip_address'] + ' has ' +  str(row['count']) + ' active connections'
                        self.neo4j_driver.update_and_return_host_block(row['h']['ip_address'], "True")

                        self.email_notification.connect_to_smtp_server()
                        self.email_notification.send_email(message)
                        self.email_notification.stop_smtp()
                        self.neo4j_driver.update_and_return_host_notification_sent(row['h']['ip_address'], "True")
                        message = ""
                        
                        # Was used for perfromance test
                        #end_time = time.time() * 1000
                        #execution_time = end_time - start_time
                        #all_execution_times.append(execution_time)
                        #i=i+1
                
            # Was used for perfromance test   
            #all_execution_times = list(filter(lambda num: num != 0.0, all_execution_times))
            #print(all_execution_times)
            #print(median(all_execution_times))
            #print(mean(all_execution_times))
            #print(stdev(all_execution_times))
            #time.sleep(1)

        if self.monitoring_status is False:
            sys.exit()

    def start(self):
        threading.Thread(target=self._start, daemon=True).start()

    def stop(self):
        self.monitoring_status = False

if __name__ == "__main__":
    NEO4J_URI = 'bolt://localhost:30687'
    NEO4J_USER = 'neo4j'
    NEO4J_PASS = '1234'
    network_monitoring = NetworkMonitoring(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    network_monitoring._start()
