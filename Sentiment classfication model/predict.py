import os
import pandas as pd
import torch
import numpy as np
import json
from config import Options
from dataloaders import make_data_loader
from train import train, init_network, evaluate, inference
from config import DEVICE


def predict(content):
    emotion=["0","1","-1"]
    args = Options().parse()
    f=open("predict.txt","w",encoding="utf-8")
    f.write(content)
    f.close()
    vocab, train_loader, val_loader, test_loader, num_class = make_data_loader(args)
    vocab_size = len(vocab)

    from models.FastText import FastText, Config
    config = Config()
    model = FastText(config, vocab_size, num_class)
    model.to(DEVICE)
    model.load_state_dict(torch.load(args.model + '.ckpt',map_location='cpu'))
    y_preds = inference(args, model, test_loader)
    return emotion[y_preds[0]]

if __name__ == '__main__':
    files_path='C:\\Users\\cheng sirui\\Desktop\\Project\\merge\\'
    files=os.listdir(files_path)
    for file in files:
        tmp=pd.read_csv(files_path+file)
        tmp['emotion']=tmp['tweets'].apply(predict)
        tmp.to_csv('C:\\Users\\cheng sirui\\Desktop\\Project\\merge_emo\\'+file)
        print(file+' done')
    # twitter="Stand Your Ground authors: Trayvon Martin’s shooter should likely be charged. http://t.co/Ij79FA7x http://t.co/151g5qsP via @miamiherald"
    # res=predict(twitter)
    # print(res)

