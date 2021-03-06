import os
import pickle
import json
import nltk
import re
from tqdm import tqdm

class Lexicon:
    """Lexicon = {word1: 1,word2: 2,word3: 3,...}"""

    #Creating object for removing stopwords, i.e.,the,an,a....
    LexiconStopwords = set(nltk.corpus.stopwords.words('english'))

    #Creating object for removing stemmer,converting words to root forms i.e., quickly->quick...
    LexiconStemmer = nltk.stem.PorterStemmer()

    #start of function
    #acts as constructor
    #fun init, takes self & path

    def __init__(self, path):
        """Takes pickle path to store lexicon,calls open lexicon"""
        self.path = path
        self.DocHistory={}
        self.DocHistoryPath=self.path+"Doclist"
        self.lexicon = self.OpenLexicon()
          
    #end of constructor


    #start of function
    #fun getlength, takes self instance 
    #returns length

    def __len__(self):
 
        return len(self.lexicon)

    #end of functon
    

    #start of function
    #acts as constructor
    #fun init, takes self & path

    def OpenLexicon(self):
        """Called by lexicon constructor. Opens existing dictionary, if doestnot exist create new.
        Takes self instance, opens/creates lexicon & loads it, catches exception if any. Serializes file, dumps it, returns lexicon"""
        #creating empty dictionary
        Lexicon1 = {} 

        #try block
        try:
            OpenFile1 = open(self.path, 'rb')
            Lexicon1 = pickle.load(OpenFile1)
            OpenFile1 .close()

        #catch block    
        except IOError:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, 'wb') as file:

                #dumping file
                pickle.dump(Lexicon1, file)

            #closing file    
            file.close()
         #try block
       
        DocHistoryPath= self.DocHistoryPath
        try:
            OpenFile1 = open(DocHistoryPath , 'rb')
            self.DocHistory = pickle.load(OpenFile1)
            OpenFile1.close()

        #catch block    
        except IOError:
            # os.makedirs(DocHistoryPath, exist_ok=True)
            with open(DocHistoryPath, 'wb') as file:

                #dumping file
                pickle.dump(self.DocHistory, file)
   

        return Lexicon1

    #end of function


    #start of function
    #fun createlexicon, takes self & path
    #returns nothing

    def CreateLexicon(self, documentpath):
        """Createslexicon take self & doc path. Creates lexicon, Counts for files passed. Genertes progress bars.  Reads json file
        create tokens. Saves lexicon prints article counts."""
        Lexicon2 = self.lexicon
        articlecount=0

        DocHistoryPath=self.DocHistoryPath

        #iterating through each path
        for path in tqdm(documentpath):

            #if the input file is not in dochistory i.e., lexicon not created
            if path not in self.DocHistory:
                
                with open(path, encoding="utf8") as OpenFile2:

                    #reading the file
                    documents = json.load(OpenFile2)
                    self.DocHistory[path]=1

                #closing the file    
                OpenFile2.close()
                print("\n"+path)
                for document in documents:
                    #calling the function,passign the args

                    #tokenizing title
                    token1 = self.CreateTokens(document['title'])

                    #tokenizing content/article
                    token2 = self.CreateTokens(document['content'])

                    #counting articles
                    articlecount+=1

                    #checking that title words/tokens exists in lexicon, if doesnot exist, adding it in lexicon
                    for x in token1:
                        if x != '' and x not in Lexicon2:
                            #adding at the en of lexicon
                            Lexicon2[x] = len(Lexicon2) + 1

                    #checking that content words/tokens exists in lexicon, if doesnot exist, adding it in lexicon
                    for x in token2:
                        if x != '' and x not in Lexicon2:
                            #adding at the en of lexicon
                            Lexicon2[x] = len(Lexicon2) + 1
                
                    #assigning file name on basis of URL as every URL takes to unique page
                    #saving files with .json extension. Removing any spaces,punctuations from URL....
                    docName=''.join(e for e in (document['url'].lstrip("https://").replace("/","_")) if e.isalnum())

                    #saving files with .json extension at path
                    docpath= self.path.rstrip("Lexicon/Lexicon")+"/UpdatedJsons/"+docName[-50:]+".json"

                    #saving files with .json extension
                    with open(docpath, "w") as newjson:
                        json.dump(document,newjson)


        #saving the lexicon created
        with open(self.path, 'wb') as file:
            pickle.dump(Lexicon2, file)

        #dumping
        with open(DocHistoryPath, 'wb') as file:
            pickle.dump(self.DocHistory, file)

        #closing the file    
        file.close()

        #printing article count
        print(f"Articles= {articlecount}")

    #end of function


    #start of function
    #fun createtoken, takes self instance & word
    #returns token

    #Removes URLs & Stop words
    #Change words to root form i.e., quickly->quick  

    def CreateTokens(self, words):
        """Creates tokens, takes self instance and wordids, removes URLs, punctuations, does steeming, removes stop words
        returns tokens"""
        
        #Removing URLs, numbers and punctuations
        #Removing stop words
        #Stemming words 

        tokens = re.sub('[^A-Za-z]', " ", words).split()
        tokens = [re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in tokens]
        tokens = [re.sub(r'[^A-Za-z]+', '', x) for x in tokens]
        tokens = [x for x in tokens if not x in self.LexiconStopwords]
        tokens = [self.LexiconStemmer.stem(x) for x in tokens]

        return tokens

    #end of funcion

    
    #start of function
    #fun readlexicon, takes self instance
    #returns lexicon

    def ReadLexicon(self):
        """Reads lexicon, takes self instance, loads it & returns it"""
        OpenFile3 = open(self.path, 'rb')
        Lexicon3 = pickle.load(OpenFile3)
        OpenFile3.close()
        return Lexicon3

    #end of function

    #start of function
    #fun searchwordid, takes self instance & word
    #returns wordid if exists

    #looks for word in dictionary
    #returns id if found, else -1

    def SearchWordId(self, word):
        """takes self & word, looks for word in lexicon, returns its id, if not found returns -1. Called while searching."""
        stemmer1 = nltk.stem.PorterStemmer()
        stemmer2 = stemmer1.stem(word)

        #try block
        try:
            id = self.lexicon[stemmer2]
            return id

        #catch block
        except KeyError:
            return -1

    #end of function


    #start of function
    #fun exists, takes self instance & word

    def Exist(self, word):
        """Checks if word exists or not, returns -1 if not"""
        return self.SearchWordId(word) != -1

    #end of function

