###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids:
# Anand Karandikar  (askarand)
# Sagar Shah        (sasshah)
# Tejas Kumthekar   (tejakumt)
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
'''

In the formulation the observed states are the words and the hidden states are the part of speech.
The training on the corpus on the train file is done and we generate four tables:
        1) initial probability table
        2) transition probability table
        3) emission probability table
        4) suffix probability table
Here we are only considering the emission and initial probabilities of every word independently for solving the bayes net.
In addition to the above formulation, we also consider the transition probabilities to compute the likelihood sequence using the Viterbi algorithm.

The program works as, first the training stage ensures that every probability table is populated with values. Here, smoothing is also performed to ensure
there is no empty entry in any of the probability tables.
Then we compare every coming word from the test data. While solving for Bayes net, if the word if present in the emission probability table then its values
are used, otherwise, the suffixes for this word is compared and if that too returns us no result, then we get the probability distribution for a dummy
variable stored as 'word_x' in the emission prob. table and return the part of speech with max probability value.
For the viterbi algorithm, we use the transition probabilities and follow the same pattern as in the above problem when a particular word is not found.
Lastly we perform the backtracking and return the results.

'''







####

import random
import math
import copy
import sys

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # change in the type of dictionary structure
    # storing as key combination of (word,pos)

    emission_prob = {}
    transition_prob = {}
    transition_prob_2 = {}
    first_pos_prob = {}
    suffix_prob = {}
    train_set_sentences = 0
    viterbi_table = {}

    pos_prob_sim = [[],[]]
    pos_prob_hmm = [[],[]]
    pos_prob_com = [[],[]]

    list_pos = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.','EOS']

    # mainitaining a suffixes list
    suffixes = {}
    total_words_in_corpus = 0


    def __init__(self):
        self.suffixes = ['sion', 'tion', 'ance', 'ence', 'hood', 'ment', 'ness',
                         'like', 'able', 'ible', 'ion', 'acy', 'age', 'ism', 'ist',
                         'ity', 'ful', 'ish', 'ous', 'ate',  'ify', 'ate', 'ize',
                         'ar', 'or', 'ic', 'al', 'ly', 'en',  'y' ]

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label, algo):

        log_posterior = 0.0

        if "simplified" in str.lower(algo):
            for i in xrange(0, len(sentence)):
                log_posterior += self.pos_prob_sim[1][i]

        elif "hmm" in str.lower(algo):
            for i in xrange(0,len(sentence)):
                log_posterior += math.log(self.pos_prob_hmm[1][i])
        elif "complex" in str.lower(algo):
            return 0
        return log_posterior

    '''
    Probes the suffixes and if present keeps the frequency of the suffix.
    '''
    def probe_suffixes(self, word, pos_word):

        for suff in self.suffixes:
            if word.endswith(suff):
                # if word ends with 'suff' suffix
                if suff not in self.suffix_prob:
                    # check if it exists in the dictionary
                    self.suffix_prob[suff] = {}
                    self.suffix_prob[suff]['count'] = 0
                if pos_word not in self.suffix_prob[suff]:
                    # check if the pos exists in the dictionary
                    self.suffix_prob[suff][pos_word] = 0
                self.suffix_prob[suff][pos_word] += 1
                self.suffix_prob[suff]['count'] += 1

    # Do the training!
    #
    def train(self, data):

        self.train_set_sentences = len(data)

        for j in xrange(0,len(data)):

            words = data[j][0];
            pos = data[j][1];
            for i in xrange(0, len(words)):
                # print  words[i],pos[i]
                # check for the presence of the tuple word,pos
                if (words[i],pos[i]) not in self.emission_prob:
                    self.emission_prob[(words[i],pos[i])] = 0
                self.emission_prob[(words[i],pos[i])] += 1

                # check of the presence of the tuple word,count
                if (words[i],'count') not in self.emission_prob:
                    self.emission_prob[(words[i],'count')] = 0
                self.emission_prob[(words[i], 'count')] += 1
                self.probe_suffixes(words[i], pos[i])

        for j in xrange (0,len(data)):
            pos = data[j][1];
            first_pos = pos[0]

            if first_pos not in self.first_pos_prob:
                self.first_pos_prob[first_pos] = 0
            self.first_pos_prob[first_pos] += 1

            for i in xrange(0,len(pos)-2):

                if pos[i] not in self.transition_prob:
                    self.transition_prob[pos[i]] = {}
                    self.transition_prob[pos[i]]['count'] = 0
                if pos[i+1] not in self.transition_prob[pos[i]]:
                    self.transition_prob[pos[i]][pos[i+1]] = 0

                if pos[i] not in self.transition_prob_2:
                    self.transition_prob_2[pos[i]] = {}
                    self.transition_prob_2[pos[i]]['count'] = 0
                if pos[i + 2] not in self.transition_prob_2[pos[i]]:
                    self.transition_prob_2[pos[i]][pos[i + 2]] = 0

                self.transition_prob[pos[i]][pos[i+1]] += 1
                self.transition_prob[pos[i]]['count'] += 1

                self.transition_prob_2[pos[i]][pos[i + 2]] += 1
                self.transition_prob_2[pos[i]]['count'] += 1

            last_pos = pos[len(pos) - 1]
            second_last_pos  = pos[len(pos)-2]

            if last_pos not in self.transition_prob:
                self.transition_prob[last_pos] = {}
                self.transition_prob[last_pos]['count'] = 0
            if 'EOS' not in self.transition_prob[last_pos]:
                self.transition_prob[last_pos]['EOS'] = 0
            self.transition_prob[last_pos]['EOS'] += 1
            self.transition_prob[last_pos]['count'] += 1

            if second_last_pos not in self.transition_prob_2:
                self.transition_prob_2[second_last_pos] = {}
                self.transition_prob_2[second_last_pos]['count'] = 0
            if 'EOS' not in self.transition_prob_2[second_last_pos]:
                self.transition_prob_2[second_last_pos]['EOS'] = 0
            self.transition_prob_2[second_last_pos]['EOS'] += 1
            self.transition_prob_2[second_last_pos]['count'] += 1

        for dic in self.transition_prob.itervalues():
            self.total_words_in_corpus += dic['count']

        self.smooth_transition_prob()
        self.smooth_emission_prob()
        self.smooth_first_pos_prob()

    # Functions for each algorithm.
    #
    def simplified(self, sentence):

        list_max_pos_prob = [];
        list_prob = [];

        for word in sentence:
            list_s_given_w = []
            # for pos in self.transition_prob:   # to return pos - noun, verb ,...... etc
            for pos in self.list_pos:
                if pos <> 'EOS':
                    list_s_given_w.append(self.prob_s_given_w(pos,word))
            max_s_given_w_tuple = max(list_s_given_w,key=lambda item:item[0])
            list_max_pos_prob.append(max_s_given_w_tuple[1])
            list_prob.append(math.log(max_s_given_w_tuple[0]))

        self.pos_prob_sim[0] = copy.deepcopy(list_max_pos_prob)
        self.pos_prob_sim[1] = copy.deepcopy(list_prob)

        return [
            [list_max_pos_prob],
            [list_prob]
        ]

    def smooth_first_pos_prob(self):
        superset = set(self.list_pos)
        superset.remove('EOS')

        # missing first pos
        delta_set = superset - set(self.first_pos_prob)
        for item in delta_set:
            self.first_pos_prob[item] = 0
        for k in self.first_pos_prob:
            self.first_pos_prob[k] += 1
            self.train_set_sentences += 1



    def smooth_transition_prob(self):

        superset = set(self.list_pos)
        superset.remove('EOS')

        # add the missing keys in the transition prob dict
        delta_set = superset - set(self.transition_prob)
        for item in delta_set:
            self.transition_prob[item]={}
            self.transition_prob[item]['count'] = 0

        delta_set = superset - set(self.transition_prob_2)
        for item in delta_set:
            self.transition_prob_2[item] = {}
            self.transition_prob_2[item]['count'] = 0

        for k,v in self.transition_prob.iteritems():
            # for all_k, all_v in self.transition_prob[k].iteritems():
            dic_set = set(self.transition_prob[k])
            delta_set = superset - dic_set
            # delta_set is nothing but the pos which are not pos for transition_prob[k]
            for all_k in self.transition_prob[k]:
                if all_k <> 'count':
                    self.transition_prob[k][all_k] += 1
                    self.transition_prob[k]['count'] += 1

            for item in delta_set:
                self.transition_prob[k][item] = 1
                self.transition_prob[k]['count'] +=1

        for k,v in self.transition_prob_2.iteritems():
            # for all_k, all_v in self.transition_prob[k].iteritems():
            dic_set = set(self.transition_prob_2[k])
            delta_set = superset - dic_set
            # delta_set is nothing but the pos which are not pos for transition_prob[k]
            for all_k in self.transition_prob_2[k]:
                if all_k <> 'count':
                    self.transition_prob_2[k][all_k] += 1
                    self.transition_prob_2[k]['count'] += 1

            for item in delta_set:
                self.transition_prob_2[k][item] = 1
                self.transition_prob_2[k]['count'] +=1

    def smooth_emission_prob(self):

        for all_pos in self.list_pos:
            if all_pos <> 'EOS':
                proportion = self.transition_prob[all_pos]['count'] / float(self.total_words_in_corpus)
                self.emission_prob[('word_x',all_pos)] = proportion
        self.emission_prob[('word_x','count')] = 1

    def viterbi(self, sentence):

        # reinitialize the viterbi table
        self.viterbi_table = {}

        if len(sentence) > 0:

            # first word probability
            word0 = sentence[0]
            self.viterbi_table[0] = {}
            found = False
            for pos in self.list_pos:
                if (word0, pos) in self.emission_prob:
                    found = True
                    self.viterbi_table[0][pos] = {}
                    self.viterbi_table[0][pos]['prob_val'] = (self.emission_prob[(word0, pos)] / float(self.emission_prob[(word0, 'count')])) \
                                                        * (self.first_pos_prob[pos] / float(self.train_set_sentences))
                    self.viterbi_table[0][pos]['prev_pos'] = None

            if not found:
                for pos in self.list_pos:
                    for suff in self.suffix_prob:
                        if word0.endswith(suff) and pos in self.suffix_prob[suff]:
                            found = True
                            if pos not in self.viterbi_table[0]:
                                self.viterbi_table[0][pos] = {}
                                self.viterbi_table[0][pos]['prob_val'] = self.suffix_prob[suff][pos] / float(self.total_words_in_corpus)
                                self.viterbi_table[0][pos]['prev_pos'] = None
                if not found:
                    for pos in self.list_pos:
                        if pos <> 'EOS' and pos<>'det':
                            if pos not in self.viterbi_table[0]:
                                self.viterbi_table[0][pos] = {}
                                self.viterbi_table[0][pos]['prob_val'] = 0
                                self.viterbi_table[0][pos]['prev_pos'] = None
                            self.viterbi_table[0][pos]['prob_val'] = (self.first_pos_prob[pos] / float(self.train_set_sentences)) * self.emission_prob[('word_x', pos)]
            found = False
            foundInSuff = False

            for i in xrange(1, len(sentence)):

                '''
                All the viterbi table references are now made by the index i instead of the actual word.
                However the other probabilities like emission should be looked up by the word.
                '''

                # word0 = sentence[i-1]
                word1 = sentence[i]
                foundInSuff = False
                found = False
                # print  "size of vt ",len(self.viterbi_table)
                # print i
                print len(sentence)
                for word0_pos_k, word0_pos_v in self.viterbi_table[i-1].iteritems():
                    print "b4 adding ",i
                    if i not in self.viterbi_table:

                        self.viterbi_table[i] = {}
                        print "added ", i
                        for pos in self.list_pos:
                            if pos <> 'EOS' and (word1, pos) in self.emission_prob:
                                found = True
                                if pos not in self.viterbi_table[i]:
                                    self.viterbi_table[i][pos] = {}
                                    self.viterbi_table[i][pos]['prob_val'] = -sys.maxsize
                                    self.viterbi_table[i][pos]['prev_pos'] = None
                                prev_value = word0_pos_v['prob_val'] * float(self.transition_prob[word0_pos_k][pos]) / self.transition_prob[word0_pos_k]['count']
                                if prev_value > self.viterbi_table[i][pos]['prob_val']:
                                    # update the prev_pos
                                    self.viterbi_table[i][pos]['prob_val'] = prev_value
                                    self.viterbi_table[i][pos]['prev_pos'] = word0_pos_k
                        if not found:
                            print " tartar not found : suffix ",self.suffix_prob['ar'] if word1 == 'tartar' else ""
                            # find in the self.suffix_prob
                            for pos in self.list_pos:
                                print "Traversing suffixes"
                                print "for (tartar) : " if word1 == 'tartar' else ""
                                for suff in self.suffix_prob:
                                    if suff<>'count' and word1.endswith(suff) and pos in self.suffix_prob[suff]:
                                        found = True
                                        foundInSuff = True

                                        if pos not in self.viterbi_table[i]:
                                            self.viterbi_table[i][pos] = {}
                                            self.viterbi_table[i][pos]['prob_val'] = self.suffix_prob[suff][pos] / float(self.total_words_in_corpus)
                                            self.viterbi_table[i][pos]['prev_pos'] = word0_pos_k
                                            self.viterbi_table[i][pos]['suff'] = suff

                            if not found:
                                for pos in self.list_pos:
                                    if pos<>'EOS':
                                        if pos not in self.viterbi_table[i]:
                                            self.viterbi_table[i][pos] = {}
                                            self.viterbi_table[i][pos]['prob_val'] = -sys.maxsize
                                            self.viterbi_table[i][pos]['prev_pos'] = None
                                        prev_value = word0_pos_v['prob_val'] * float(self.transition_prob[word0_pos_k][pos]) / self.transition_prob[word0_pos_k]['count']
                                        if prev_value > self.viterbi_table[i][pos]['prob_val']:
                                            # update the prev_pos
                                            self.viterbi_table[i][pos]['prob_val'] = prev_value
                                            self.viterbi_table[i][pos]['prev_pos'] = word0_pos_k
                    else:
                        # print self.viterbi_table[i]
                        for pos in self.list_pos:
                            if pos <> 'EOS':
                                if pos in self.viterbi_table[i]:
                                    prev_value = word0_pos_v['prob_val'] * float(self.transition_prob[word0_pos_k][pos]) / \
                                                 self.transition_prob[word0_pos_k]['count']
                                    if prev_value > self.viterbi_table[i][pos]['prob_val']:
                                    # update the prev_pos
                                        self.viterbi_table[i][pos]['prob_val'] = prev_value
                                        self.viterbi_table[i][pos]['prev_pos'] = word0_pos_k

                for word1_pos_k, word1_pos_v in self.viterbi_table[i].iteritems():
                    ######
                    if foundInSuff:
                        suff = self.viterbi_table[i][word1_pos_k]['suff']
                        self.viterbi_table[i][word1_pos_k]['prob_val'] = self.suffix_prob[suff][word1_pos_k] / float(self.total_words_in_corpus)
                    elif found and not foundInSuff:
                        self.viterbi_table[i][word1_pos_k]['prob_val'] = word1_pos_v['prob_val'] * \
                                                                         float(self.emission_prob[(word1, word1_pos_k)]) / self.emission_prob[(word1, 'count')]
                    else:
                        # print "word_x"
                        self.viterbi_table[i][word1_pos_k]['prob_val'] = word1_pos_v['prob_val'] * \
                                                                         self.emission_prob[('word_x', word1_pos_k)]
                # found = False

        # Backtracking
        outputlist=[]
        outputprob=[]
        max_val = -sys.maxint
        prev_pos = None
        curr_pos = None


        for i in xrange(len(sentence)-1,-1,-1):
            if i == len(sentence) - 1:
                for k, v in self.viterbi_table[i].iteritems():
                    if (max_val < v['prob_val']):
                        prev_pos = v['prev_pos']
                        curr_pos = k
                        max_val = v['prob_val']
                outputlist.insert(0, curr_pos)
                outputprob.insert(0, self.viterbi_table[i][curr_pos]['prob_val'])
            elif i <> 0:
                outputlist.insert(0, prev_pos)
                outputprob.insert(0, self.viterbi_table[i][prev_pos]['prob_val'])
                prev_pos = self.viterbi_table[i][prev_pos]['prev_pos']
            elif i == 0:
                if prev_pos <> None:
                    outputlist.insert(0, prev_pos)
                    outputprob.insert(0, self.viterbi_table[i][prev_pos]['prob_val'])
                else:
                    for k, v in self.viterbi_table[i].iteritems():
                        if (max_val < v['prob_val']):
                            prev_pos = v['prev_pos']
                            curr_pos = k
                            max_val = v['prob_val']
                    outputlist.insert(0, curr_pos)
                    outputprob.insert(0, self.viterbi_table[i][curr_pos]['prob_val'])

        return outputlist,outputprob

    def hmm(self, sentence):

        list_of_pos, prob_of_pos  = self.viterbi(sentence)

        self.pos_prob_hmm[0] = copy.deepcopy(list_of_pos)
        self.pos_prob_hmm[1] = copy.deepcopy(prob_of_pos)

        return [
            [list_of_pos],
            [prob_of_pos]
        ]

    def complex(self, sentence):
        return [
            [
                [ "noun" ] * len(sentence)
              ],
            [
                [0] * len(sentence),
            ]
        ]

    def prob_s_given_w(self,s,w):

        if (w,s) in self.emission_prob:
            return self.emission_prob[(w,s)] / float(self.total_words_in_corpus), s, w
        else:
            for suff in self.suffix_prob:
                if w.endswith(suff) and s in self.suffix_prob[suff]:
                    return self.suffix_prob[suff][s] / float(self.total_words_in_corpus), s, w
        return 1./self.total_words_in_corpus, 'noun', w


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for simplified() and complex() and is the marginal probability for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:
            print "Unknown algo!"