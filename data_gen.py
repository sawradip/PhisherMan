import pandas as pd
from utils import getFeatures, feature_names
from tqdm import tqdm


data0 = pd.read_csv("data_files/online-valid.csv")
data0 = data0['url']

phish_url = data0.sample(n = 5000, random_state = 12).copy()
phish_url = phish_url.reset_index(drop=True)


data1 = pd.read_csv("data_files/Legit_site_big_list.csv", header=None)
data1 = data1[0]

legit_url = data1.sample(n = 5000, random_state = 12).copy()
legit_url = legit_url.reset_index(drop=True)


legit_features = []
phish_features = []
legit_label = 0
phish_label = 1

for url in tqdm(legit_url):
  legit_features.append(getFeatures(url, legit_label))

for url in tqdm(phish_url):
  phish_features.append(getFeatures(url, phish_label))

legit_df = pd.DataFrame(legit_features, columns= feature_names)
legit_df.to_csv('data_files/legitimate.csv', index= False)

phish_df = pd.DataFrame(phish_features, columns= feature_names)
phish_df.to_csv('data_files/phishing.csv', index= False)

urldata = pd.concat([legit_df, phish_df]).reset_index(drop=True)
urldata.to_csv('data_files/urldata.csv', index=False)

