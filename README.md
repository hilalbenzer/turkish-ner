# Turkish NER

A Named Entity Recognition tool for Turkish.

### Running Web App

1. Clone the project to local
2. `cd turkish-ner`
3. `python3 web.py`

### Prerequisites

1. Python 3
2. ```scikit-learn```
3. ```gensim```
4. ```bottle```

Or to install python3 packages

1. Python 3
2. ```pip3```

``` pip3 install -r requirements.txt ```

### Usage

To run console application

``` python3 src/find_named_entitites.py <input_file> <output_file>```

* ```<input_file>``` containing Turkish sentences
* Note that sentences should be on separate lines
* ```<output_file``` is the output file of the program, containing NER tagged version of sentences

To create a new model

``` python3 src/create_model.py ```
* Corpora not available on repository due to size

To run the tests

``` python3 src/test.py ```
