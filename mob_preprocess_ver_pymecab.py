import argparse
import json
import os
import time
from functools import partial
from multiprocessing import Pool
from typing import List
from mecab import MeCab
import re

intra_eojeol = '⧾'  # unicode : U+29FE (Intra-Eojeol)
space = '▃'  # unicode : U+2583 (Space)

def is_kr(text : str):
    return bool(re.search(r'[가-힣ᄀ-ᇿㄱ-ㅣ]', text))

def add_intra_eojeol(text : list):
    result = []
    intra_ej_flag = False
    for idx,word in enumerate(text):
        prev_word = text[idx-1]
        if word == space:
            intra_ej_flag = False
            continue
        if intra_ej_flag and is_kr(word) and is_kr(prev_word):
            result.append(intra_eojeol+word)
        else:
            result.append(word)
            intra_ej_flag = True
    return result

def mob_preprocess(text: str, space_symbol: str = space) -> List[str]: 
    mecab = MeCab() #Morpheme Analyzer
    text = text.strip()
    text_ptr = 0
    preprocess_result = []
# Example
# input : 귀여운
# return : Morpheme(span=Span(start=0, end=3), surface='귀여운', feature=Feature(pos='VA+ETM', semantic=None, has_jongseong=True, reading='귀여운', type='Inflect', start_pos='VA', end_pos='ETM', expression='귀엽/VA/*+ᆫ/ETM/*'))
# ㄴ composable 설명필요!!!
    for morph in mecab.parse(text):
        surface = morph.surface
        morpheme_restoration = morph.feature.expression
        morphemes = ''

        if text[text_ptr] == " ": # Because Mecab-ko removes space, Mark original space by using space_symbol.
            while text[text_ptr] == " ":
                text_ptr += 1
            assert text[text_ptr] == surface[0]
            preprocess_result.append(space_symbol)
        text_ptr += len(surface)

        if morpheme_restoration != None : # If morpheme restoration is conducted.
            restored_morphemes = morpheme_restoration.split('+') # restored morphemes
            restored_morpheme_cnt = len(restored_morphemes) # restored morpheme count
            for i in range(restored_morpheme_cnt):
                morphemes = restored_morphemes[i].split('/')[0]
                preprocess_result.append(morphemes)
        else : # If morpheme doesn't need to restore.
            morphemes = surface
            preprocess_result.append(morphemes)
    return preprocess_result
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--output", type=str)
    parser.add_argument("--n_jobs", type=int, default=20)
    args = vars(parser.parse_args())
    print(args)
    INPUT_DIR = args["dataset"]
    OUTPUT_DIR = args["output"]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    listdirs = os.listdir(INPUT_DIR)
    # set tokenizing func
    preprocess_fn = partial(mob_preprocess, space_symbol=space)

    start_time = time.time()
    print(f"Start preprocessing for MoB ...")
    for f_name in listdirs:
        with open(INPUT_DIR+'/'+f_name, "r", encoding="utf-8") as f:
            with Pool(args["n_jobs"]) as p:
                mecab_result = p.map(preprocess_fn, f)
    # mecab preprocess
        with open(OUTPUT_DIR+"/"+"mob_preprocess_"+f_name, "w", encoding="utf-8") as f:
            for token in mecab_result:
                result = add_intra_eojeol(token)
                f.write(" ".join(result).replace(" "+intra_eojeol, intra_eojeol) + "\n")

    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    print(f"Complete for preprocess. (elapsed time: {elapsed_time})")
