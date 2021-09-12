import torch
import numpy as np
import json
from config import Options
from dataloaders import make_data_loader
from train import train, init_network, evaluate, inference
from config import DEVICE


def main():
    args = Options().parse()# Read training parameters and model settings.
    # Set random seeds to ensure consistent results.
    np.random.seed(1)
    torch.manual_seed(1)
    torch.cuda.manual_seed_all(1)
    torch.backends.cudnn.deterministic = True
    # Load dataset.
    print("Loading data...")
    vocab, train_loader, val_loader, test_loader, num_class = make_data_loader(args)
    vocab_size = len(vocab)
    # select training model.
    if args.model == "FastText":
        from models.FastText import FastText, Config
        config = Config()
        model = FastText(config, vocab_size, 3)
    model.to(DEVICE)
    # select mode.
    if args.mode == "train":
        init_network(model)
        train(args, model, train_loader, val_loader)
    elif args.mode == "inference":
        model.load_state_dict(torch.load(args.model + '.ckpt'))
        y_preds = inference(args, model, test_loader)
        print(y_preds)

if __name__ == '__main__':
    main()