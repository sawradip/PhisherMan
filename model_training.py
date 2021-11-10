import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from utils import Results

result = Results()

data0 = pd.read_csv(os.path.join('data_files', 'urldata.csv'))
data = data0.drop(['Domain'], axis = 1).copy()

X = data.drop('Label',axis=1)
y = data['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 12)

# Decision Tree
tree = DecisionTreeClassifier(max_depth = 5)
tree.fit(X_train, y_train)

y_test_pred = tree.predict(X_test)
y_train_pred = tree.predict(X_train)

acc_train = accuracy_score(y_train,y_train_pred)
acc_test = accuracy_score(y_test,y_test_pred)

print("Training - Decision Tree")
result.add('Decision Tree', acc_train, acc_test)

# Random Forest
forest = RandomForestClassifier(max_depth=5)
forest.fit(X_train, y_train)

y_test_pred = forest.predict(X_test)
y_train_pred = forest.predict(X_train)

acc_train = accuracy_score(y_train,y_train_pred)
acc_test = accuracy_score(y_test,y_test_pred)

print("Training - Random Forest")
result.add('Random Forest', acc_train, acc_test)


# Support Vector Classifier
svc = SVC( kernel = "rbf" , random_state = 0)
svc.fit(X_train,y_train)

y_test_pred = svc.predict(X_test)
y_train_pred = svc.predict(X_train)

acc_train = accuracy_score(y_train,y_train_pred)
acc_test = accuracy_score(y_test,y_test_pred)

print("Training - Support Vector Classifier")
result.add('Support Vector Classifier', acc_train, acc_test)

# Multi Layer Perceptron
mlp = MLPClassifier(alpha=0.001, hidden_layer_sizes=([100,100,100]))

mlp.fit(X_train, y_train)

y_test_pred = mlp.predict(X_test)
y_train_pred = mlp.predict(X_train)

acc_train = accuracy_score(y_train,y_train_pred)
acc_test = accuracy_score(y_test,y_test_pred)

print("Training - Multi Layer Perceptron")
result.add('Multi Layer Perceptron', acc_train, acc_test)



# XGBoost
xgb = XGBClassifier(learning_rate=0.4,max_depth=7)

xgb.fit(X_train, y_train)

y_test_pred = xgb.predict(X_test)
y_train_pred = xgb.predict(X_train)

acc_train = accuracy_score(y_train,y_train_pred)
acc_test = accuracy_score(y_test,y_test_pred)

print("Training - XGBoost")
result.add('XGBoost', acc_train, acc_test)

pickle.dump(xgb, open(os.path.join('data_files','XGBoost_phishing_detector.pkl'), "wb"))

if __name__ == "__main__":
    print(result.get_df())