#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import requests
from bs4 import BeautifulSoup

Leagues = {'BBVA':'www.comunio.es',
           'Adelante':'www.comuniodesegunda.es',
           'Bundesliga':'www.comunio.de',
           'Bundesliga2':'www.comdue.de',
           'Serie A':'www.comunio.it',
           'Premier League':'www.comunio.co.uk',
           'Liga Sagres':'www.comunio.pt'}


#You can use the user-agent that you want (This is only an example)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'

class Comunio:

    def __init__(self,username,password,league):
        self.username = username
        self.password = password
        self.domain = Leagues[league]
        self.session = requests.session()

    def login(self):
        payload = { 'login':self.username,
                    'pass':self.password,
                    'action':'login'}
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","User-Agent": user_agent}
        req = self.session.post('http://'+self.domain+'/login.phtml',headers=headers,data=payload).content
        soup = BeautifulSoup(req)
        self.load_info() #Function to load the account information
    
    def load_info(self):
        """Get info from account logged"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/login.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/team_news.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        self.title = soup.title.string
        
        estado = soup.find('div',{'id':'content'}).find('div',{'id':'manager'}).string                                      
        [s.extract() for s in soup('strong')]
        if (soup.find('div',{'id':'userid'}) != None):
            self.id = soup.find('div',{'id':'userid'}).p.text
            self.money = soup.find('div',{'id':'manager_money'}).p.text
            self.teamvalue = soup.find('div',{'id':'teamvalue'}).p.text

    def getMoney(self):
        return self.money

    def getTeamvalue(self):
        return self.teamvalue
    
    def getID(self):
        return self.id

    def getTitle(self):
        return self.title

    def getNews(self):
        """Only work if you are logged"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/login.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/team_news.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        news = []
        for i in soup.find_all('div',{'class','article_content_text'}):
            news.append(i.text)
        return news
        

    def logout(self):
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","User-Agent": user_agent}
        self.session.get('http://'+self.domain+'/logout.phtml',headers=headers)

    
    def standings(self):
        """Get standings from the comunity of account"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/standings.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        table = soup.find('table',{'id':'tablestandings'}).find_all('tr')
        clasificacion = []
        [clasificacion.append(('%s\t%s\t%s\t%s\t%s')%(tablas.find('td').text,tablas.find('div')['id'],tablas.a.text,tablas.find_all('td')[3].text,tablas.find_all('td')[4].text)) for tablas in table[1:]]
        return clasificacion

    def info_player(self,userid):
         """Get player info using a ID"""
         headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/standings.phtml',"User-Agent": user_agent}
         req = self.session.get('http://'+self.domain+'/playerInfo.phtml?pid='+userid,headers=headers).content
         soup = BeautifulSoup(req)
         title = soup.title.string 
         comunity = soup.find_all('table',border=0)[1].a.text
         info = []
         info.append(title)
         info.append(comunity)
         for i in soup.find_all('table',border=0)[1].find_all('td')[1:]:
             info.append(i.text)
         for i in soup.find('table',cellpadding=2).find_all('tr')[1:]:
             cad = i.find_all('td')
             team = i.find('span')['title']
             info.append("%s\t%s\t%s\t%s\t%s\t%s"%(cad[0].text,cad[2].text,team,cad[4].text,cad[5].text,cad[6].text))
         return info

    def lineup_player(self,userid):
         """Get player lineup using a ID"""
         headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/standings.phtml',"User-Agent": user_agent}
         req = self.session.get('http://'+self.domain+'/playerInfo.phtml?pid='+userid,headers=headers).content
         soup = BeautifulSoup(req)
         info = []
         for i in soup.find_all('td',{'class':'name_cont'}):
             info.append(i.text)
         return info

    def info_comunity(self,teamid):
        """Get comunity info using a ID"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/standings.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/teamInfo.phtml?tid='+teamid,headers=headers).content
        soup = BeautifulSoup(req)
        info = []
        for i in soup.find('table',cellpadding=2).find_all('tr')[1:]:
            info.append('%s\t%s\t%s\t%s\t%s'%(i.find('td').text,i.find('a')['href'].split('pid=')[1],i.a.text,i.find_all('td')[2].text,i.find_all('td')[3].text))
        return info


    def getInfo(self,pid):
       """Get info by football player using a ID"""
       """Return name,position,team,points,price"""
       headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
       req = self.session.get('http://'+self.domain+'/tradableInfo.phtml?tid='+pid,headers=headers).content
       soup = BeautifulSoup(req)
       info = []
       info.append(soup.title.text)
       for i in soup.find('table',cellspacing=1).find_all('tr'):
           info.append(i.find_all('td')[1].text)
       return info

    def getClub(self,cid):
       """Get info by team using a ID"""
       """Return name,[player list]"""
       headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/',"User-Agent": user_agent}
       req = self.session.get('http://'+self.domain+'/clubInfo.phtml?cid='+cid,headers=headers).content
       soup = BeautifulSoup(req)
       plist = []
       for i in soup.find('table',cellpadding=2).find_all('tr')[1:]:
           plist.append('%s\t%s\t%s\t%s\t%s'%(i.find_all('td')[0].text,i.find_all('td')[1].text,i.find_all('td')[2].text,i.find_all('td')[3].text,i.find_all('td')[4].text))
       return soup.title.text,plist

    def getteamID(self,team):
        """Get team ID using a name"""
        """return an ID"""
        #UTF-8 comparison
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain,headers=headers).content
        soup = BeautifulSoup(req)
        for i in soup.find('table',cellpadding=2).find_all('tr'):
           #Get teamid from the bets
           team1 = i.find('a')['title']
           team2 = i.find_all('a')[1]['title']
           if (team == team1):
               return i.find('a')['href'].split('cid=')[1]
           elif (team == team2):
               return i.find_all('a')[1]['href'].split('cid=')[1]
        
        return None


    def getplayerID(self,player):
        """Get player ID using a name. Only work if you are logged"""
        """return an ID"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/standings.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        for i in soup.find('table',cellpadding=2).find_all('tr'):
           if (player == i.find_all('td')[2].text):
               return  i.find('a')['href'].split('pid=')[1]
        
        return None

    def exchangeMarket(self):
        """Only work if you are logged"""
        """return name,team,minimum price,market value,points,date,owner,position"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/exchangemarket.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        info = []
        for i in soup.find('table',{'class','tablecontent03'}).find_all('tr')[1:]:
           info.append('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(i.find_all('td')[0].text,i.find('span')['title'],i.find_all('td')[2].text,i.find_all('td')[3].text,i.find_all('td')[4].text,i.find_all('td')[5].text,i.find_all('td')[6].text,i.find_all('td')[7].text))
        return info

    def getBidding(self):
        """Only work if you are logged"""
        """return name,bidder,team,money,date,datechange,status"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/exchangemarket.phtml?viewoffers_x=',headers=headers).content
        soup = BeautifulSoup(req)
        table = []
        for i in soup.find('table',{'class','tablecontent03'}).find_all('tr')[1:]:
            table.append('%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(i.find_all('td')[0].text,i.find_all('td')[1].text,i.find('span')['title'],i.find_all('td')[3].text,i.find_all('td')[4].text,i.find_all('td')[5].text,i.find_all('td')[6].text))
        return table

    def getYourbids(self):
        """Only work if you are logged"""
        """return name,bidder,team,money,date,datechange,status"""
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/exchangemarket.phtml?viewoffers_x=',headers=headers).content
        soup = BeautifulSoup(req)
        table = []
        for i in soup.find_all('table',{'class','tablecontent03'})[1].find_all('tr')[1:]:
            table.append('%s\t%s\t%s\t%s\t%s\t%s\t%s\t'%(i.find_all('td')[0].text,i.find_all('td')[1].text,i.find('span')['title'],i.find_all('td')[3].text,i.find_all('td')[4].text,i.find_all('td')[5].text,i.find_all('td')[6].text))
        return table
        
	




