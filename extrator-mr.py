#!/usr/bin/env python3
# -*- coding: UTF-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import bs4
import requests
import re
from urllib.request import urlretrieve
import os.path
import csv


if __name__ == "__main__":
    base__url = "http://pesquisa.memoriasreveladas.gov.br/mrex/consulta/"
    first_url = "http://pesquisa.memoriasreveladas.gov.br/mrex/consulta/resultado_pesquisa_new.asp?v_pesquisa=&v_fundo_colecao=1278707&Pages={}"

    cookies = dict(ASPSESSIONIDCCBQCQSR='EEPJMIIDAOLDBMOABLJODJAJ',ASPSESSIONIDACCRCQSQ='BPKADPKDIEABCDGGLBAAHEAK',ASPSESSIONIDCACTCQSQ='EEGDOMLCJKKNGPFIPJLCMFBI',TS01dc25d1='01770c3a9841dbb80f087c5796c0c8a70c918eb8b9a5fb7229d46b84e736c80391564a8a27de44504d56d751444c19f2040f128a02c04b95e7951acf7b4448895e221d9514')

    series = ['BR RJANRIO CNV.0.ERE','BR RJANRIO CNV.0.OCO','BR RJANRIO CNV.0.PEI','BR RJANRIO CNV.0.EST','BR RJANRIO CNV.0.GRG','BR RJANRIO CNV.0.RCE']

    arquivos = []

    for serie in series:

        payload = {'input_pesqfundocolecao': '1278707', 'input_pesqnotacao': serie,'v_fundo_colecao': '1278707', 'v_ordem': 'CodigoReferencia' }

        if not os.path.exists(serie):
            os.makedirs(serie)

        with open('{}/{}.csv'.format(serie, serie), 'w', newline='') as f:
            writer = csv.writer(f)

            num_pgs = 2
            pagina = 1

            while pagina <= num_pgs:
                url = first_url.format(pagina)
                print('Serie', serie, 'lendo pagina', pagina, 'de', num_pgs)

                r = requests.post(url, data=payload, cookies=cookies)
                r.encoding = 'utf-8'

                s1 = bs4.BeautifulSoup(r.text, "lxml")

                ulres = s1.find('ul', id='resultado')

                ptp = re.compile(r'var TotalPag = (\d+)')
                match = ptp.search(r.text)
                if match:
                    num_pgs = int(match.group(1))

                # cnt = 0
                for li in ulres.find_all('li'):
                    l = li.find("a", title="Fazer download do arquivo")

                    if l and l.find_parent('li') == li:
                        link = l["onclick"]
                        parts = link.split('\',\'')
                        arq = parts[0][30:]
                        arq_name = parts[1]
                        link = "{}download.asp?NomeArquivo={}&arquivo={}&apresentacao=2".format(base__url, arq_name, arq)
                        arquivos.append((link, arq_name, serie))
                    else:
                        arq_name = 'Sem arquivo'
                        link = '--'

                    description = li.span.text

                    writer.writerow((description, arq_name, link))
                    # cnt += 1
                    # print('Dados:', cnt, serie, description[1:10], arq_name)

                pagina += 1

    for arq_tpl in arquivos:
        filename = '{}/{}'.format(arq_tpl[2], arq_tpl[1])
        if not os.path.isfile(filename):
            urlretrieve(arq_tpl[0], filename)
            print('Carregou arquivo:', filename)
