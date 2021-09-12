import json
import numpy as np
import pickle as pkl
from torch.utils import data
from dataloaders import custom_transforms as tr
from config import DEVICE
from dataloaders.custom_transforms import UNK, PAD

# get word frequency dictionary from data set.
def build_vocab(file_path, tokenizer, max_len, min_freq=3):
    vocab_dic = {}
    with open(file_path, 'r',encoding="utf-8") as f:
        data = f.readlines()
    texts=[]
    for each in data:
        m=each.split("\t")
        if(len(m)==2):
            texts.append(m[0])
    for text in texts:
        for word in tokenizer.tokenize(text):
            vocab_dic[word] = vocab_dic.get(word, 0) + 1
    vocab_list = sorted([_ for _ in vocab_dic.items() if _[1] >= min_freq], key=lambda x: x[1], reverse=True)[:max_len - 2]
    vocab_dic = {word[0]: idx for idx, word in enumerate(vocab_list)}
    vocab_dic.update({UNK: len(vocab_dic), PAD: len(vocab_dic) + 1})

    return vocab_dic

# Initialize reading data sets according to different modes.
class ClimateData(data.Dataset):
    NUM_CLASSES = 3
    def __init__(self, args, tokenizer, vocab, split='train'):
        self.texts = []
        self.labels = []
        self.args = args
        self.split = split
        self.vocab = vocab
        # output the data set in the form of text and label.
        if self.split == "train":
            with open(self.args.train_path, 'r',encoding="utf-8") as f:
                data = f.readlines()
            self.texts = []
            self.labels = []
            for each in data:
                m = each.split("\t")
                if (len(m) == 2):
                    if(len(m[1])<5) and "1" in m[1]:
                        self.texts.append(m[0])
                        self.labels.append(1)
                    if (len(m[1]) < 5) and "0" in m[1]:
                        self.texts.append(m[0])
                        self.labels.append(0)
                    if (len(m[1]) < 5) and "2" in m[1]:
                        self.texts.append(m[0])
                        self.labels.append(2)
            print(self.labels)
        elif self.split == "val":
            with open(self.args.val_path, 'r',encoding="utf-8") as f:
                data = f.readlines()
                self.texts = []
                self.labels = []
                for each in data:
                    m = each.split("\t")
                    if (len(m) == 2):
                        if (len(m[1]) < 5) and "1" in m[1]:
                            self.texts.append(m[0])
                            self.labels.append(1)
                        if (len(m[1]) < 5) and "0" in m[1]:
                            self.texts.append(m[0])
                            self.labels.append(0)
                        if (len(m[1]) < 5) and "2" in m[1]:
                            self.texts.append(m[0])
                            self.labels.append(2)
                print(self.texts[0:10])
                print(self.labels[0:10])
        elif self.split == "test":
            with open("predict.txt","r",encoding="utf-8") as f:
                content=f.read()
            self.texts = [content]
            self.labels = [3]
        else:
            raise Exception("No file for split %s" % self.split)

        assert len(self.texts) == len(self.labels)

        self.texts = [tokenizer.tokenize(text) for text in self.texts]
    
    def __len__(self):
        return len(self.texts)
    # Dataset output style.
    def __getitem__(self, index):
        _text = self.texts[index]
        _label = self.labels[index]

        sample = {'text': _text, 'label': _label}

        if self.split == 'train':
            return self.transform_tr(sample)
        elif self.split == 'val':
            return self.transform_val(sample)
        elif self.split == 'test':
            return self.transform_ts(sample)

    def transform(self, trans, sample):
        for obj in trans:
            sample = obj(sample)
        return sample

    #train
    def transform_tr(self, sample):
        trans = [
            tr.PadAndCut(self.args.max_len),
            tr.WordToId(self.vocab),
            tr.ToTensor()]
        return self.transform(trans, sample)
    #val
    def transform_val(self, sample):
        trans = [
            tr.PadAndCut(self.args.max_len),
            tr.WordToId(self.vocab),
            tr.ToTensor()]
        return self.transform(trans, sample)
    #test
    def transform_ts(self, sample):
        trans = [
            tr.PadAndCut(self.args.max_len),
            tr.WordToId(self.vocab),
            tr.ToTensor()]
        return self.transform(trans, sample)
