import random
from typing import *
from tqdm import tqdm
import os
import string

SUBSET_SENTENCE_CNT = 50000
TRAIN_SET_CNT = 40000
VALID_SET_CNT = 5000
TEST_SET_CNT = SUBSET_SENTENCE_CNT-TRAIN_SET_CNT-VALID_SET_CNT
MIN_CHAR_LEN = 200
MAX_CHAR_LEN = 2000

# def sample_sub_spoiler_set(sentence_cnt:int,seed:int=42)->List[dict]:
#     random.seed(seed)
#     path = f"./sampled_datasets/review_spoiler_dataset_l{sentence_cnt}_s{seed}.txt"
#     if os.path.exists(path):
#         res = list()
#         with open(path) as fin:
#             lines = fin.readlines()
#             for l in lines:
#                 res.append(eval(l))
#         return res
#     random.seed(seed)
#     res = list()
#     viewed_sample_cnt=0
#     with open("./goodreads_reviews_spoiler.json/goodreads_reviews_spoiler.json",encoding="utf-8") as fin:
#         lines = fin.readlines()
#         for line in tqdm(lines):
#             line = line.replace("true","True")
#             line = line.replace("false","False")
#             datum = eval(line)
#             book_id = datum['book_id']
#             rating = datum['rating']
#             for label,sentence in datum['review_sentences']:
#                 if len(sentence)<VALID_SENTENCE_LEN_IN_CHAR_THS:
#                     continue
#                 viewed_sample_cnt+=1
#                 if len(res)<sentence_cnt:
#                     d = dict()
#                     d["label"]=label
#                     d["review_sentence"]=sentence
#                     d["book_id"]=book_id
#                     d['rating']=rating
#                     res.append(d)
#                 else:
#                     i = random.randint(0,viewed_sample_cnt-1)
#                     if i<sentence_cnt:
#                         d = dict()
#                         d["label"]=label
#                         d["review_sentence"]=sentence
#                         d["book_id"]=book_id
#                         d['rating']=rating
#                         res[i]=d
#     with open(path,"w+") as fout:
#         for datum in res:
#             fout.write(repr(datum)+"\n")
#     return res

def sample_sub_spoiler_set(sentence_cnt:int,seed:int=42)->List[dict]:
    END_SENTENCE_TOKENS = string.punctuation
    random.seed(seed)
    path = f"./sampled_datasets/review_spoiler_dataset_l{sentence_cnt}_s{seed}.txt"
    if os.path.exists(path):
        res = list()
        with open(path) as fin:
            lines = fin.readlines()
            for l in lines:
                res.append(eval(l))
        return res
    random.seed(seed)
    res = list()
    viewed_sample_cnt=0
    with open("./goodreads_reviews_spoiler.json/goodreads_reviews_spoiler.json",encoding="utf-8") as fin:
        lines = fin.readlines()
        for line in tqdm(lines):
            should_append = len(res)<sentence_cnt
            should_replace = False
            replace_i = -1
            if not should_append:
                replace_i = random.randint(0,viewed_sample_cnt)
                should_replace = replace_i<sentence_cnt
            if not (should_append or should_replace):
                continue
            try:
                line = line.replace("true","True")
                line = line.replace("false","False")
                datum = eval(line)
                book_id = datum['book_id']
                rating = datum['rating']
                label = int(datum["has_spoiler"])
                review_paragraph=""
                for _lbl,sentence in datum['review_sentences']:
                    sentence = sentence.replace("\n"," ").replace("\t"," ")
                    sentence = sentence.strip()
                    if len(sentence)==0:
                        continue
                    if not sentence[-1] in END_SENTENCE_TOKENS:
                        sentence+="."
                    review_paragraph+=(sentence+" ")
                if MIN_CHAR_LEN<=len(review_paragraph)<=MAX_CHAR_LEN:
                    viewed_sample_cnt+=1
                else:
                    continue
                d = dict()
                d["label"]=label
                d["book_id"]=book_id
                d["rating"]=rating
                d["review_sentence"] = review_paragraph
                if should_append:
                    res.append(d)
                if should_replace:
                    res[replace_i]=d
            except BaseException as err:
                print(err)
    with open(path,"w+") as fout:
        for datum in res:
            fout.write(repr(datum)+"\n")
    return res

if __name__=="__main__":
    sample_sub_spoiler_set(SUBSET_SENTENCE_CNT)