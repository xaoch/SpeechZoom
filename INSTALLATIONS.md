#I - Speech-to-text recognition

1. Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the JSON file that contains the service account key.
example:
``export GOOGLE_APPLICATION_CREDENTIALS="/home/user/service-account-file.json"``

This variable only applies to your current shell session, so if you open a new session, set the variable again.

2. Install and initialize the Cloud SDK (https://cloud.google.com/sdk/docs)

3. install the client library:
``pip install --upgrade google-cloud-speech``


#II - Keywords extraction


##for RAKE mehod:

install nltk: ``pip install nltk``
rake-nltk: ``pip install rake-nltk``


##for EMBEDRANK method:
(steps taken from https://github.com/swisscom/ai-research-keyphrase-extraction)

First, download [this github repository](https://github.com/swisscom/ai-research-keyphrase-extraction)

1. Download full Stanford CoreNLP Tagger version 3.8.0
http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip

2. Install sent2vec from 
https://github.com/epfml/sent2vec
    * Clone/Download the directory
    * go to sent2vec directory
    * git checkout f827d014a473aa22b2fef28d9e29211d50808d48
    * make
    * pip install cython
    * inside the src folder 
        * ``python setup.py build_ext``
        * ``pip install . ``
        * (In OSX) If the setup.py throws an **error** (ignore warnings), open setup.py and add '-stdlib=libc++' in the compile_opts list.        
    * Download a pre-trained model (see readme of Sent2Vec repo) , for example wiki_bigrams.bin
    
3. Install requirements:
    
    pip install langdetect==1.0.7
    pip install nltk==3.4.1
    pip install numpy==1.14.3
    pip install scikit-learn==0.19.0
    pip install scipy==0.19.1
    pip install six==1.10.0
    pip install requests==2.21.0

4. Download NLTK data
```
import nltk 
nltk.download('punkt')
```

5. Launch Stanford Core NLP tagger
    * Open a new terminal
    * Go to the stanford-core-nlp-full directory
    * Run the server `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos -status_port 9000 -port 9000 -timeout 15000 & `


6. Set the paths in config.ini.template
    * You can leave [STANFORDTAGGER] parameters empty
    * For [STANFORDCORENLPTAGGER] :
        * set host to localhost
        * set port to 9000
    * For [SENT2VEC]:
        * set your model_path to the pretrained model
        your_path_to_model/wiki_bigrams.bin (if you choosed wiki_bigrams.bin)
    * rename config.ini.template to config.ini


##for SIFRANK method:
(steps taken from https://github.com/sunyilgdx/SIFRank)

First, download [this github repository](https://github.com/sunyilgdx/SIFRank)

* download ELMo ``elmo_2x4096_512_2048cnn_2xhighway_options.json`` and ``elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5`` from [here](https://allennlp.org/elmo) , and save it to the ``auxiliary_data/`` directory
* download StanfordCoreNLP ``stanford-corenlp-full-2018-02-27`` from [here](https://stanfordnlp.github.io/CoreNLP/), and save it to anywhere