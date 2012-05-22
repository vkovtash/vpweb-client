#-*- coding: utf-8 -*-

__author__ = 'kovtash'

from serviceFetcher import serviceFetcher
import cookielib, downloader


class AOSFetcher(serviceFetcher):
    SHORT_NAME='AOS'
    def downloadWorker(self,episodeUrl,tmpFilePath):
        return True #TODO: разблокировать загрузку файлов
        aosCookie = cookielib.CookieJar()
        aosCookie.set_cookie(self.makeCookie('UniversalUserID','fd720b1afbfd40d0bc484aec8651fe1e'))
        return downloader.fetchfile(episodeUrl,tmpFilePath,cookie=aosCookie)

    def makeCookie(self,name, value):
        return cookielib.Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain="myvi.ru",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
    )
