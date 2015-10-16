#!/usr/bin/env python
# -*- coding: UTF-8
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import bs4
import requests
import re
import urlparse
import os.path
import urllib


pat_d = re.compile("(\d\d)?/?(\d\d)?/?(\d\d\d\d)")

def format_date(string):
    m = pat_d.search(string)
    ret = ""
    if m:
        ret = "".join([e + "_" for e in reversed(m.groups()) if e])

    if not ret:
        ret="_SEM_DATA__"

    return ret

r = requests.get("http://www.an.gov.br/sian/multinivel/multinivel_consulta5.asp?v_codReferenciaPai_ID=1316324&v_codFundo_ID=&v_nivel=4&v_pula_nivel=")
s1 = bs4.BeautifulSoup(r.text, "html.parser")

pat = re.compile('[^\w ]+')
p_s = re.compile("\s+")
p_did = re.compile(".*fjs_editar.(\d+).*")

doc_links = s1.find_all("a", href=re.compile("javascript:fjs_editar\("))


for l in doc_links:
    n = l.parent.parent.contents[7].text
    n = format_date(l.parent.parent.contents[11].text) + p_s.sub("_", pat.sub("", n))[:20]
    did = p_did.sub(r"\1", l["href"])
    lnk = "http://www.an.gov.br/sian/Multinivel/Lista_Diretorios.asp?visualiza=0&v_CodReferencia_ID=" + did
    print n, lnk

    r = requests.get(lnk)
    s2 = bs4.BeautifulSoup(r.text, "html.parser")
    la = s2.find("a", href=re.compile("Mostra_Arquivo.asp"))
    if la:
        v_arquivo = urlparse.parse_qs(urlparse.urlparse(la["href"]).query).get("v_arquivo")[0]

        i = 0
        fname = n + v_arquivo[-4:]
        while os.path.isfile(fname) and i < 10000:
            i += 1;
            fname = n + "_" + str(i) +  v_arquivo[-4:]

        urllib.urlretrieve (v_arquivo, fname)
        print "Saved", v_arquivo, " to ", fname
