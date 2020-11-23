# -*- coding: utf-8 -*-
"""RNN-Sentiment Analysis with IMDb Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hc_43Vo5xAkKKnHKyjVFC0uGy8eHVsm0

# Introduction

Sentiment analysis- Positive or Negative ->Binary classification problem. IMDb-->Movie reviews dataset.  Recurrent NN --process sequences of data --Natural Language processing. (NLP)

1.   Time series
2.   Text in sentences

Recurrent -- the NN contains loops -output of a given layer becomes the input to the same layer in the next time step. The time step  --Next point in time for a time series, or the next word in a sequence of words for text sequence

1.   Loops in RNNs help them to learn relationships among data in the sequence.

*   Good-- on its own has a positive sentiment
*   Not good has a negative sentiment, Not is earlier in the sequence.

RNNs do consider the relationships among earlier and later data in the sequence.Here the words that determine sentiment are adjacent. But when considering texts meaning there can be many words to consider and an arbitrary number of words between them. 
Long Short-Term Memory(LSTM)-- layer that makes the neural network recurrent.

1.   predictive text input
2.   sentiment analysis
3.   responding to questions with predicted best answers.
4.   Inter-language translation
5.   Automated video closed captioning --speech recognition
6.   Speech synthesis

### Loading the IMDb Movie Review Dataset
"""

pip install tensorflow

from tensorflow.keras.datasets import imdb

"""88,000 unique works, in the dataset, you can specify the number of unique words to import-- training and testing data. 

*   Usually 10,000 most frequently occuring words are used.
*   Due system memory limitations and training on cpu.--GPU...TPUS--The more the data longer it takes to train-- may producebetter models

### Loading data
"""

# Load_data replaces any words outside the 10,000 with a palceholder 
number_of_words=10000

import tensorflow as tf

tf.__version__

import numpy as np

"""Save the np.load"""

np_load_old=np.load

"""Modify the default parameters of the np.load"""

np.load=lambda *a,**k: np_load_old(*a, allow_pickle=True)

(x_train,y_train), (x_test,y_test) =imdb.load_data(num_words=number_of_words)

x_train

"""x_test and x_train appear as one dimension --Numpy arrays of objects(List of integer)"""

x_train.shape

y_train.shape

y_test.shape

"""### Data Exploration

The arrays y_train and y_test - 1D with 0s(Negative) and 1s(Positive). The x_train and x_test are list of integersw each representing one's review's contents. Keras models require numeric data-- IMDb dataset is preprocessed for you.
"""

# Commented out IPython magic to ensure Python compatibility.
# %pprint #toggle better printing, so that the elements do not display vertically

x_train[123]

"""To view the original text you need to know the word to which each number corresnponds to. The keras dictionary --provides the dic that maps words to their indexes. Each words value is its frequency occuring word...... For example randing 1 --frequently occuring in that dataset. The training and testing data have an offest of 3. (1+3) =4 --, most frequently word has a value of 4. The values 0,1 and 2 = reserved words.

1.   padding(0)-- all the training/testing must have some dimensions. Some reviews may need to be padded with a 0 and some shortened.
2.   Start of the sequence(1)-- A token used by keras internally for learning purposes
3.   Unknown word(2) not loaded--load_data dunction uses 2 for words with freq rankings greater than the num_words 



"""

word_to_index =imdb.get_word_index()

word_to_index['great']

#great is the 84 most frequent word

"""### Lets create a mapping for checking words by frequency ratings"""

index_to_word={index: word for(word, index) in word_to_index.items()}

#we then pick the top 60 most frequently used words whose key is one. 
[index_to_word[i] for i in range (1,61)]

"""### Decoding a Movie Review

T o decode a review:
1. i-3 accounts for the frequency ratings offesets in the encoded reviews.
2. i values 0-2 =? otherwise should return the word
"""

' '.join([index_to_word.get(i-3,'?') for i in x_train[123]])

y_train[123]

"""### Data preparation

1. Number of words per review -vary
2. Keras requires all samples to have the same dimension
3. Prepare the data
    - Restrict every review to the same number of words
    - Pad some wth 0's truncate others
    - Pad sequences function- reshapes the samples in 2D array
"""

words_per_review=100

from tensorflow.keras.preprocessing.sequence import pad_sequences

x_train= pad_sequences(x_train,maxlen=words_per_review)

x_train.shape

x_train[34]

"""#### Data preparation continuation

Reshape the x-test
"""

x_test= pad_sequences(x_test, maxlen=words_per_review)

x_test.shape

"""### Splitting the test data into validation and test data

- Split the 25,000 test samples into 20,000 test samples and 5,000 validation samples
- We pass validation samples to the models fit method - validation_data argument
- we use the scikit-learn train_test_split function
"""

from sklearn.model_selection import train_test_split

x_test,x_val,y_test,y_val =train_test_split(x_test,y_test,random_state=11, test_size=0.20)

x_test.shape

x_val.shape

"""# Creating the Neural Network"""

from tensorflow.keras.models import Sequential

rnn= Sequential()

rnn

from tensorflow.keras.layers import Dense, LSTM, Embedding

"""### Adding an embedding layer

- Convnet example we used one-hot encoding - into categorical data -others 0 and one 1
- Index values that represents words
- 1,000000000000000000000000000000000000000000000000000000000000000000000000
- 0,10000000000000000000000000000000000000000000000000000000000000000000000
- recall cnn.add(Dense(units=10, activation='softmax'))- 0,1,2,3,4,5,6,7,8,9=>0.0003,0.88
- Will need 10,000 by 10,000 array to represent all the words.
 - All would be 0 except 1
 - all 88,000+ unique words-- you eight billion elements

- Reduce dimensionality - RNN process Text Sequences, use the embedding layer
- Each encodes each word in a more compact dense vector representation
- Help RNN - word relations ->this movie is not good -- 0 this movie is good--1
    - Predefined word embeddings --Word2Vec and GloVe
      - can load into nueral networks to save training time.
      -used to add basic word relationships to model smaller amouts of training data(available)
      -Improve model accuracy by looking at the previous word relationships- Transfer Learning
"""

rnn.add(Embedding(input_dim=number_of_words,output_dim=128, input_length=words_per_review))

"""- input_dim ==number of unique words
- output_dim==size of the word embedding
- input length== Number of words in each input sample.

### Adding an LSTN LAYER
"""

rnn.add(LSTM(units=128,dropout=0.2, recurrent_dropout=0.2))

"""- units --number of neurons in the layer(the more the neurons the more network can remember)
- length of the sequences -200-- and the number of classesto predict --2 class -2-200
- dropout- percentage of neurons that are disabled when preprocessing the layer's input and output.
- keras provides a Drop out layer that you can add to your models
 --  % of neurons that are randomly disabled

### Adding Dense Output Layer

We nned to reduce the LSTM layer's output to onr value (result should be one) -+ or- We need the value of 1 for the units arguments. 'sigmoid' activation function- used for binary classification-reduces arbitrary values into the range 0.0 -1.0, producing a probability.
"""

rnn.add(Dense(units=1,activation='sigmoid'))

"""### Compiling the model and Displaying summary

'categorical_cross entropy' --'binary_crossentropy' regression-- mean_squared error
"""

rnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

rnn.summary()

"""Training and evaluating the model
 - For every epoch in RNN model takes longer to train than the CNN (Number of parameters). 
"""

rnn.fit(x_train,y_train, epochs= 10, batch_size=32, validation_data=(x_test, y_test))

"""# Natural Language Processing

Tuning deep learning models
- Some variables that can affect the model performance
  - more or less data to train with
  - more or less data to test with
  - more or less data to validate
  - having more or fewer layers
  - types of layers you use
  - order of the layers
Some things that we could tune:
    - Try different amounts of training data - 10,000
    - Different number of words per review - 200-- 300
    - Different number of neurons in our layers
    - More layers 
    - Transfer learning - loading pre-trained word vectors rather learning from scratch
    - k-fold cross-validation - fold cross validation ANN - longer time- tuning with hyperparameters

### Objectives

- NLP - It is important for most cases
- TextBlob, NLTK, textatisitic and spaCAY
- Tokenize text into words and sentences
- parts of speech tagging
- Sentiment analysis - + - neutral
- Detecting languate of text and translate between languages
- word roots- stemming and lemmatization
- spell checking and correction
- Remove the stop wods from the text
- word visualizations
- readability assessment
- named entity recognition and similarly detection

### Examples of NL communications
- conversations between 2 people
- learning a foreign language
- use of smartphone to read menu
- reading/writing text messages
- blind-braille or listening to the screen reader
- email - spanish- english

* Text collections - corpora or plural corpus
- tweets
- facebook posts
- movie reviews
- documents
- books
- news

*** Nuances of meaning- makes NL understanding - difficult
-- Meaning can be influenced by context and reader's view of the world

* TextBlob: Simplified text processing
- Object oriented NLP text processing - built on the NLTK and pattern NLP libraries
- jobs 
  -Tokenization -splitting text into pieces of tokens -words or numbers
  - parts to speech(POS) tagging - nouns, verb, adjective
  - noun phrase extraction- 'red brick factory'
    - Is a red brick factory - a factory that makes red bricks
    - is it a red factory that makes bricks of any color
    - is it a factory built of red bricks that makes products of any type
    - Music group - pop
 - sentiment analysis
  -Inter- language translations and detecting the language -Google Translate
  - Inflection- pluralizing or singularizing words
  - spellchecking and spelling correction
  - stemming -varieties- varieti
  - lemmatization- varieties- variety- generate real words based on word's context
  - wordNet intergation
  - word frequencies
  - Stop word elimination- as, a,an,the,I, we
  - n-grams- producing sets of consecutive words in a corpus for use in identifying words that frequently appear adjacent to one other.
"""

pip install textblob

"""# Project gutenberg

Rich source for text for analysis - free e-books

# Create a TextBlob
"""

from textblob import TextBlob

text= 'Today is a beautiful day. Tomorrow looks like bad weather.'

blob= TextBlob(text)

blob

"""The text blob does support various string methods and comparisons - sentences words"""

import nltk
nltk.download('punkt')

blob.sentences #sentence (s) word(s)- inherit from BaseBlob--

blob.words

"""### Parts of speech Tagging

- Evaluate words based on context -determine POS- determine the meaning
- nouns, pronouns,verbs, adjectives,adverbs, prepositions, conjunctions and interjections
- sub-categories-
- meaning of words-'set', 'run'
"""

nltk.download('averaged_perceptron_tagger')

blob

blob.tags

"""- TextBlob- patternTagger 63 parts of speech tages
- NN -Singular noun or mass noun
- VBZ- third person singular present verb.
- DT- determiner- (the an that, my this, their)
- NNP- proper singular noun
- IN- subordinating conjuction or preposition

# Extracting noun phrases
"""

nltk.download('brown')

blob

blob.noun_phrases

"""# Sentiment Analysis with the TextBlob Default Sentiment Analyzer

- positive, negative, neutral
- food is not good, the movie was not bad, the movie was excellent
- deep learning
"""

blob

blob.sentiment

"""- Polarity- -1(neg), 1.0(pos), 0.0neutral
-subjectivity- 0.0objective, 1.0 subjective
"""

text2="Vote! Vote! Vote!"
blob2=TextBlob(text2)

blob2

blob2.sentiment

"""default precision for standalone float obejct- lists,tuples,dic"""

# Commented out IPython magic to ensure Python compatibility.
# %precision 3

blob.sentiment.polarity

blob.sentiment.subjectivity

blob

for sentence in blob.sentences:
  print(sentence.sentiment)

"""### Sentiment Analysis with the NaiveBayesAnalyzer"""

from textblob.sentiments import NaiveBayesAnalyzer

text

blob= TextBlob(text,analyzer=NaiveBayesAnalyzer())

nltk.download('movie_reviews')

blob.sentiment

for sentence in blob.sentences:
  print(sentence.sentiment)

"""### Language detection and Translation

- near real-time translation
- IBM Watson- inter language translation
"""

blob

blob.detect_language()

spanish= blob.translate(to='es')

spanish

spanish.detect_language()

chinese= blob.translate(to='zh')

chinese

swahili= blob.translate(to='sw')

swahili

"""### Inflections: Pluralization and Singularization

### Inflections: Pluralization and Singularization

Inflections are different forms of the same words, such as singular and plural, people person, and different verb tenses -run ran
- word freq- want to convert all inflected words to swame form-- accurate word freq
"""

from textblob import Word

index= Word('index')

index

index.pluralize()

cacti=Word('cacti')

cacti.singularize()

from textblob import TextBlob

animals= TextBlob('dog cat fish bird').words

animals

animals.pluralize()

"""### Spell checking and Correction"""

