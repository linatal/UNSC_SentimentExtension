import os
import argparse
from pathlib import Path
import configparser
import pandas as pd
import numpy as np
import shutil

def read_each_file(speeches_folder):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # manage paths in config file
    config = configparser.ConfigParser()
    #config.read("config.ini") # CHANGE
    config.read("config_temp.ini")

    meta_path = config["DATA_INPUT"]["meta_table"]
    speaker_path = config["DATA_INPUT"]["speaker_table"]
    speeches_folder = config["DATA_INPUT"]["corpus_raw_dir"]
    df_meta = pd.read_csv(meta_path, sep="\t")
    df_speech = pd.read_csv(speaker_path, sep="\t")

    read_each_file(speeches_folder)

