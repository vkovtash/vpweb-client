#-*- coding: utf-8 -*-

__author__ = 'kovtash'

import os.path, os, logging, downloader, sys

if sys.platform == 'darwin':
    LIBRARY_DIR = '/Users/kovtash/vpweb'
elif sys.platform == 'linux2':
    LIBRARY_DIR = '/Volumes/Library/vpweb'

class Show():
    class Episode():
        def __init__(self,parentShow=None,episodeNumber=None,episodeUrl=None,completeCallback=None):
            self._episodeNumber=episodeNumber
            self._episodeUrl=episodeUrl
            self._completeCallback=completeCallback
            self._parentShow=parentShow

        @property
        def episodeNumber(self):
            return self._episodeNumber

        @property
        def episodeUrl(self):
            return self._episodeUrl

        @property
        def episodeFilename(self):
            result="Unknown"
            suffix = ""
            if self._parentShow is not None:
                if self._parentShow.showName is not None:
                    result = self._parentShow.showName
                    result = result.replace(" ","_")
                if self._parentShow.showSeason is not None:
                    suffix = "".join([suffix,'S',self._parentShow.showSeason])

            if self.episodeNumber is not None:
                suffix = "".join([suffix,'E',str(self.episodeNumber)])

            result = "".join([result,'_',suffix])

            return result.strip('_')

        @property
        def completeCallback(self):
            return self._completeCallback

    def __init__(self,showName=None,showSeason=None,posterURL=None):
        self._showName=showName
        self.showSeason=showSeason
        self._posterURL=posterURL
        self.episodeList=[]
        self.index=0

    def __iter__(self):
        #sort episodes
        self.episodeList = sorted(self.episodeList, key=lambda k: int(k.episodeNumber))
        return self

    @property
    def posterURL(self):
        return self._posterURL

    @property
    def posterFilename(self):
        return self.showName.replace(' ','_')

    @property
    def showName(self):
        return self._showName

    def appendEpisode(self,number,url,callback=None):
        self.episodeList.append(self.Episode(self,number,url,callback))

    def next(self):
        if self.index  >= len(self.episodeList):
            raise StopIteration

        result=self.episodeList[self.index]
        self.index = self.index + 1
        return result


class serviceFetcher():
    SHORT_NAME='' #Требует оверрайда
    def __init__(self):
        self.showList=[]
        self.TMP_DIR = os.path.join(LIBRARY_DIR,'tmp')
        self.COMPLETE_DIR=os.path.join(LIBRARY_DIR,'complete')
        self.POSTER_DIR=os.path.join(LIBRARY_DIR,'poster')

    def appendShow(self,showName,showSeason,posterURL):
        self.showList.append(Show(showName,showSeason,posterURL))
        return self.showList[len(self.showList)-1]

    def downloadEpisode(self,episodeUrl,episodeFilename,completeCallback):

        if not os.path.exists(self.TMP_DIR):
            os.makedirs(self.TMP_DIR)

        tmpFilename=os.path.join(self.TMP_DIR,episodeFilename)
        completeFilename=os.path.join(self.COMPLETE_DIR,episodeFilename)

        logging.error("".join(["Begin download file ",episodeFilename, ' into ', tmpFilename]))
        if self.downloadWorker(episodeUrl,tmpFilename):
            completeCallback.complete()

            if not os.path.exists(self.COMPLETE_DIR):
                os.makedirs(self.COMPLETE_DIR)

            if os.path.exists(tmpFilename):
                os.rename(tmpFilename,completeFilename)

    def downloadPoster(self,posterURL,posterName):
        if not os.path.exists(self.POSTER_DIR):
            os.makedirs(self.POSTER_DIR)

        posterFilename=os.path.join(self.POSTER_DIR,posterName)

        if not os.path.exists(posterFilename):
            self.downloadPosterWorker(posterURL,posterFilename)

    def downloadPosterWorker(self,posterURL,posterFilename):
        """
        Требует оверрайда.
        """
        #=================Add your code here====================

        downloader.fetchfile(posterURL,posterFilename)
        #=======================================================


    def downloadWorker(self,episodeUrl,tmpFilePath):
        """
        Требует оверрайда. Должна возвращать True в случае успешного завершения загрузки. Иначе False
        """
        #=================Add your code here====================

        print tmpFilePath, episodeUrl
        return True
        #=======================================================

    def downloadAll(self):
        #sort sows by season
        self.showList = sorted(self.showList, key=lambda k: int(k.showSeason))
        for show in self.showList:
            self.downloadPoster(show.posterURL,show.posterFilename)
            for episode in show:
                self.downloadEpisode(episode.episodeUrl,episode.episodeFilename,episode.completeCallback)
