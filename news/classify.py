# Create your views here.

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

def classify(articles):
    #Classify

    def word_feats(words):
        return dict([(word, True) for word in words])

    negids = articles.filter(score__lt=0)
    posids = articles.filter(score__gt=0)

    negfeats = [(word_feats(a.body), 'neg') for a in negids]
    posfeats = [(word_feats(a.body), 'pos') for a in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

    classifier = NaiveBayesClassifier.train(trainfeats)
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    classifier.show_most_informative_features()
