#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from comuniopy import Comunio
import time

test = Comunio('','','BBVA') # set username and password
test.login()
#test.load_info()

print "ID: %s"%test.getID()
print "Money: %s"%test.getMoney()
print "TeamValue: %s"%test.getTeamvalue()
print "Title: %s"%test.getTitle()

print '[*] Clasificacion:'

time.sleep(1)
for i in test.standings():
    print i
    
time.sleep(1)



print '[*] Info_player test:\n'
time.sleep(1)
for i in test.info_player(test.getplayerID('player')):
    print i

print '[*] lineup_player test:\n'
time.sleep(1)
for i in test.lineup_player(test.getplayerID('player')):
    print i

print '[*] info_comunity test:\n'
time.sleep(1)
for i in test.info_comunity('communityID'):
    print i

#plist = []

#x,plist = test.getClub(test.getteamID('Real Madrid'))
#print "Team: %s"%x
#for i in plist:
#    print i


#for i in test.lineup_player(test.getplayerID('nameplayer')):
#    print i


time.sleep(1)

#for i in test.getNews():
#    print i
#print "***"

for i in test.getYourbids():
    print i

#for i in test.info_player(test.getplayerID('nameplayer')):
#    print i

#for i in test.exchangeMarket():
#    print i

test.logout()
