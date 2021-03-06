from collections import Counter
import numpy as np
import re
import pickle
import os #imports
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
app = Flask(__name__, template_folder='./templates') #initialize the flask - used to create web apps with python- and we set the templates foldet for the template of the html

label = {0:'ham', 1:'spam'}
stop = pickle.load(open(
                os.path.join('model', 
                'pickles', 
                'stopwords.pkl'), 'rb')) # loading the stopwords

classifier = pickle.load(open(
                os.path.join('model', 
                'pickles', 
                'classifier.pkl'), 'rb')) # loading the classifier

def make_Dictionary(train_dir):
    emails = [os.path.join(train_dir,f) for f in os.listdir(train_dir)]    
    all_words = []       
    for mail in emails:    
        with open(mail) as m:
            for i,line in enumerate(m):
                if i == 2:  #Body of email is only 3rd line of text file
                    words = line.split()
                    all_words += words 
    
    dictionary = Counter(all_words)
    list_to_remove = dictionary.keys()
    for item in list(list_to_remove):
        if item.isalpha() == False: 
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
    dictionary = dictionary.most_common(3000)
    return dictionary #same function to create a dictionary - we put it here in order for pythn to be able to use it 


def extract_features(mail_dir): 
    train_dir = './data/train-mails'
    dictionary = make_Dictionary(train_dir)
    files = [os.path.join(mail_dir,fi) for fi in os.listdir(mail_dir)]
    features_matrix = np.zeros((len(files),3000))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
          if i == 2:
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1     
    return features_matrix # same extract feature because this is a python file





 
@app.route("/")
def index():
  return render_template('index.html') # set the route

def write_mail_to_file(mailContent = ''):
  path = './data/example'
  filename = 'example.txt'
  if not os.path.exists(path):
      os.makedirs(path) 

  f = open(os.path.join(path, filename), 'w+')
  f.write(mailContent)
  f.close() #function tp save the mail tht we he have inputted to save it in the file exapmle . txt in the folder data/example

@app.route("/check-email", methods=['POST'])
def check_mail():
  try:
      print(request.form)
      write_mail_to_file(request.form['mailContent'])
      example_dir = './data/example'
      X = extract_features(example_dir)

      print('Prediction 1: %s\nProbability 1: %.2f%%' %(label[classifier.predict(X)[0]], np.max(classifier.predict_proba(X))*100))

      res = {"success": True, "isSpam": label[classifier.predict(X)[0]], "probability": np.max(classifier.predict_proba(X))*100}
      return jsonify(res)
  except Exception as e:
        print(e)
        res = {"success": False, "error": e}
        return jsonify(res)  # post method to make the request based on what you have and return result wether its a spam or not and return the probabilit of it being true


if __name__ == "__main__":
  app.run(port = 5002, debug=True) # this is for flask so it knows on which port python flask app should run the code