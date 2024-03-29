import flwr as fl
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import pickle
from sklearn.metrics import accuracy_score, log_loss
import utils
import numpy as np
import pandas as pd
from flwr_datasets import FederatedDataset
import argparse



with open('data/processed/loan_status.pkl','rb') as f:
    x_treino,y_treino,x_teste,y_teste = pickle.load(f)

model = DecisionTreeClassifier()


class TreeClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_params()
  
    def fit(self,parameters,config):     
        acc = []
        #utils.set_model_params(model,parameters)
        acc  = utils.get_accuracy(model,x_treino,y_treino,x_teste,y_teste)
        return (utils.get_model_params(model), len(x_treino), {"accuracy": acc})
   
    def evaluate(self,parameters,config):
        acc = []
        loss = []
        #utils.set_model_params(model,parameters)
        model.fit(x_treino,y_treino)
        prediction = model.predict(x_teste).round()


        acc  = accuracy_score(y_teste,prediction)
        loss = log_loss(y_teste, prediction)
        return loss, len(x_teste), {"accuracy": acc}
    
fl.client.start_numpy_client(server_address="127.8.0.1:8080", client=TreeClient())
