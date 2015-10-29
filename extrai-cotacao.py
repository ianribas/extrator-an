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

    URL_COTACAO = "https://ptax.bcb.gov.br/ptax_internet/consultaBoletim.do?method=consultarBoletim&RadOpcao=3&DATAINI=%s&ChkMoeda=61"
    primeiro = True

    while True:
        cotacao_alvo = 3.75

        st = time.gmtime()
        hoje = time.strftime('%d/%m/%Y')

        if st.tm_wday < 5 and (primeiro or (st.tm_hour > 7 and st.tm_hour < 18)):

            r = requests.get(URL_COTACAO % hoje)

            for match in re.finditer(r"<td.*(\d+,\d+)</td>", r.text):
                cotacao = float(match.group(1).replace(',', '.'))
                print "Found! Cotacao is ", cotacao
                if cotacao < cotacao_alvo:
                    avisa(cotacao)

            primeiro = False
            time.sleep(3600)