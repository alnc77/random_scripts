#!/usr/bin/python3
# Simple Python script to inject CEF to local port 514 or local syslog 

# Importing the libraries used in the script
import random
import syslog
import time
import os

# Simple list that contains usernames that will be randomly selected and then output to the "duser" CEF field.
usernames = ['Satya', 'Vanda', 'George' , 'xico']

# Simple list that contains authentication event outcomes that will be randomly selected and then output to the CEF "msg" field.
message = ['wanda is great ', 'wanda forever', 'wanda is wandarful']

# Endless loop that will run the below every five minutes.
while True:

# Assigning a random value from the above lists to the two variables that will be used to write to the Syslog file.

    selected_user = random.choice(usernames)
    selected_message = random.choice(message)

# Assigning a random integer value from 1-255 that will be appended to the IP addresses written to the Syslog file.
    ip = str(random.randint(1,255))
    ip2 = str(random.randint(1,255))

# The full Syslog message that will be written.   
    syslog_message = "CEF:0|bencatel system | bogus python Script local syslog |1.0|1000|CEF Authentication Event|10|src= 167.0.0.1|" + ip + " dst=10.0.0." + ip + " duser=" + selected_user + " msg=" + selected_message

# Writing the event to the Syslog file.

    syslog.openlog(facility=syslog.LOG_LOCAL7)
    syslog.syslog(syslog.LOG_NOTICE, syslog_message)

# inject to port 514
    os.system('logger -P 514 -p local4.warn -t CEF \'CEF:0|bencatel system | bogus python Script inject CEF |1.0|1000|CEF Authentication Event|10|src= 167.0.0.1|dst= 127.0.0.0|duser= Vanda|msg= \'' +selected_message)

# Pausing the loop for five seconds.
time.sleep(5)

# End of script