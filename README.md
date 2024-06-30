# Extension for UNSC with Sentiment Scores per Debate and per Speech  

Compute sentiment scores for UN Security Council debates and speeches, based on the corpus by Schoenfeld et al. 2019: 

## Prepare Corpus
### For Lexicoder sentiment analysis:
- Download the the Lexicoder Sentiment Dictionary ("LSDaug2015") from: https://www.snsoroka.com/data-lexicoder/
- Unzip LSDaug2015.zip in /lexicoder_UNSC: `$unzip LDSDaug2015.zip -d ./lexicoder_UNSC`
- Run `$python make_lstable.py` to prepare the lexicon for further processing (eventually update paths in config.ini)

### Prepare UNSC Corpus
If you want to use the full corpus by Schoenfeld et al. 2019:
1. Download the original "UN Security Council Debates" corpus from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/KGVSYH
(Schoenfeld et al. 2019) containing all debates. 
2. Unzip directory ``dataverse_files.zip`` and extract subdirectiory ``speeches.tar``. 
3. Copy ``dataverse_files`` into ``/data`` project folder. 
The projectstructure should look like the following:
```
- /UNSC_subcorpus_creation
-- /data
---- /dataverse_files <--original UNSC corpus dirname
------ speaker.tsv
------ meta.tsv
------ /speeches
------------UNSC_2013_SPV.6990_spch001.txt
------------UNSC_2013_SPV.6990_spch002.txt
------------...
-- /output
-- create_subcorpus.py
-- config.ini
```

If you want to use your own subcorpus, under `\data` you need a folder with:
1. The speeches-dir containing speeches txt files
2. subcorpus meta.tsv
3. subcorpus speeches.tsv
4. Please redefine your paths in `config.ini`

## Compute Lexicoder sentiment scores
Run:   
```$cd code```  
```$python analyze:speeches_lexicoder.py```

The new tables with lexicoder-based sentiment scores per debate (`meta_subcorpus_sc.tsv`) and per speech (`speeches_subcorpus_sc.tsv`) are saved under `/output`.

