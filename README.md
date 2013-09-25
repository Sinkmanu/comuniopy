comuniopy
=========

Comunio API Python


Intro
-----

This is a simple API to get the information of your comunio account. Comunio is a webgame where You are a manager of a team.


Installation
-----------

``` 
python setup.py install 
```


Usage
-----

### Login into your account and get the information

```
	>>> from comuniopy import Comunio
	>>> test = Comunio(USER,PASS,LEAGUE)
	>>> test.login()
	>>> uid = test.getID()
	>>> money = test.getMoney()
	>>> teamvalue = test.teamValue()
```
### Get the latest news from your community

```
	>>> from comuniopy import Comunio
	>>> test = Comunio(USER,PASS,LEAGUE)
	>>> test.login()
	>>> news = []
	>>> news = test.getNews()
```

### Functions and methods

#### login()
#### logout()
#### load_info() 
```
This function is included in login()
```
#### getMoney():string
#### getID():string
#### getTeamvalue():string
#### getTitle():string
#### getNews():list
#### standings():list
```
get the standings of the community and return a list with the elements:
position	uid	player	points	teamvalue
``` 
#### info_player(userid):list
```
get the	information of a player and return a list with:
name	email	community_name	points	name	number_notices	list_of_players
```
#### lineup_player(userid):list
```
return a list with the name of players
```
#### info_comunity(teamid):list
```
position        uid     player  points  teamvalue
```
#### getInfo(playerid):list
```
name,position,team,points,price
```
#### getClub(clubid):(string,list)
```
return a tuple with the name and a list:
name,[player list]
```
#### getteamID(team):string
```
	>>> cid = test.getteamID('Real Madrid')
	>>> players = []
	>>> club,players = test.getClub(cid)
```
#### getplayerID(player):string
```
	>>> pid = test.getplayerID('name')
	>>> info = []
	>>> info = test.getInfo(pid)
```
#### exchangeMarket():list
```
return a list with:
name,team,minimum price,market value,points,date,owner,position
```
#### getBidding():list
```
return a list with:
name,bidder,team,money,date,datechange,status
```
#### getYourbids():list
```
return a list with:
name,bidder,team,money,date,datechange,status
```




Author
------

Manuel Mancera (sinkmanu@gmail.com/[@manukaos](https://twitter.com/manukaos))
