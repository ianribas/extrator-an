#!/usr/l/env python
# -*- coding: UTF-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from osxnotification import notify
import time
import requests
import re

def avisa(cotacao):
    title = "Dolar baixou!"
    msg = "Valor atual é %f" % cotacao
    print title, msg
    notify(title, None, msg)


if __name__ == "__main__":

    URL_COTACAO = "https://ptax.bcb.gov.br/ptax_internet/consultarUltimaCotacaoDolar.do"
    cotacao_alvo = 3.75

    while True:
        r = requests.get(URL_COTACAO)

        match = re.search(r"<td.*(\d+,\d+)</td>", r.text)
        if match:
            cotacao = float(match.group(1).replace(',', '.'))
            print "Found! Cotacao is ", cotacao
            if cotacao < cotacao_alvo:
                avisa(cotacao)
        else:
            print "Not found. Estranho ..."
        time.sleep(3600)