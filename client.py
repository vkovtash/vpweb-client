#-*- coding: utf-8 -*-

__author__ = 'kovtash'
from AOSFetcher import AOSFetcher
from vpwebAPI import vpwebAPI
import sys

class CompleteCallback():
    def __init__(self,showKey,episodeNumber):
        self.showKey=showKey
        self.episodeNumber=episodeNumber
    def complete(self):
        vpwebAPI().setEpisodeDownloaded(self.showKey,self.episodeNumber)

class Fetcher():
    def __init__(self,serviceList):
        self._serviceList=[]

        for service in serviceList:
            self._serviceList.append((service[0],service[1]()))

    def fetchAll(self):
        for service in self._serviceList:
            service[1].downloadAll()

    def fetchNewEpisodeList(self):
        episodeList=vpwebAPI().newEpisodes

        for service in self._serviceList:
            shows=episodeList['services'][service[0]]
            serviceWorker = service[1]
            for show in shows:
                showWorker = serviceWorker.appendShow(show['title'],show['season'],show['posterURL'])

                for episode in show['episodes']:
                    print episode['url']
                    showWorker.appendEpisode(episode['number'],episode['url'],CompleteCallback(show['showKey'],episode['number']))


if __name__=='__main__':
    try:
        import socket
        s = socket.socket()
        host = socket.gethostname()
        port = 35636    #make sure this port is not used on this system
        s.bind((host, port))
    except:
        #pass
        print "Already running. Exiting."
        sys.exit(0)

    test = Fetcher([('animeonline.su',AOSFetcher)])
    test.fetchNewEpisodeList()
    test.fetchAll()
