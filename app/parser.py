# -*- coding: utf-8 -*-
import urllib3
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from app.database import DomainRule, session

http = urllib3.PoolManager()


def extract_domain(url):
    o = urlparse(str(url))
    return o.netloc.replace("www.", "")


def extract_text(url):
    domain = extract_domain(url)
    soup = BeautifulSoup(http.request("GET", url).data)

    title = soup.title.text
    main_content = soup

    s = session()
    domain_rule = s.query(DomainRule).filter_by(domain=domain).first()
    s.close()
    if domain_rule:
        main_content = soup.find(domain_rule.element, {"class": domain_rule.css_class})
        if not main_content:
            main_content = soup

    text = " ".join(map(lambda p: p.text, main_content.find_all("p")))
    return title, text
