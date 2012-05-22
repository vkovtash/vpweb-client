#-*- coding: utf-8 -*-

__author__ = 'kovtash'

from serviceFetcher import serviceFetcher
import cookielib, downloader, json, logging

class SORGFetcher(serviceFetcher):
    SHORT_NAME = 'SORG'
    def downloadWorker(self,episodeUrl,tmpFilePath):

        showURL = episodeUrl.split('|')[0]
        episodeID = episodeUrl.split('|')[1]
        showCookie = cookielib.CookieJar()
        showPage=downloader.HTMLDocGet(showURL,None,showCookie)

        #Если не удалось получить страницу, перейти к слеующей
        if showPage.data==None:
            logging.error("Can\'t fetch show page")
            return False

        playlistRaw="".join(showPage.data.xpath('//div[@class="content"]/script/descendant::text()')).replace('\\/','/')


        playlistDataStart=playlistRaw.find('p.setPlaylist( ')+15
        playlistData=playlistRaw[playlistDataStart:playlistRaw.find(']',playlistDataStart)+1]

        playlist=json.loads(playlistData)

        episodeURL=None

        for playlistEntry in playlist:
            if str(playlistEntry[u"episodeId"])==episodeID:
                episodeURL=playlistEntry[u"file"]

        if episodeURL==None:
            logging.error("Can\'t find clip url")
            return False

        logging.error(episodeURL)
        return True #TODO: разблокировать загрузку файлов
        return downloader.fetchfile(episodeURL,tmpFilePath,cookie=showCookie)