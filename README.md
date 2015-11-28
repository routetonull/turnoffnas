# turnoffnas

##Scenario
I run a NAS server VM on an ESXi host. 
The NAS is mostly used to store data, download files from internet and stream videos to a media center connected via LAN.
I don't need it to be powered on 24x7 so it can be turned off a night under some conditions.

##Script

###Conditions:
- no active ssh sessions from LAN
- no downloads runnint (aria2c, axel etc)
- no active media streaming (udp/tcp sessions to media center)
- no VMs active on ESXi host other than NAS (sometimes I run some lab servers that should be active 27x4) 

###Actions:
- connect to ESXi host and run halt command
- stop the VM itself with halt command

###Notifications
PushOver notification included to track when the NAS is turnet off.

###Schedule

The script is scheduled to run from 23 every 10 minutes until the morning.

*/10 0,1,2,3,4,5,6,7,23 * * * /root/turnoff.py
