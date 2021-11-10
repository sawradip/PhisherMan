import re
import os
import pandas as pd
from bs4 import BeautifulSoup
import whois
import requests
import urllib
import urllib.request
from datetime import datetime
from urllib.parse import urlparse,urlencode
import ipaddress


shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                      'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
                      'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards', 'Label']

util_funcs = {
    'url':{
        'getDomain'       : lambda url : urlparse(url).netloc.replace('www.', ''),
        'ipInDOmain'      : lambda url : 1 if haveIpAddress(url) else 0,
        'haveAtSign'      : lambda url : 1 if '@' in url else 0,
        'isLongURL'       : lambda url : 1 if len(url) > 50 else 0,
        'depthOfDomain'   : lambda url : len([urlPart for urlPart in url.split(r'/') if (urlPart != '')]),
        'urlRedirection'  : lambda url : 1 if url.rfind('//') > 7 else 0,
        'httpsInDOmain'   : lambda url : 1 if 'https' in urlparse(url).netloc else 0,
        'isShortened'     : lambda url : 1 if re.search(shortening_services,url) else 0,
        'hyphenInDomain'  : lambda url : 1 if '-' in urlparse(url).netloc else 0,
        'urlNotInDNS'     : lambda url : 1 if getDomainInfo(url) else 0,
        'isPopular'       : lambda url : 1 if 0 < web_traffic(url) < 100000 else 0,
    },

    'dnsInfo' :{
        'isDomainAged'    : lambda dnsInfo : domainAge(dnsInfo),
        'isExpirationNear': lambda dnsInfo : domainEnd(dnsInfo),
    },

    'response': {
        'isIframeMissing' : lambda response : 0 if response and re.findall(r"[<iframe>|<frameBorder>]", response.text) else 1,
        'isStatbarChanged': lambda response : 0 if response and not re.findall("<script>.+onmouseover.+</script>", response.text) else 1,
        'isRclickDisabled': lambda response : 0 if response and re.findall(r"event.button ?== ?2", response.text) else 1,
        'isForwarded'     : lambda response : 0 if response and len(response.history) <= 2 else 1,
    }
}

def domainAge(domain_name):
    if domain_name is None:
        return 1
    # print(domain_name)
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
        try:
            creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain/30) < 6):
            age = 1
        else:
            age = 0
    return age

def domainEnd(domain_name):
    if domain_name is None:
        return 1
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date,str):
        try:
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    elif (type(expiration_date) is list):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end/30) < 6):
            end = 0
        else:
            end = 1
    return end

def getDomainInfo(url):
    try:
        dnsInfo = whois.whois(urlparse(url).netloc)
        return dnsInfo
    except:
        return None

def getUrlResponse(url):
    try:
        response = requests.get(url)
    except:
        response = ""
    return response

def haveIpAddress(url):
  try:
    ipaddress.ip_address(url)
    return ip
  except:
    return None

def web_traffic(url):
    try:
        #Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "lxml").find(
            "REACH")['RANK']
        rank = int(rank)
    except TypeError:
            return 0
    return rank


def getFeatures(url, label = None):
    dnsInfo = getDomainInfo(url)
    response = getUrlResponse(url)
    features = []
    url_funcs = util_funcs['url']
    dnsInfo_funcs = util_funcs['dnsInfo']
    response_funcs = util_funcs['response']

    url_features = [func(url) for func in url_funcs.values() ]
    features.extend(url_features)

    dnsInfo_features = [func(dnsInfo) for func in dnsInfo_funcs.values() ]
    features.extend(dnsInfo_features)

    response_features = [func(response) for func in response_funcs.values() ]
    features.extend(response_features)

    if label is not None:
        features.append(label)

    # for i, func in enumerate(url_funcs.values()):
    #     func(url)
    #     print(i)
    return features

try:
    urldata = pd.read_csv(os.path.join('data_files','urldata.csv'))
except FileNotFoundError:
    urldata = pd.read_csv(os.path.join('..','data_files','urldata.csv'))

def getSaneFeatures(url):
    if not url.startswith('http'):
        url = 'https://' + url
    
    feat = getFeatures(url)
    refined_url = feat[0]
    # print(feat.shape)
    if refined_url in urldata['Domain'].tolist():
        feat = urldata[urldata['Domain'] == refined_url].iloc[0, :-1].values
        feat[1:] = feat[1:].astype(int)
        feat = list(feat)
        # print(feat.shape)
    
    return feat


class Results:
    def __init__(self):
        self.model = []
        self.acc_train = []
        self.acc_test = []

    def add(self, model, tr, ts):
        self.model.append(model)
        self.acc_train.append(round(tr, 4))
        self.acc_test.append(round(ts, 4))

    def get_df(self):
        return pd.DataFrame({    
                                'ML Model': self.model,    
                                'Train Accuracy': self.acc_train,
                                'Test Accuracy': self.acc_test
                                })

if __name__ == "__main__":
    feat = getFeatures('http://facebook.com/')
    print(feat)
