import sys
import argparse
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

if len(sys.argv) == 1:
  raise argparse.ArgumentError

if 'legit' in sys.argv:
  legit_features = []
  legit_label = 0
  for url in tqdm(legit_url):
    legit_features.append(getFeatures(url, legit_label))

  legit_df = pd.DataFrame(legit_features, columns= feature_names)
  legit_df.to_csv('data_files/legitimate.csv', index= False)


if 'phishing' in sys.argv:
  phish_features = []
  phish_label = 1
  for url in tqdm(phish_url):
    phish_features.append(getFeatures(url, phish_label))

  phish_df = pd.DataFrame(phish_features, columns= feature_names)
  phish_df.to_csv('data_files/phishing.csv', index= False)

if 'urldata' in sys.argv:
  legit_df = pd.read_csv("data_files/legitimate.csv")
  phish_df = pd.read_csv("data_files/phishing.csv")

  if 'Tiny_URL' in phish_df.columns:
    phish_df['TinyURL'] = phish_df['Tiny_URL']
    phish_df.drop('Tiny_URL', 1, inplace = True)
  urldata = pd.concat([legit_df, phish_df]).reset_index(drop=True)
  print(legit_df.columns)
  print(phish_df.columns)
  urldata.to_csv('data_files/urldata.csv', index=False)

if __name__ == "__main__":
  if len(sys.argv) == 2:
    args = sys.argv[1]

