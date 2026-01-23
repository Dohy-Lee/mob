from mob import *
import sys
import argparse
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vocab",type=str,help="Input vocab.txt by vocab_construction.py")
    parser.add_argument("--merge",type=str,help="Input merg.json by vocab_construction.py")
    args = parser.parse_args()
    args = vars(args)
    vocab_size = len(open(args['vocab'],'r').readlines())
    mob = MoB([], vocab_size)

    # 학습 결과 불러오기
    mob.load_vocab(args['vocab'])
    mob.load_merge(args['merge'])

    # 토크나이즈할 문장
    text_line = "새롭⧾ᆫ 마을⧾에서 맞⧾는 새롭⧾ᆫ 노을⧾은 감회⧾가 새롭⧾다 ."

    tokens = mob.tokenize(text_line)
    print("[Input Text]")
    print(text_line)
    print("\n[Tokenized Result]")
    for i, tk in enumerate(tokens):
        print(f"[{i}] {tk}")

    # 토큰 → ID 변환
    ids = mob.tokens_to_ids(tokens)
    print("\n[Token Ids]")
    print(ids)
    
    tokens = mob.ids_to_tokens(ids)
    print("\n[Token Ids -> Token]")
    print(tokens)
if __name__ == "__main__":
    main()

