# install and import libraries
from collections import Counter, defaultdict
from transformers import AutoTokenizer
import json
#from autonotebook import tqdm as notebook_tqdm

inter_eojeol = '▁'  # unicode : U+2581 org : _ 
intra_eojeol = '⧾'  # unicode : U+29FE org : +

class MoB():
    """Byte-Pair Encoding: Subword-based tokenization algorithm. prefix(_) for non-first char and prefix(+) for following morpheme"""
    def __init__(self, corpus, vocab_size):
        """Initialize BPE tokenizer."""
        self.corpus = corpus
        self.vocab_size = vocab_size
        
        # pre-tokenize the corpus into words, BERT pre-tokenizer is used here
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.word_freqs = defaultdict(int)
        self.splits = {}
        self.merges = {}
        self.vocab = []

    def load_merge(self,f_path):
        with open(f"{f_path}", "r") as file:
            load_data = json.load(file)
            self.merges = {eval(key): value for key, value in load_data.items()}

    def load_vocab(self,f_path):
        load_file = open(f"{f_path}", "r").readlines()
        for line in load_file:
            line = line.strip()
            self.vocab.append(line)

    def train(self):
        """Train BPE tokenizer."""

        # compute the frequencies of each word in the corpus
        for text in self.corpus:
            words_with_offsets = self.tokenizer.backend_tokenizer.pre_tokenizer.pre_tokenize_str(text)
            new_words = [word for word, offset in words_with_offsets]
# Mb code   
            new_words_mb = []
            prefix = ''
            for word in new_words:
                if word == intra_eojeol or word == inter_eojeol:
                    prefix = word
                    continue
                if prefix == intra_eojeol or prefix == inter_eojeol:
                    word = prefix + word
                    prefix = ''
#                else :
#                    word = inter_eojeol + word
                new_words_mb.append(word)
            new_words = new_words_mb
#           print("new_words:", new_words)
##
            
            for word in new_words:
                self.word_freqs[word] += 1
## Mb code
#        print("word_freqs:", self.word_freqs)
##
        
        # compute the base vocabulary of all characters in the corpus
        alphabet = []
        for word in self.word_freqs.keys():
            firstLetter = True
            for letter in word:
## Mb code
                if letter == intra_eojeol or letter == inter_eojeol:
                    prefix = letter
                    continue
                if prefix == intra_eojeol or prefix == inter_eojeol:
                    letter = prefix+letter
                    prefix = ''
                elif not firstLetter:
                    letter = inter_eojeol + letter
                firstLetter = False
##
                
                if letter not in alphabet:
                    alphabet.append(letter)
        alphabet.sort()

        # add the special token </w> at the beginning of the vocabulary
        self.vocab = ["[PAD]","[UNK]","[CLS]","[SEP]","[MASK]"] + alphabet.copy()
        # split each word into individual characters before training
## Mb code
#        self.splits = {word: [c for c in word] for word in self.word_freqs.keys()}
        for word in self.word_freqs.keys():
            c_list=[]
            prefix = ''
            firstLetter = True
            for c in word:
                if c == intra_eojeol or c == inter_eojeol:
                    prefix = c
                    continue
                if prefix == intra_eojeol or prefix == inter_eojeol:
                    c = prefix + c
                    prefix = ''
                elif not firstLetter:
                    c = inter_eojeol + c
                    
                firstLetter = False
                c_list.append(c)
            self.splits[word] = c_list

#        print("splits:", self.splits)
##        
        # merge the most frequent pair iteratively until the vocabulary size is reached
        while len(self.vocab) < self.vocab_size:

            # compute the frequency of each pair
            pair_freqs = self.compute_pair_freqs()

            # find the most frequent pair
            best_pair = ""
            max_freq = None
            for pair, freq in pair_freqs.items():
                if max_freq is None or max_freq < freq:
                    best_pair = pair
                    max_freq = freq

            # merge the most frequent pair
            self.splits = self.merge_pair(*best_pair)
            merge = best_pair[0] + (best_pair[1][1:] if best_pair[1][0] == inter_eojeol else best_pair[1])
            self.merges[best_pair] = merge
            self.vocab.append(merge)
        self.save_vocab()
        self.save_merge()
        return self.merges


    def compute_pair_freqs(self):
        """Compute the frequency of each pair."""

        pair_freqs = defaultdict(int)
        for word, freq in self.word_freqs.items():
            split = self.splits[word]
            if len(split) == 1:
                continue

            for i in range(len(split) - 1):
## Mb code
                if split[i+1][0] == intra_eojeol :
                    continue
##
                pair = (split[i], split[i + 1])
                pair_freqs[pair] += freq
        return pair_freqs


    def merge_pair(self, a, b):
        """Merge the given pair."""
## Mb code
        if b[0] == intra_eojeol:
            return self.splits
##
        for word in self.word_freqs:
            split = self.splits[word]
            if len(split) == 1:
                continue
            i = 0
            while i < len(split) - 1:
                if split[i] == a and split[i + 1] == b:
                    merge = a + (b[1:] if b[0] == inter_eojeol else b)
                    split = split[:i] + [merge] + split[i + 2 :]
                else:
                    i += 1
            self.splits[word] = split
        return self.splits
    

    def tokenize(self, text):
        """Tokenize a given text with trained BPE tokenizer (including pre-tokenization, split, and merge)."""
        
        pre_tokenize_result = self.tokenizer._tokenizer.pre_tokenizer.pre_tokenize_str(text)
        pre_tokenized_text = [word for word, offset in pre_tokenize_result]

# Mb code   
        new_words_mb = []
        prefix = ''
        for word in pre_tokenized_text:
            if word == intra_eojeol or word == inter_eojeol:
                prefix = word
                continue
            if prefix == intra_eojeol or prefix == inter_eojeol:
                word = prefix + word
                prefix = ''
#            else:
#                word = inter_eojeol + word
            new_words_mb.append(word)
            pre_tokenized_text = new_words_mb
##
        

## Mb code
#        splits_text = [[l for l in word] for word in pre_tokenized_text]

        splits_text = []
        for word in pre_tokenized_text:
            c_list=[]
            prefix = ''
            firstLetter = True
            for c in word:
                if c == intra_eojeol :
                    prefix = c
                    continue
                if prefix == intra_eojeol :
                    c = prefix + c
                    prefix = ''
                elif not firstLetter:
                    c = inter_eojeol + c
                firstLetter = False
                c_list.append(c)
            splits_text.append(c_list)
##  


        for pair, merge in self.merges.items():
## Mb code
            if pair[1][0] == intra_eojeol :
                continue
##
            for idx, split in enumerate(splits_text):
                i = 0
                while i < len(split) - 1:
                    if split[i] == pair[0] and split[i + 1] == pair[1]:
                        split = split[:i] + [merge] + split[i + 2 :]
                    else:
                        i += 1
                splits_text[idx] = split
        result = sum(splits_text, [])
        return result

    def save_merge(self):
        tp_to_str = {str(key): value for key, value in self.merges.items()}
        with open('merge.json', 'w') as f:
            json.dump(tp_to_str, f, indent=4,ensure_ascii=False)

    def save_vocab(self):
        sf = open('vocab.txt','w')
        for word in self.vocab:
            sf.write(word+'\n')
    def token_to_id(self, token : str):
        try:
            self.vocab.index(token)
            return self.vocab.index(token)
        except:
            return self.vocab.index('[UNK]')

    def tokens_to_ids(self, tokens: list):
        return [self.token_to_id(each) for each in tokens]

    def id_to_token(self, tid : int):
        if 0<=tid and tid<len(self.vocab):
            return self.vocab[tid]

    def ids_to_tokens(self, tids : list):
        return [self.id_to_token(tid) for tid in tids]
