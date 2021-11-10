import os
import pickle
from tkinter import *
import pandas as pd
import numpy as np
from utils import getSaneFeatures, feature_names

root = Tk()
root.geometry("644x433")
root.maxsize(1000, 625)

root.title("PhisherMan - Check Phishing Sites")

project_title = Label(  root,
                        text = " PhisherMan", 
                        fg = "blue",
                        padx = 100, 
                        pady = 50, 
                        # relief = SUNKEN,
                        font=("comicsansms", 33, "bold"))
project_title.pack()

input_box = Text(root, height = 3,  width = 100, font=("comicsansms", 15))
input_box.insert("1.0", "\n  ", "center")
# input_box.grid(pady = 20)
input_box.pack(padx = 50, pady = 20)

url_response = Label(  root,
                    text = "",
                    pady = 30, 
                    font=("comicsansms", 23, "bold")
                    )

def checkURL():

    xgb_loaded = pickle.load(open(os.path.join('data_files','XGBoost_phishing_detector.pkl'), "rb"))
    url = input_box.get("1.0", "end-1c")
    print(url)

    url_features = np.array(getSaneFeatures(url)[1:]).reshape((1, 16))
    # print(url_features)
    X_test = pd.DataFrame(url_features, columns= feature_names[1:-1])
    # print(X_test)
    prediction = xgb_loaded.predict(X_test)[0]

    if url == "":
        response = f"URL is an Empty String"
        url_response['fg'] = 'black'
    elif prediction > 0.5:
        response = f"{url} \n is a Phishing Site"
        url_response['fg'] = 'red'
    else:
        response = f"{url} \n is not a Phishing Site"
        url_response['fg'] = 'green'

    url_response['text'] = response 
    




check_btn = Button(root, text = "Check", bg = "deep sky blue", fg = "white", font=('Calibri', '20'), command = checkURL)
check_btn.pack()


url_response.pack()

root.mainloop()