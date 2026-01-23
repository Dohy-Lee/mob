from mob import *
import os
import time
import argparse

def load_corpus(path):
    dirs = os.listdir(path)
    corpus=[]
    for f_name in dirs:
        with open(path+'/'+f_name,'r') as f:
            for line in f.readlines():
                line = line.strip()
                corpus.append(line)
        return corpus

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset",type=str,help="Folder with Corpus")
    parser.add_argument("--size",type=int,help="Vocabulary Size")
    args = parser.parse_args()
    args = vars(args)
    corpus = load_corpus(args['dataset'])
    mob = MoB(corpus, args['size'])
    print("Training MoB...")
    start_time = time.time()
    mob.train()
    end_time = time.time()
    print(f"\nTotal Time: {end_time - start_time:.4f} seconds")
    print("Training done.")


if __name__ == "__main__":
    main()
