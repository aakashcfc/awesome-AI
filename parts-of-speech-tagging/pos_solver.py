###################################


import random
import math
import sys
from collections import Counter

import numpy as np

import pandas as pd

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        # 12 part-of-speech tags
        self.pos = ('adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.')


    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!

    def posterior(self, model, sentence, label):
        words = list(sentence)
        labels = list(label)
        if model == "Simple":
            simple_prior = 0
            for t in np.arange(len(label)):
                simple_prior += -1*math.log(self.prior_prob[label[t]][t])
            simple_cond = 0
            for t in np.arange(len(label)):
                if sentence[t] in self.unique_words:
                    simple_cond += -1*math.log(self.cond_prob[label[t]][sentence[t]])
            return -1*(simple_prior + simple_cond)

        elif model == "HMM":
            hmm_init = -1*math.log(self.init_prob[label[0]])
            hmm_trans = 0
            for t in np.arange(len(label)-1):
                hmm_trans += -1*math.log(self.trans_prob[label[t]][label[t+1]])
            hmm_emis = 0
            for t in np.arange(len(label)):
                if sentence[t] in self.unique_words:
                    hmm_emis += -1*math.log(self.emis_prob[label[t]][sentence[t]])
            return -1*(hmm_init + hmm_trans + hmm_emis)

        elif model == "Complex":
            prob = 0
            prob = self.mcmc_probability(labels, words)
            if prob == 0:
                prob = 1 / 100000000
            return math.log(prob)
        else:
            print("Unknown algo!")

    prob = math.log(1 / 100000000)
    unique_label = 0

    def mcmc_probability(self, tags, words):
        joint_prob = 0
        # For first terms
        joint_prob = self.e_prob.get(tags[0], {}).get(words[0], self.prob) + self.ps1[tags[0]]

        # For 2nd terms
        if len(words) >= 2:
            joint_prob += self.pss.get((tags[0], tags[1]), self.prob) - self.ps1[tags[0]] + self.e_prob.get(tags[1],
                                                                                                            {}).get(
                words[1], self.prob)

        # For subsequent terms
        if len(words) >= 3:
            for i, j in zip(range(2, len(words)), range(2, len(tags))):
                joint_prob += self.pc.get((tags[j - 2], tags[j - 1], tags[j]), self.prob) - self.pss.get(
                    (tags[j - 2], tags[j - 1]), self.prob) + self.e_prob.get(tags[j], {}).get(words[i],
                                                                                              self.prob)

        return math.exp(joint_prob)
    # Do the training!
    # find all unique words in given data, return a set
    def find_unique_words(self, data):
        self.unique_words = set()
        for (s, gt) in data:
            for word in s:
                self.unique_words.add(word)

    # train simplified model
    def train_simple(self, data):
        N = len(data)
        # find maximum length of sentence
        M = 0
        for (s, gt) in data:
            if len(s) > M:
                M = len(s)
        # prior probabilities P(Q)
        self.prior_prob = {}
        for tag in self.pos:
            self.prior_prob[tag] = np.zeros(M)
        for (s, gt) in data:
            for t in np.arange(len(gt)):
                self.prior_prob[gt[t]][t] += 1
        alpha = 1  # laplace smoothing
        for tag in self.pos:
            self.prior_prob[tag] = (self.prior_prob[tag] + alpha) / (N + len(self.pos))

        # emission/conditional probabilities P(O|Q)
        self.cond_prob = {}
        for tag in self.pos:
            self.cond_prob[tag] = {}
            for word in self.unique_words:
                self.cond_prob[tag][word] = 0
        for (s, gt) in data:
            for i in np.arange(len(s)):
                self.cond_prob[gt[i]][s[i]] += 1
        m = len(self.unique_words)
        alpha = 1  # laplace smoothing
        for tag in self.pos:
            word_sum = 0
            for word in self.unique_words:
                word_sum += self.cond_prob[tag][word]
            for word in self.unique_words:
                self.cond_prob[tag][word] = (self.cond_prob[tag][word] + alpha) / (word_sum + m)

    # train HMM
    def train_hmm(self, data):
        N = len(data)
        # initial probabilities P(Q0)
        self.init_prob = {}
        for tag in self.pos:
            self.init_prob[tag] = 0
        for (s, gt) in data:
            self.init_prob[gt[0]] += 1
        for tag in self.pos:
            self.init_prob[tag] /= N

        # transition probabilities P(Qt+1|Qt)
        pos_12 = self.pos
        self.trans_prob = {}
        for tag in self.pos:
            self.trans_prob[tag] = {}
            for tag_12 in pos_12:
                self.trans_prob[tag][tag_12] = 0
        for (s, gt) in data:
            for t in np.arange(len(gt) - 1):
                self.trans_prob[gt[t]][gt[t+1]] += 1
        m = len(self.pos)
        alpha = 1  # laplace smoothing
        for tag in self.pos:
            tag_sum = 0
            for tag_12 in pos_12:
                tag_sum += self.trans_prob[tag][tag_12]
            for tag_12 in pos_12:
                self.trans_prob[tag][tag_12] = (self.trans_prob[tag][tag_12] + alpha) / (tag_sum + m)

        # emission probabilities P(O|Q)
        self.emis_prob = {}
        for tag in self.pos:
            self.emis_prob[tag] = {}
            for word in self.unique_words:
                self.emis_prob[tag][word] = 0
        for (s, gt) in data:
            for i in np.arange(len(s)):
                self.emis_prob[gt[i]][s[i]] += 1
        m = len(self.unique_words)
        alpha = 1   # laplace smoothing
        for tag in self.pos:
            word_sum = 0
            for word in self.unique_words:
                word_sum += self.emis_prob[tag][word]
            for word in self.unique_words:
                self.emis_prob[tag][word] = (self.emis_prob[tag][word] + alpha) / (word_sum + m)

    def train_mcmc(self,data):
        tags1 = []
        for i in range(len(data)):
            tags1.append(data[i][1][0])

        self.unique_label = list(set(tags1))

        #calculate inital prob
        self.ps1 = dict(Counter(tags1))
        self.ps1 = {k: math.log(v / total) for total in (sum(self.ps1.values(), 0.0),) for k, v in self.ps1.items()}

        tags3 = []
        for i in range(len(data)):
            t = list(data[i][1][1:])
            tags3.append(t)

        tags4 = [item for sublist in tags3 for item in sublist]
        self.ps = dict(Counter(tags4))
        self.ps = {k: math.log(v / total) for total in (sum(self.ps.values(), 0.0),) for k, v in self.ps.items()}

        #calculate transition probability
        self.pss = {}
        tags2 = []
        for i in range(len(data)):
            for j in range(1, len(data[i][1])):
                t1 = data[i][1][j]
                t2 = data[i][1][j - 1]
                t = (t2, t1)
                tags2.append(t)
        self.pss = dict(Counter(tags2))
        self.pss = {k: math.log(v / total) for total in (sum(self.pss.values(), 0.0),) for k, v in self.pss.items()}
        self.pss[('pron', 'x')] = math.log(1 / 1000000)

        #calculate emission probability
        self.e_prob = {}
        for tag in self.unique_label:
            l = []
            for i in range(len(data)):
                for j in range(len(data[i][1])):
                    if data[i][1][j] == tag:
                        l.append(data[i][0][j])
            l = dict(Counter(l))
            l = {k: math.log(v / total) for total in (sum(l.values(), 0.0),) for k, v in l.items()}
            self.e_prob[tag] = l
        self.e_prob = pd.DataFrame(self.e_prob)
        self.e_prob = self.e_prob.fillna(math.log(1 / 1000000))
        #calculate complex probabilitys
        tags3 = []
        for i in range(len(data)):
            for j in range(2, len(data[i][1])):
                t1 = data[i][1][j]
                t2 = data[i][1][j - 1]
                t3 = data[i][1][j - 2]
                t = (t3, t2, t1)
                tags3.append(t)
        self.pc = dict(Counter(tags3))
        self.pc = {k: math.log(v / total) for total in (sum(self.pc.values(), 0.0),) for k, v in self.pc.items()}
        pass

    def train(self, data):
        self.find_unique_words(data)
        self.train_simple(data)
        self.train_hmm(data)
        self.train_mcmc(data)

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        M = len(sentence)
        # part-of-speech labelings of the sentence
        pos_labels = []
        for t in np.arange(0, M):
            label = ''
            if sentence[t] in self.unique_words:
                min = -1*math.log(self.prior_prob['adj'][t]) + -1*math.log(self.cond_prob['adj'][sentence[t]])
                for tag in self.pos:
                    post = -1*math.log(self.prior_prob[tag][t]) + -1*math.log(self.cond_prob[tag][sentence[t]])
                    if post <= min:
                        min = post
                        label = tag
                pos_labels.append(label)
            else:  # assign majority tag if word is unknown
                min = -1*math.log(self.prior_prob['adj'][t])
                for tag in self.pos:
                    post = -1*math.log(self.prior_prob[tag][t])
                    if post <= min:
                        min = post
                        label = tag
                pos_labels.append(label)

        return pos_labels

    def hmm_viterbi(self, sentence):
        M = len(sentence)
        # recording the most probable path of each ending state
        prob_paths = {}
        for tag in self.pos:
            prob_paths[tag] = [''] * M
        # v table: the probability of the most probable path ending at state i at time t
        v_prob = {}
        for tag in self.pos:
            v_prob[tag] = np.zeros(M)
        # initialize v table when t = 0
        for tag in self.pos:
            if sentence[0] in self.unique_words:
                v_prob[tag][0] = -1*math.log(self.init_prob[tag]) + -1*math.log(self.emis_prob[tag][sentence[0]])
            else:
                v_prob[tag][0] = -1*math.log(self.init_prob[tag])

        # find other probabilities for t > 1
        pos_12 = self.pos
        for t in np.arange(1, M):
            for tag in self.pos:
                min = v_prob['adj'][t-1] + -1*math.log(self.trans_prob['adj'][tag])
                parent = ''
                for tag_12 in pos_12:
                    vi_pij = v_prob[tag_12][t-1] + -1*math.log(self.trans_prob[tag_12][tag])
                    if vi_pij <= min:
                        min = vi_pij
                        parent = tag_12
                if sentence[t] in self.unique_words:
                    v_prob[tag][t] = min + -1*math.log(self.emis_prob[tag][sentence[t]])
                else:   # how to handling unseen words?
                    v_prob[tag][t] = min
                prob_paths[tag][t] = parent

        # retrieve the part-of-speech labelings of the sentence
        pos_labels = []
        min = v_prob['adj'][M-1]
        ending_label = ''
        for tag in self.pos:
            if v_prob[tag][M-1] <= min:
                min = v_prob[tag][M-1]
                ending_label = tag
        parent = ending_label
        pos_labels.append(parent)
        for t in np.arange(1, M):
            parent = prob_paths[parent][M-t]
            pos_labels.append(parent)
        pos_labels.reverse()
        return pos_labels

    def complex_mcmc(self, sentence):
        words = list(sentence)
        corpus = ["noun"] * len(sentence)
        samples = []
        for n in range(50):
            new_sample = corpus[:]
            tags = new_sample[:]
            corpus = []
            for i in range(len(new_sample)):
                temp = {}
                temp = temp.fromkeys(self.unique_label)
                for tag in self.unique_label:
                    tags[0:len(corpus)] = corpus
                    tags[i] = tag
                    prob = self.mcmc_probability(tags, words)
                    temp[tag] = prob
                temp = {k: v / total for total in (sum(temp.values(), 0.0),) for k, v in temp.items()}
                choice = np.random.choice(list(temp.keys()), 1, p=list(temp.values()))
                choice = choice[0]
                corpus.append(choice)
            if n > 20:
                samples.append(corpus)
        final = []
        for i in range(len(samples[0])):
            ele = []
            for j in range(len(samples)):
                ele.append(samples[j][i])
                count = Counter(ele).most_common(1)[0][0]
            final.append(count)
        return final

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")