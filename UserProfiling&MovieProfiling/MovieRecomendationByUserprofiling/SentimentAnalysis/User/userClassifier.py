import nltk
import random
from nltk.corpus import movie_reviews
import _pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from nltk.classify import ClassifierI
from statistics import mode
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC
from sklearn.tree import DecisionTreeClassifier
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk import precision
from nltk import recall
import collections
import pypyodbc
class NewClassifier(ClassifierI):
    def __init__(self,*classifiers):
        self._classifiers=classifiers

    def classify(self,features):
        votes=[]
        for c in self._classifiers:
            v=c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf


def word_feats_extrnl(words):
    return dict([(word, True) for word in nltk.bigrams(word_tokenize(words))])

def find_features(words):
    return dict([(word, True) for word in nltk.bigrams(word_tokenize(words))])


with open("E:\MovieRecomendationByUserprofiling\SentimentAnalysis\Movie\positive.txt",encoding='utf-8', errors='ignore')as f:
    pos_content = f.readlines()

with open("E:\MovieRecomendationByUserprofiling\SentimentAnalysis\Movie\\negative.txt", encoding='utf-8', errors='ignore') as f:
    neg_content = f.readlines()

negfeats = []
posfeats = []



for s in neg_content:
    negfeats.append((word_feats_extrnl(s.lower()), 'neg'))

for s in pos_content:
    posfeats.append((word_feats_extrnl(s.lower()), 'pos'))

len_of_day = int(len(negfeats) * 3 / 4)
len_of_movie = int(len(posfeats) * 3 / 4)

print(len(negfeats))
print(len(posfeats))

training_set = negfeats[:len_of_day] + posfeats[:len_of_movie]
testing_set = negfeats[len_of_day:] + posfeats[len_of_movie:]
#naive bayes
classifier = nltk.NaiveBayesClassifier.train(training_set)
print("naive bayes classifier accuracy percentage",(nltk.classify.accuracy(classifier,testing_set))*100)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
#
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues

#train MNB classifier
MNB_classifier=SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB classifier accuracy percentage",(nltk.classify.accuracy(MNB_classifier,testing_set))*100)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
#
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = MNB_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues
#
#train BNB Classifier
BNB_classifier=SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print("BNB classifier accuracy percentage",(nltk.classify.accuracy(BNB_classifier,testing_set))*100)

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = BNB_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues

#MNB classifier
MNB_classifier=SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB classifier accuracy percentage",(nltk.classify.accuracy(MNB_classifier,testing_set))*100)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
#
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = MNB_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues

#SVM classifier
LSVS_classifier=SklearnClassifier(LinearSVC())
LSVS_classifier.train(training_set)
print("SVM_LSVS classifier accuracy percentage",(nltk.classify.accuracy(LSVS_classifier,testing_set))*100)

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = LSVS_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues

#logistic regression
LR_classifier=SklearnClassifier(LogisticRegression())
LR_classifier.train(training_set)

print("Logistic Regression model accuracy percentage",(nltk.classify.accuracy(LR_classifier,testing_set))*100)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = LR_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues
#
#
#
# ensemble classifiers
random_classifier=SklearnClassifier(RandomForestClassifier())
random_classifier.train(training_set)
print("random forest classifier accuracy percentage",(nltk.classify.accuracy(random_classifier,testing_set))*100)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = random_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues

#decision tree
decision_classifier=SklearnClassifier(DecisionTreeClassifier())
decision_classifier.train(training_set)
print("Decision tree classifier accuracy percentage",(nltk.classify.accuracy(decision_classifier,testing_set))*100)
refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = decision_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues

new_classifier=NewClassifier(LSVS_classifier,LR_classifier,classifier,MNB_classifier,BNB_classifier)
print("new classifier accuracy",((nltk.classify.accuracy(new_classifier,testing_set))*100))
for i, (feats, label) in enumerate(testing_set):
    refsets[label].add(i)
    observed = new_classifier.classify(feats)
    testsets[observed].add(i)
# print('Precision:', precision(refsets['pos'], testsets['pos'])) #from trues actual trues
# print ('Recall:', recall(refsets['pos'], testsets['pos']))# from total actual trues
# print('Precision:', precision(refsets['neg'], testsets['neg'])) #from trues actual trues
# print ('Recall:', recall(refsets['neg'], testsets['neg']))# from total actual trues



def AccessNewClassifier(text):
    feats = find_features(text.lower())
    return new_classifier.classify(feats),new_classifier.confidence(feats)
