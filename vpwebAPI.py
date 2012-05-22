#-*- coding: utf-8 -*-

__author__ = 'kovtash'

import os.path,downloader,logging

class vpwebAPI():
    def __init__(self):
        self._serverURL='http://vpsrvr.appspot.com'
        self._newEpisodes=None

    def getData(self,dataURL):
        requestURL=os.path.join(self._serverURL,dataURL)

        result=None
        response=downloader.JSONDocGet(requestURL).data
        if response is not None:
            try:
                result=response['response']
            except KeyError:
                pass
        return result

    @property
    def newEpisodes(self):
        if self._newEpisodes is None:
            self._newEpisodes=self.getData('getnewepisodes')
        return self._newEpisodes

    def getServiceShows(self,serviceName):
        try:
            result=self.newEpisodes['services'][serviceName]
        except KeyError:
            result=None
        return result

    def setEpisodeDownloaded(self,showKey,episodeNumber):
        #TODO:setEpisodeDownloaded
        requestURL=os.path.join(self._serverURL,'setdownloaded')
        logging.error("".join([episodeNumber]))
        downloader.DocGet(requestURL,params=[("ep_num",episodeNumber),("show_key",showKey)])

if __name__=='__main__':
    testModel=vpwebAPI()
    logging.error(testModel.newEpisodes)
    logging.error(testModel.getServiceShows('animeonline.su'))