comuniopy
=========

Comunio API Python


Intro
-----

This is a simple API to get the information of your comunio account. Comunio is a webgame where You are a manager of a team.


Instalation
-----------

``` 
python setup.py install 
```


Usage
-----

### Login your account and get the information


	>>> from comuniopy import Comunio
	>>> test = Comunio(USER,PASS,LEAGUE)
	>>> test.login()
	>>> uid = test.getID()
	>>> money = test.getMoney()
	>>> teamvalue = test.teamValue()

```


