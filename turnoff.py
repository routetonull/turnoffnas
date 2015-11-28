#!/usr/bin/python
'''
last change: 20151128
test if nas server is in use
for auto shutdown at night
'''

import commands
import httplib, urllib

def sendPush(messageText):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	urllib.urlencode({
		"token": "INSERT TOKEN HERE",
		"user": "INSERT USER HERE",
		"message": messageText,
	}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

tests = (
'netstat -an | grep 10\.99\.0\.11',
'ps aux | grep -v grep | grep aria2c',
'netstat -an | grep 10\.99\.0\.10:22.*ESTABLISHED',
'ping 10.99.0.11 -c 2 -n',
'ps aux | grep -v grep | grep axel'
,'ssh root@10.99.0.19 esxcli vm process list | grep Display\ Name | grep -v NAS',
)

'''
TESTS
	active sessions to media center
	aria2c is active
	active ssh sessions to LAN addresses
	media center is alive - redundant to test 1 - keep it
	axel is active
	VMs other than NAS are active
'''	

r=0

for t in tests:
	c = commands.getstatusoutput(t)
	#print c
	if not c[0]:
		r+=1

if not r:		
	
	# if nas unused notify pushbullet and turn off ESXi host and NAS
	
	#send message
	
	m = 'NAS not in use, turning it OFF'
	sendPush(m)
	
	# now turn off
	
	#sometimes first ESXi halt doesn't work, run two to be sure
	turnOffCommands='date'
	#turnOffCommands=turnOffCommands=('ssh root@10.99.0.19 halt','ssh root@10.99.0.19 halt','halt')
	for c in turnOffCommands:
		c = commands.getstatusoutput(c)
