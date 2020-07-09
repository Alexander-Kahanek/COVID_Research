# Twitter COVID-19 dataset building

This is where the dataset will be built, you can use `python3 build_dataset.py` 
to run through all the scripts that take decompressed json files to filter the tweeets, 
run them through flair and spaCy, and output them to a final csv file. More information 
on each script can be found within the `/scripts/` folder.


# Dependencies

These are the packages that are required for build_dataset.py

* Python >= 3.8.0
* pandas
* tweet-preprocessor
* flair
* torch >= 1.4
* spacy
