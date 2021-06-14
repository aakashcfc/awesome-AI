import copy
import random
import math
import itertools
import operator

#
class Solver:
    def __init__(self):
        self.probability_speech = {}
        self.foward_matrix_vt = {}
        self.probability_next_speech = {}
        self.probability_last_speech = {}
        self.probability_previous_speech = {}
        self.probability_word_speech = {}
        self.probability_first_speech = {}
        self.all_word_speech_keys = []
        self.all_next_speech_keys = []
        self.sampled_values = [[]]
        self.path_vt = []
        # Calculate the log of the posterior probability of a given sentence

    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):

        sum = 0.0
        mult = 1
        for i in range(0, len(sentence)):
            word_speech = sentence[i] + '_' + label[i]
            probab_wrd_speech = 1
            if word_speech in self.all_word_speech_keys:
                probab_wrd_speech = self.probability_word_speech[word_speech]
            speech = label[i]
            if i == 0:
                probab_next_speech = self.probability_first_speech[label[0]]
            else:
                probab_next_speech = self.probability_next_speech[label[i] + '_' + label[i - 1]]
            probab_speech = self.probability_speech[speech]
            mult *= probab_wrd_speech * probab_next_speech
            #sum += probab_wrd_speech * probab_speech
        try:
            answer = math.log(mult)
        except ValueError:
            answer =0

        return answer

    def update(self, m, k, count):
        m[k] = float(m[k]) / count

    # Do the training!
    #
    def train(self, data):
        print("Inside training")
        total_count = 0
        total_count_last_speech = 0.0
        for line in data:
            total_count += len(line[1])
            for index in range(0, len(line[1])):
                if index == 0:
                    self.probability_first_speech.setdefault(line[1][0], 0)
                    self.probability_first_speech[line[1][0]] += 1
                elif index == len(line[1]) - 1:
                    self.probability_last_speech.setdefault(line[1][index], 0)
                    self.probability_last_speech[line[1][index]] += 1
                    total_count_last_speech += 1

                if index < (len(line[1])) - 1:
                    x = line[1][index + 1].lower() + '_' + line[1][index]
                    y = line[1][index].lower() + '_' + line[1][index + 1]
                    self.probability_next_speech.setdefault(x, 0)
                    self.probability_next_speech[x] += 1
                    self.probability_previous_speech.setdefault(y, 0)
                    self.probability_previous_speech[y] += 1
                x = line[0][index].lower() + '_' + line[1][index]
                self.probability_word_speech.setdefault(x, 0)
                self.probability_word_speech[x] += 1
                self.probability_speech.setdefault(line[1][index], 0)
                self.probability_speech[line[1][index]] += 1

        # s=min(self.probability_next_speech.values())
        s = 1
        self.probability_next_speech['x_pron'] = 1
        self.probability_previous_speech['pron_x'] = 1
        [self.update(self.probability_next_speech, k, self.probability_speech[k.split('_')[1]]) for k in
         self.probability_next_speech.keys()]
        [self.update(self.probability_previous_speech, k, self.probability_speech[k.split('_')[1]]) for k in
         self.probability_previous_speech.keys()]
        [self.update(self.probability_word_speech, k, self.probability_speech[k.split('_')[1]]) for k in
         self.probability_word_speech.keys()]

        [self.update(self.probability_speech, k, total_count) for k in
         self.probability_speech.keys()]
        count_first_speech = sum(self.probability_first_speech.values())
        [self.update(self.probability_first_speech, k, count_first_speech) for k in
         self.probability_first_speech.keys()]
        [self.update(self.probability_last_speech, k, total_count_last_speech) for k in
         self.probability_last_speech.keys()]
        self.all_next_speech_keys = self.probability_next_speech.keys()
        self.all_word_speech_keys = self.probability_word_speech.keys()
        print("Training Complete")

    # Functions for each algorithm.
    #
    def naive(self, sentence):
        speech_map = []
        prob_map = []

        for word in sentence:
            max = 0
            s = ''

            for speech in self.probability_speech.keys():
                k = word + '_' + speech
                if k not in self.all_word_speech_keys:
                    continue
                prob_wrd_spch = self.probability_word_speech[k]
                new_prob = (prob_wrd_spch * self.probability_speech[speech])

                if new_prob > max:
                    s = speech
                    max = new_prob
            if max != 0:
                speech_map = speech_map + [s]
                prob_map = prob_map + [max]

            else:
                speech_map = speech_map + ["noun"]
                prob_map = prob_map + [max]

        p = [[speech_map], []]
        return p

        # return [[["noun"] * len(sentence)], []]

    def mcmc(self, sentence, sample_count):

        sample_list = list(sentence)
        self.sampled_values = [[]]
        map(lambda x: self.sampled_values[0].append('noun'), range(0, len(sample_list)))
        initial_values = copy.copy(self.sampled_values[0])
        speech_list = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        for i in range(0, 200):  # sample generation

            for j in range(0, len(sample_list)):
                probability_values = []
                probablility_sum = 0
                for k in range(0, 12):
                    t = 0
                    wrd_speech = float(4.22316915059e-8)
                    u = 1
                    new_speech = speech_list[k]

                    if j == 0:
                        t = self.probability_first_speech[new_speech]
                    else:
                        if new_speech + '_' + initial_values[j - 1] in self.all_next_speech_keys:
                            t = self.probability_next_speech[new_speech + '_' + initial_values[j - 1]]

                    x = sample_list[j] + '_' + new_speech
                    if x in self.probability_word_speech:
                        wrd_speech = self.probability_word_speech[x]

                    if k < len(sample_list) - 1:
                        next_speech = initial_values[k + 1] + '_' + new_speech
                        if next_speech in self.all_next_speech_keys:
                            u = self.probability_next_speech[next_speech]
                    temp_val = u * t * wrd_speech
                    probablility_sum += temp_val
                    probability_values.append(temp_val)
                # probablility_sum=sum(probability_values)
                c = 0
                r = random.uniform(0.00, 1.00)
                for q in range(0, len(probability_values)):
                    probability_values[q] = probability_values[q] / probablility_sum
                    c += probability_values[q]
                    probability_values[q] = c
                    if r < probability_values[q]:
                        o = q
                        break

                initial_values[j] = speech_list[o]
            self.sampled_values.append(initial_values)
        top_sampled_value = self.sampled_values[len(self.sampled_values) - sample_count:]

        return [top_sampled_value, []]

        # return [[["noun"] * len(sentence)], []]

    def best(self, sentence):
        forward_matrix_best = {}
        sen = list(sentence)
        sentence = list(reversed(sen))
        path = []
        speech_list = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        previous_flag = {}
        for index_eachword in range(0, len(sentence)):
            eachword = sentence[index_eachword]
            last_max_value = 0
            if eachword[len(eachword) - 1] == 's' and eachword[len(eachword) - 2] == "'":
                eachword = eachword[0:len(eachword) - 2]
            previous_flag[index_eachword] = 0
            if index_eachword == 0:
                for speech in speech_list:
                    if sentence[0] + '_' + speech in self.all_word_speech_keys:
                        forward_matrix_best[speech, index_eachword] = ((self.probability_last_speech[speech] *
                                                                        self.probability_word_speech[
                                                                            sentence[0] + '_' + speech]), -1)
                        previous_flag[index_eachword] = 1
                    else:
                        forward_matrix_best[speech, index_eachword] = (
                        float(4.22316915059e-10) * self.probability_last_speech[speech], -1)
                        previous_flag[index_eachword] = 1
                    if index_eachword == len(sentence) - 1 and last_max_value < \
                            forward_matrix_best[speech, index_eachword][0]:
                        last_max_value = forward_matrix_best[speech, len(sentence) - 1][0]
                        last_max_tag = speech
            else:
                temp_back_pointer = -1
                for speech in speech_list:
                    max_value = 0
                    if eachword + '_' + speech in self.all_word_speech_keys:
                        emission = self.probability_word_speech[eachword + '_' + speech]
                        previous_flag[index_eachword] = 1
                    else:
                        emission = float(4.22316915059e-10)
                        previous_flag[index_eachword] = 1
                    for i in speech_list:
                        if speech + '_' + i in self.all_next_speech_keys:
                            transition_prob = self.probability_previous_speech[speech + '_' + i]
                        else:
                            transition_prob = 0
                        previous_veterbi_coeff = forward_matrix_best[i, index_eachword - 1][0]
                        new_veterbi_coeff = float(transition_prob) * previous_veterbi_coeff
                        if new_veterbi_coeff > max_value:
                            max_value = float(new_veterbi_coeff)
                            temp_back_pointer = i
                        #
                    forward_matrix_best[speech, index_eachword] = (float(max_value) * emission, temp_back_pointer)
                    if index_eachword == len(sentence) - 1 and last_max_value < \
                            forward_matrix_best[speech, index_eachword][0]:
                        last_max_value = forward_matrix_best[speech, len(sentence) - 1][0]
                        last_max_tag = speech

        for i in list(reversed(range(0, len(sentence)))):
            path.append(last_max_tag)

            last_max_tag = forward_matrix_best[last_max_tag, i][1]
        '''
        for i in range(0,len(path)):
            if self.foward_matrix_vt[self.path_vt[i],i] > forward_matrix_best[path[i],i]:
                path[i]=self.path_vt[i]
        '''

        return [[path], []]
        # return [[["noun"] * len(sentence)], []]

    def max_marginal(self, sentence):
        top_samples = self.sampled_values.pop()
        value_dict = {}
        for i in range(0, len(self.sampled_values)):
            each_sample = self.sampled_values[i]
            for k in range(0, len(each_sample)):
                value_dict.setdefault((k, each_sample[k]), 0)
                value_dict[(k, each_sample[k])] += 1

        probab_values = []
        for i in range(0, len(top_samples)):
            sp = top_samples[i]
            total = 0.0
            actual = 0.0
            for key, value in value_dict.items():
                if key[0] == i:
                    total += value
                    if key[1] == sp:
                        actual += value
            probab_values.append(actual / total)
        return [[top_samples], [probab_values]]

    def viterbi(self, sentence):
        path = []
        self.foward_matrix_vt = {}
        speech_list = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        previous_flag = {}
        for index_eachword in range(0, len(sentence)):
            eachword = sentence[index_eachword]
            last_max_value = 0
            if eachword[len(eachword) - 1] == 's' and eachword[len(eachword) - 2] == "'":
                eachword = eachword[0:len(eachword) - 2]
            previous_flag[index_eachword] = 0
            if index_eachword == 0:
                for speech in speech_list:
                    if sentence[0] + '_' + speech in self.all_word_speech_keys:
                        self.foward_matrix_vt[speech, index_eachword] = ((self.probability_first_speech[speech] *
                                                                          self.probability_word_speech[
                                                                              sentence[0] + '_' + speech]), -1)
                        previous_flag[index_eachword] = 1
                    else:
                        self.foward_matrix_vt[speech, index_eachword] = (
                        float(4.22316915059e-10) * self.probability_first_speech[speech], -1)
                        previous_flag[index_eachword] = 1
                    if index_eachword == len(sentence) - 1 and last_max_value < \
                            self.foward_matrix_vt[speech, index_eachword][0]:
                        last_max_value = self.foward_matrix_vt[speech, len(sentence) - 1][0]
                        last_max_tag = speech
            else:
                temp_back_pointer = -1
                for speech in speech_list:
                    max_value = 0
                    if eachword + '_' + speech in self.all_word_speech_keys:
                        emission = self.probability_word_speech[eachword + '_' + speech]
                        previous_flag[index_eachword] = 1
                    else:
                        emission = float(4.22316915059e-10)
                        previous_flag[index_eachword] = 1
                    for i in speech_list:
                        if speech + '_' + i in self.all_next_speech_keys:
                            transition_prob = self.probability_next_speech[speech + '_' + i]
                        else:
                            transition_prob = 0
                        previous_veterbi_coeff = self.foward_matrix_vt[i, index_eachword - 1][0]
                        new_veterbi_coeff = float(transition_prob) * previous_veterbi_coeff
                        if new_veterbi_coeff > max_value:
                            max_value = float(new_veterbi_coeff)
                            temp_back_pointer = i
                        #
                    self.foward_matrix_vt[speech, index_eachword] = (float(max_value) * emission, temp_back_pointer)
                    if index_eachword == len(sentence) - 1 and last_max_value < \
                            self.foward_matrix_vt[speech, index_eachword][0]:
                        last_max_value = self.foward_matrix_vt[speech, len(sentence) - 1][0]
                        last_max_tag = speech
        path = []
        for i in list(reversed(range(0, len(sentence)))):
            path.append(last_max_tag)
            last_max_tag = self.foward_matrix_vt[last_max_tag, i][1]

        self.path_vt = list(reversed(path))

        return [[self.path_vt], []]


        # return [[["noun"] * len(sentence)], []]

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #    Most algorithms only return a single labeling per sentence, except for the
    #    mcmc sampler which is supposed to return 5.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for max_marginal() and is the marginal probabilities for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "Sampler":
            return self.mcmc(sentence, 5)
        elif algo == "Max marginal":
            return self.max_marginal(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        elif algo == "Best":
            return self.best(sentence)
        else:
            print("Unknown algorithm!")