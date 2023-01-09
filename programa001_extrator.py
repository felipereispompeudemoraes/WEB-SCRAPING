import time
from lib.Db import db_session
from lib.Scrap import Scrap

SLEEP_TIME = 30

conector_db = db_session()

#url_inicial = "https://www6g.senado.gov.br/apem/search?browse-all=yes"
url_inicial = "https://www6g.senado.gov.br/apem/search?browse-all=yes;startDoc=29881"

url = url_inicial

while url != None:
    try:
        html = Scrap.getSoup(url)
        list = Scrap.extrairDocBusca(html)
        prox_url = Scrap.getProximaUrl(html)
        conector_db.add_all(list)
        conector_db.commit()
        print("Sucesso ao obter dados na URL " + url)
        url = prox_url
    except:
        print("Houve um erro na URL " + url + ". Aguardando " + str(SLEEP_TIME) + " segundos para tentar novamente.")
        time.sleep(SLEEP_TIME)