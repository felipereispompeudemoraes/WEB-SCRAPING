import requests
from bs4 import BeautifulSoup
from model.BaseHistorica import BaseHistorica

from model.MetaDado import MetaDado

BASE_INNER_URL = "https://www6g.senado.gov.br/apem/"
STRIP_CHARS = "\xa0: \t"

class Scrap:
    @staticmethod
    def getMetadadoExistente(bh, chave):
        ret = None
        if isinstance(bh, BaseHistorica):
            for md in bh.dados:
                if md.chave == chave:
                    ret = md
                    break
        return ret

    @staticmethod
    def getSoup(url):
        page = requests.get(url)
        return BeautifulSoup(page.content, "html.parser")

    @staticmethod
    def extrairInnerDocBusca(url, bh):
        if isinstance(bh, BaseHistorica):
            soup = Scrap.getSoup(url)
            chaves = soup.select('div.result_col1')
            valores = soup.select('div.result_col2, div.texto_pre')
            i = 0
            for chave in chaves:
                chaveStr = chave.text.strip(STRIP_CHARS).upper()
                md = Scrap.getMetadadoExistente(bh, chaveStr)
                if md == None:
                    md = MetaDado()
                    md.chave = chaveStr
                    bh.dados.append(md)
                md.valor = valores[i].text.strip(STRIP_CHARS)
                i += 1

    @staticmethod
    def getProximaUrl(soupObject):
        ret = None
        if(isinstance(soupObject, BeautifulSoup)):
            a = soupObject.select_one('body > div.results > table > tr:nth-child(2) > td > a:last-of-type')
            if a != None and a.text.strip(STRIP_CHARS) != '...':
                ret = BASE_INNER_URL + a.get('href')
        return ret

    @staticmethod
    def extrairDocBusca(soupObject):
        ret = []
        if(isinstance(soupObject, BeautifulSoup)):
            docs = soupObject.select('div.docHit')
            for doc in docs:
                id = int(doc.select_one(".col1").text.strip(STRIP_CHARS))
                col2s = doc.select(".col2")
                col3s = doc.select(".col3")
                i = 0
                bh = BaseHistorica()
                bh.id = id
                bh.dados = []
                for col2 in col2s:
                    md = MetaDado()
                    md.chave = col2.text.strip(STRIP_CHARS).upper()
                    valorElem = col3s[i] 
                    md.valor = valorElem.text.strip(STRIP_CHARS)
                    anchor = valorElem.select_one('a')
                    if anchor != None:
                        url = BASE_INNER_URL + anchor.get('href')
                        mdUrl = MetaDado()
                        mdUrl.chave = "URL"
                        mdUrl.valor = url
                        bh.dados.append(mdUrl)
                        check_url = url.lower()
                        if check_url.endswith(".html") or check_url.endswith(".htm"):
                            Scrap.extrairInnerDocBusca(url, bh)
                    bh.dados.append(md)
                    i += 1
                ret.append(bh)
        return ret