import configparser
import pandas as pd
import glob
import os
import re
from pathlib import Path

def create_score_each_file(speeches_folder, lexicoder_data):
    list_fullpath = glob.glob(speeches_folder+"/*.txt")
    list_filename = [os.path.basename(x) for x in list_fullpath]
    pol_word_list = []
    score_list = []
    for f in list_fullpath:
        x = open(f).read()
        x_prepr = preprocess(x)
        #find_sentiment_entries(x_prepr, lexicoder_data)
        # calculate sentiment score for each speech
        line_preprocessed, out_entries = find_sentiment_entries(x_prepr, lexicoder_data)
        pol_words, score = calc_sentiment_score(line_preprocessed, out_entries)
        pol_word_list.append(pol_words)
        score_list.append(score)
        # dict with filename
    assert len(list_fullpath) == len(score_list)
    fn_score_dict = dict(zip(list_filename, score_list))
    return fn_score_dict

def sort_dict_according2list(list_from_orig_df, dict_to_sort):
    index_map = {v:i for i, v in enumerate(list_from_orig_df)}
    dict_sorted = sorted(dict_to_sort.items(), key=lambda pair: index_map[pair[0]])
    return dict_sorted


def append_score_table(df_speech, df_debate, fn_score_dict):
    # sort dictionary based on df.filename, creating first an index map
    list_df_fn = df_speech["filename"].to_list()
    #fn_score_dict_sorted = sorted(fn_score_dict.items(), key=lambda pair: list_df_fn.index(pair[0]))
    assert len(list_df_fn) == len(fn_score_dict)
    fn_score_dict_sorted = sort_dict_according2list(list_df_fn, fn_score_dict)
    df_speech["lexicoder_score"] = [x[1] for x in fn_score_dict_sorted]
    # TODO: mittelwert aus allen speeches für debate
    basename_list = list(set(df_speech["basename"].to_list()))
    debates_dict = {}
    for bn in basename_list:
        df_bn = df_speech[df_speech["basename"] == bn]
        summi = df_bn["lexicoder_score"].mean()
        debates_dict[bn] = summi
    assert len(df_debate["basename"].to_list()) == len(debates_dict)
    debate_score_dict_sorted = sort_dict_according2list(df_debate["basename"].to_list(), debates_dict)
    df_debate["lexicoder_score"] = [x[1] for x in debate_score_dict_sorted]
    return df_speech, df_debate




def preprocess(text: str):
    """Remove punctuation, transform to lower case."""
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text


def find_sentiment_entries(string, LEXICODER_data):
    """Get the sentiment words in a input string.
    Check the words in the string that are contained in the sentiment dictionary.
    Return the string and the words and their polarity.
    The polarities are negative|positive|neg_negative|neg_positive.
    input: input string, lsd.tsv
    return: string preprocessed and their polarities
    """
    df_lsd = pd.read_csv(LEXICODER_data, sep="\t")
    out_entries = []
    string_pp = preprocess(string)
    string_pp_separated = string_pp.split()

    for row in df_lsd.values:
        entry = row.tolist()
        # lex entry is single token
        if entry[1] == 1:
            # lex entry is not a prefix
            if entry[2] == 0:
                out_entries.extend([(entry[0], entry[3]) for t in string_pp_separated if entry[0] == t])
            else:
            # if lex entry is a prefix
                out_entries.extend([(entry[0], entry[3]) for t in string_pp_separated if t.startswith(entry[0])])
        else:
            # lex entry is not a prefix
            if entry[2] == 0:
                pattern_in_sent = entry[0] + " "
                out_entries.extend([(entry[0], entry[3]) for i in range((len(string_pp.split(pattern_in_sent)) - 1))])
                if string_pp.endswith(entry[0]):
                    out_entries.append((entry[0], entry[3]))
                else:
                    out_entries.extend([(entry[0], entry[3]) for i in range((len(string_pp.split(entry[0])) - 1))])
    return string_pp, out_entries

def calc_sentiment_score(sentence: str, pol_words):
    """Calculate the sentiment score of a sentence.
    The score is in [-1,1] and score = (n_positive_words - n_negative_words) / n_words.
    input: input string, words and their polarities or just polarites
    return: sentiment score
    """
    neg = sum([1 for t in pol_words if "negative" in t])
    neg_neg = sum([1 for t in pol_words if "neg_negative" in t])
    pos = sum([1 for t in pol_words if "positive" in t])
    neg_pos = sum([1 for t in pol_words if "neg_positive" in t])
    pos = pos - neg_pos + neg_neg
    neg = neg - neg_neg + neg_pos
    score = pos - neg
    if score != 0:
        score = score / len(sentence.split())
    return pol_words, score


if __name__ == '__main__':
    #cwd = os.getcwd()
    #print(cwd)
    # manage paths in config file
    config = configparser.ConfigParser()
    #config.read("config.ini") # CHANGE
    config.read("../config_temp.ini")

    meta_path = config["DATA_INPUT"]["meta_table"]
    speaker_path = config["DATA_INPUT"]["speaker_table"]
    speeches_folder = config["DATA_INPUT"]["corpus_raw_dir"]
    lexicoder_data = config["LEXICODER"]["LSD"]
    output_dir = config["DATA_OUTPUT"]["output_dir"]
    #prepare dataframes
    df_meta = pd.read_csv(meta_path, sep="\t")
    df_speech = pd.read_csv(speaker_path, sep="\t")
    df_meta = df_meta.rename(columns={"Unnamed: 0":"old_idx"})
    df_speech = df_speech.rename(columns={"Unnamed: 0":"old_idx"})

    fn_score_dict = create_score_each_file(speeches_folder, lexicoder_data)
    df_speech_sc, df_debate_sc = append_score_table(df_speech, df_meta, fn_score_dict)

    # check if output path exists, if not create
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    df_speech_sc.to_csv(output_dir+"/speeches_subcorpus_sc.tsv", sep="\t", index=False)
    df_debate_sc.to_csv(output_dir+"/meta_subcorpus_sc.tsv", sep="\t", index=False)



