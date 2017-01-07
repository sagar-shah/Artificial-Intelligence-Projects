###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math
import copy

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    emission_prob = {}
    transition_prob = {}
    first_pos_prob = {}
    total_words_in_corpus = 0

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    #
    def train(self, data):

        pos_dic = {};
        pos_dic['adj'] = None
        pos_dic['adv'] = None
        pos_dic['adp'] = None
        pos_dic['conj'] = None
        pos_dic['det'] = None
        pos_dic['noun'] = None
        pos_dic['num'] = None
        pos_dic['pron'] = None
        pos_dic['prt'] = None
        pos_dic['verb'] = None
        pos_dic['x'] = None
        pos_dic['.'] = None
        pos_dic['EOS'] = None
        pos_dic['count'] = 0



        for j in range (0,len(data)):

            words = data[j][0];
            pos = data[j][1];
            for i in range(0, len(words)):
                # print  words[i],pos[i]
                if words[i] in self.emission_prob:
                    if(self.emission_prob[words[i]][pos[i]] == None):
                        self.emission_prob[words[i]][pos[i]] = 1
                    else:
                        self.emission_prob[words[i]][pos[i]] += 1
                else:
                    self.emission_prob[words[i]] = copy.deepcopy(pos_dic)
                    self.emission_prob[words[i]][pos[i]] = 1

                self.emission_prob[words[i]]['count'] += 1


        self.first_pos_prob = copy.deepcopy(pos_dic)



        # print first_pos_prob
        # transition_prob['EOS'] = copy.deepcopy(pos_dic)

        for j in range (0,len(data)):
            pos = data[j][1];

            first_pos = pos[0]
            if self.first_pos_prob[first_pos] == None:
                self.first_pos_prob[first_pos] = 1
            else:
                self.first_pos_prob[first_pos] += 1

            for i in range(0,len(pos)-1):
                if pos[i] in self.transition_prob:
                    if self.transition_prob[pos[i]][pos[i+1]] == None:
                        self.transition_prob[pos[i]][pos[i+1]] = 1
                    else:
                        self.transition_prob[pos[i]][pos[i+1]] += 1
                else:
                    self.transition_prob[pos[i]] = copy.deepcopy(pos_dic)
                    self.transition_prob[pos[i]][pos[i+1]] = 1

                self.transition_prob[pos[i]]['count'] += 1

            last_pos = pos[len(pos) - 1]
            if last_pos in self.transition_prob:
                if self.transition_prob[pos[len(pos)-1]]['EOS'] == None:
                    self.transition_prob[pos[len(pos) - 1]]['EOS'] = 1
                else:
                    self.transition_prob[pos[len(pos) - 1]]['EOS'] += 1
            else:
                self.transition_prob[last_pos] = copy.deepcopy(pos_dic)
                self.transition_prob[last_pos]['EOS'] = 1

            self.transition_prob[last_pos]['count'] += 1

        for dic in self.transition_prob.itervalues():
            self.total_words_in_corpus += dic['count']

        # print "AAAAAAAAAAAAAAAAA     ",self.total_words_in_corpus
        #
        #
        # print self.transition_prob
        # pass

    # Functions for each algorithm.
    #
    def simplified(self, sentence):

        list_max_pos_prob = [];
        list_prob = [];

        for word in sentence:
            list_s_given_w = []
            for pos in self.transition_prob:   # to return pos - noun, verb ,...... etc
                list_s_given_w.append(self.prob_s_given_w(pos,word))
            max_s_given_w_tuple = max(list_s_given_w,key=lambda item:item[0])
            list_max_pos_prob.append(max_s_given_w_tuple[1])
            list_prob.append(math.log(max_s_given_w_tuple[0]))

        # for word in sentence:
        #     try:
        #         dic = self.emission_prob[word]
        #
        #         max = -1
        #         max_key = None
        #         max_value = None
        #         for key,value in dic.iteritems():
        #             if key <> 'count':
        #                 if value <> None and value > max:
        #                     max_key = key
        #                     max_value = value
        #
        #         list_max_pos_prob.append(max_key)
        #         list_prob.append((float(max_value) / dic['count']))
        #     except:
        #         list_max_pos_prob.append("NOT FOUND")
        #         list_prob.append(0.01)

        return [
            [list_max_pos_prob],
            [list_prob]
        ]

    def hmm(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]

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
        try:
            return self.emission_prob[w][s] / float(self.total_words_in_corpus), s, w
        except:
            return 0.000000000000000000000000000000000001, s, w  # Check later



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

