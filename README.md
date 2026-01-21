![EACL](./img/EACL2026_logo_website-high-res.png)
# Morpheme Matters: Morpheme-Based Subword Tokenization for Korean Language Models 
> **Authors** : [Donghyeok Lee](http://github.com/Dohy-Lee), [Jeongyeon Park](https://github.com/Jeongyeon0), [Kyungbeen Cho](https://github.com/kyungbeen-nlp), [Jae Sung Lee](https://scholar.google.com/citations?user=mYKw_7oAAAAJ&hl=ko)† <br>
> († indicates Corresponding Author) <br>
> 🎉 Accepted to EACL 2026 (Main Conference) <br>
> Download : [PDF](http://google.com)

> **Abstract** : Tokenization plays a crucial role in the performance of language models.
> However, most existing tokenizers rely on frequency-based segmentation, which fails to capture the morphological structure of languages and often leads to inefficient token representations.<br> In this study, we propose a novel tokenization method that emphasizes the importance of Korean morphological structures in ___eojeol___ (Korean spacing unit). This method is designed to accommodate both inter-___eojeol___ segmentation and intra-___eojeol___ segmentation, enabling the selection of subwords based on morphemes.<br>
> We pretrained a language model using the proposed method and evaluated its performance on Korean benchmark tasks. Experimental results demonstrate that the proposed method generally outperforms existing approaches. Notably, it produces significantly fewer tokens per input sequence, indicating its effectiveness and efficiency for Korean language modeling.

> **⚠️Note**: In our experiments, we used the original `Mecab-ko (C/C++)`. To assist users who may face difficulties installing the C++ version, we provide a `python-mecab-ko` version along with a `uv` environment configuration.<br>
> Please be aware that since the MoB code is implemented in Python, it may exhibit slower processing speeds compared to tokenizers highly optimized in C++, such as SentencePiece.

## Result
<div align="center">
<table><thead>
  <tr>
    <th></th>
    <th colspan="2">KorQuAD</th>
    <th>KorSTS</th>
    <th>KorNLI</th>
    <th>NSMC</th>
    <th>PAWS-X</th>
  </tr></thead>
<tbody>
  <tr>
    <td>Tokenizer</td>
    <td>EM</td>
    <td>F1</td>
    <td>$\rho$</td>
    <td>Acc</td>
    <td>Acc</td>
    <td>Acc</td>
  </tr>
  <tr>
    <td>BPE</td>
    <td>49.72 ±0.31</td>
    <td>65.07 ±0.35</td>
    <td>63.00 ±0.77</td>
    <td>64.47 ±0.39</td>
    <td>85.04 ±0.04</td>
    <td>61.11 ±0.82</td>
  </tr>
  <tr>
    <td>MoA</td>
    <td>50.25 ±0.57</td>
    <td>66.35 ±0.46</td>
    <td>68.30 ±0.74</td>
    <td>67.32 ±0.18</td>
    <td><b>86.07 ±0.08</b></td>
    <td>59.20 ±2.57</td>
  </tr>
  <tr>
    <td>MoB</td>
    <td><b>51.65 ±0.38</b></td>
    <td><b>69.33 ±0.14</b></td>
    <td><b>69.53 ±0.60</b></td>
    <td><b>68.61 ±0.22</b></td>
    <td><b>85.73 ±0.07</b></td>
    <td><b>62.66 ±0.89</b></td>
  </tr>
</tbody>
</table>
</div>

**Table 1. Performance of BPE, MoA, and MoB tokenizers. Values are mean ± standard deviation. KorQuAD is evaluated on the dev set due to the unavailability of a public test set, while KorSTS, KorNLI, NSMC, and PAWS-X are evaluated on their respective test sets. KorSTS is reported as Spearman correlation ($\rho \times$ 100), and KorNLI, NSMC, and PAWS-X are reported as Accuracy (%).**

<div align="center">
<table><thead>
  <tr>
    <th rowspan="2">Dataset</th>
    <th colspan="3">Number of Token Types</th>
    <th colspan="3">Number of Token Instances</th>
  </tr>
  <tr>
    <th>MoA</th>
    <th>MoB</th>
    <th>$\Delta$</th>
    <th>MoA</th>
    <th>MoB</th>
    <th>$\Delta$</th>
  </tr></thead>
<tbody>
  <tr>
    <td>KorQuAD</td>
    <td>14,551</td>
    <td>13,183</td>
    <td><b>91%</b></td>
    <td>430.53</td>
    <td>340.13</td>
    <td><b>79%</b></td>
  </tr>
  <tr>
    <td>KorSTS</td>
    <td>5,795</td>
    <td>5,499</td>
    <td><b>95%</b></td>
    <td>52.26</td>
    <td>41.00</td>
    <td><b>78%</b></td>
  </tr>
  <tr>
    <td>KorNLI</td>
    <td>5,592</td>
    <td>5,159</td>
    <td><b>92%</b></td>
    <td>60.76</td>
    <td>48.18</td>
    <td><b>79%</b></td>
  </tr>
  <tr>
    <td>NSMC</td>
    <td>10,445</td>
    <td>10,377</td>
    <td><b>99%</b></td>
    <td>28.18</td>
    <td>23.97</td>
    <td><b>85%</b></td>
  </tr>
  <tr>
    <td>PAWS-X</td>
    <td>6,391</td>
    <td>5,901</td>
    <td><b>92%</b></td>
    <td>90.60</td>
    <td>77.35</td>
    <td><b>85%</b></td>
  </tr>
  <tr>
    <td><b>Average</b></td>
    <td>8,555</td>
    <td>8,024</td>
    <td><b>94%</b></td>
    <td>132.07</td>
    <td>106.13</td>
    <td><b>81%</b></td>
  </tr>
</tbody></table>
</div>

**Table 2. Comparison of the size of token types and instances. The number of token types denotes the total number of unique tokens observed in the dataset, and the  number of token instances denotes the average frequency with which a given token appears within a single input sequence. $\Delta$ is calculated as (MoB/MoA) $\times$ 100.** 

We evaluate and compare the performance of BPE, Morpheme-Aware Subword Tokenization[(MoA)](https://github.com/kakaobrain/kortok) and Morpheme-Based Subword Tokenization(MoB).

**Table 1** presents the fine-tuning performance on the five downstream tasks. MoB outperformed MoA on all tasks, with the exception of NSMC. For NSMC, MoB method showed slightly lower performance than MoA. The NSMC dataset showed a different trend, which we attribute to its nature as an online corpus containing numerous neologisms, abbreviations, and typographical errors, making it difficult for the morphological analyzer to produce accurate analyses. A more detailed error analysis is provided in [Appendix A.2 of our paper](url).

**Table 2** summarizes the number of unique token types and the average number of tokens per input sequence generated by each tokenization method. MoB yielded on average 6 percentage fewer token types than MoA across all development datasets. This reduction in token variety indicates that MoB achieves more efficient vocabulary compression by grouping morphologically different but semantically equivalent word forms into a single token through morpheme restoration.
Furthermore, the average number of token instances per input sequence was about 19 percentage lower for MoB than for MoA across all tasks. This outcome can be attributed to MoB's design, which avoids inserting an ___eojeol___ boundary token. Instead, MoB employs the inter-___eojeol___ prefix and intra-___eojeol___ prefix to denote both the ___eojeol___ and morpheme boundaries directly within existing tokens.

## Prerequisites
- **Python-mecab-ko(or Mecab-ko)**
- **Python ≥ 3.11**
- **Transformers ≥ 4.57.3**
  
## Pre-training
> For pretraining, we utilized the implementation from [BERT-pytorch](https://github.com/codertimo/BERT-pytorch). The model was trained on a subset of the [AI-Hub dataset](https://www.aihub.or.kr)(3.7GB) and [Wikipedia dumps](https://dumps.wikimedia.org/kowiki/)(780MB). 

## Fine-tuning
> For fine-tuning, we adapted the source code from Morpheme-Aware Subword Tokenization[(MoA)](https://github.com/kakaobrain/kortok).


## How To Use
> **0. Setting**
> ```bash
> 1. git clone https://github.com/Dohy-Lee/mob.git
> 2. uv sync

> **1. Preprocess**
> ```bash
> uv run python mob_preprocess_ver_pymecab.py --dataset [your folder with corpus] --output [your folder]
> (If you install 'mecab-ko', 'mob_preprocess_ver_mecab.py' instead of mob_preprocess_ver_pymecab.py)
 
> **2. Consturct Vocabulary**
> ```bash
> uv run python vocab_construction.py --dataset [your folder with preprocessed corpus] --size [vocab size]

> **3. Run MoB Tokenizer**
> ```bash
> uv run python tokenize_by_mob.py --vocab vocab.txt --merge merge.json

## Citation
If you find our work useful, please cite it using the follwoing BibTex:
```bibtex
@inproceedings{
  lee2026morpheme,
  title={Morpheme Matters: Morpheme-Based Subword Tokenization for Korean Language Models},
  author={DongHyeok Lee and Jeongyeon Park and Kyungbeen Cho and Jae Sung Lee},
  booktitle={19th Conference of the European Chapter of the Association for Computational Linguistics},
  year={2026},
  url={https://openreview.net/forum?id=iqzcpbIsx1}
}
