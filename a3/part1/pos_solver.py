###################################
# CS B551 Fall 2021, Assignment #3
#
# mmonshiz-moyu-msrilekh
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import numpy as np


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        self.prob_fixed = 0.00000000000000001
        self.count_of_words = {}
        self.prob_words = {}
        self.partofspeech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        self.count_partofspeech = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0, 'num': 0, 'pron': 0,
                                   'prt': 0, 'verb': 0, 'x': 0, '.': 0}
        self.prob_partofspeech = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0, 'num': 0, 'pron': 0,
                                  'prt': 0, 'verb': 0, 'x': 0, '.': 0}
        self.prob_words_partofspeech = {}
        self.count_transition = {}
        self.prob_transition = {}
        self.prob_emission = {}

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!

    def posterior(self, model, sentence, label):

        if model == "Simple":

            P = 0

            for i in range(len(sentence)):

                if label[i] in self.prob_partofspeech:
                    P_speech = math.log(self.prob_partofspeech[label[i]])
                else:
                    P_speech = math.log(self.prob_fixed)

                if (sentence[i], label[i]) in self.prob_emission:
                    P_emission = math.log(self.prob_emission[(sentence[i], label[i])])
                else:
                    P_emission = math.log(self.prob_fixed)

                P += P_speech + P_emission

            return P

        elif model == "HMM":

            P = 0

            for i in range(len(sentence)):

                if (sentence[i], label[i]) in self.prob_emission:
                    P_emission = math.log(self.prob_emission[(sentence[i], label[i])])
                else:
                    P_emission = math.log(self.prob_fixed)

                if i == 0:
                    P += P_emission + math.log(self.prob_transition.get(('Start', label[i]), self.prob_fixed))
                else:
                    P += P_emission + math.log(self.prob_transition.get((label[i - 1], label[i]), self.prob_fixed))

            return P

        elif model == "Complex":

            P = 0

            for i in range(len(sentence)):

                if (sentence[i], label[i]) in self.prob_emission:
                    P_emission = math.log(self.prob_emission[(sentence[i], label[i])])
                else:
                    P_emission = math.log(self.prob_fixed)

                if len(sentence) == 1:
                    P += P_emission + math.log(self.prob_transition.get(('Start', label[i]), self.prob_fixed))

                elif i == 0:
                    P += P_emission + math.log(
                        self.prob_transition.get(('Start', label[i]), self.prob_fixed)) + math.log(
                        self.prob_transition.get((label[i], label[i + 1]), self.prob_fixed))

                elif i == len(sentence) - 1:
                    P += P_emission + math.log(
                        self.prob_transition.get((label[i - 1], label[0]), self.prob_fixed)) + math.log(
                        self.prob_emission.get((sentence[i], label[i - 1]), self.prob_fixed)) + math.log(
                        self.prob_transition.get((label[i], label[i - 1]), self.prob_fixed))

                else:
                    P += P_emission + math.log(
                        self.prob_emission.get((sentence[i - 1], label[i - 1]), self.prob_fixed)) + math.log(
                        self.prob_emission.get((sentence[i], label[i - 1]), self.prob_fixed)) + math.log(
                        self.prob_emission.get((sentence[i + 1], label[i]), self.prob_fixed)) + math.log(
                        self.prob_emission.get((sentence[i + 1], label[i + 1]), self.prob_fixed)) + math.log(
                        self.prob_transition.get((label[i - 1], label[i]), self.prob_fixed)) + math.log(
                        self.prob_transition.get((label[i], label[i + 1]), self.prob_fixed))

            return P
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):

        for words, partsofspeech in data:

            for w, p in zip(words, partsofspeech):

                if w not in self.count_of_words.keys():
                    self.count_of_words[w] = 1
                else:
                    self.count_of_words[w] += 1

                self.count_partofspeech[p] += 1

                if w not in self.prob_words_partofspeech.keys():

                    self.prob_words_partofspeech[w] = {'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'noun': 0,
                                                       'num': 0, 'pron': 0, 'prt': 0, 'verb': 0, 'x': 0, '.': 0}
                    self.prob_words_partofspeech[w][p] += 1

                else:
                    self.prob_words_partofspeech[w][p] += 1

        Total = 0
        for partsofspeech in self.partofspeech:
            Total += self.count_partofspeech[partsofspeech]

        for partsofspeech in self.partofspeech:
            self.prob_partofspeech[partsofspeech] = round((self.count_partofspeech[partsofspeech] / Total), 16)

        Total = 0
        for words in self.count_of_words.keys():
            Total += self.count_of_words[words]

        for words in self.count_of_words.keys():
            self.prob_words[words] = round((self.count_of_words[words] / Total), 16)

        self.prob_simplified = {}

        for i in self.prob_words_partofspeech.keys():

            for j in self.partofspeech:

                if self.prob_words_partofspeech[i][j] == 0:
                    self.prob_simplified[i, j] = self.prob_emission[i, j] = self.prob_fixed

                else:
                    self.prob_emission[i, j] = round(self.prob_words_partofspeech[i][j] / self.count_partofspeech[j],
                                                     16)

                    self.prob_simplified[i, j] = round(
                        (self.prob_emission[i, j] * self.prob_partofspeech[j]) / self.prob_words[i], 16)
        d = []
        speech = []

        for w, p in data:
            speech.append(p)

        for p in speech:

            for i in range(len(p)):

                if i == 0:
                    if ('Start', p[i]) not in self.count_transition:
                        self.count_transition['Start', p[i]] = 1
                    else:
                        self.count_transition['Start', p[i]] += 1

                elif i == len(p) - 1:
                    if (p[i - 1], p[i]) not in self.count_transition:
                        self.count_transition[p[i - 1], p[i]] = 1
                    else:
                        self.count_transition[p[i - 1], p[i]] += 1

                else:
                    if (p[i - 1], p[i]) not in self.count_transition:
                        self.count_transition[p[i - 1], p[i]] = 1
                    else:
                        self.count_transition[p[i - 1], p[i]] += 1

        for k in self.count_transition:
            d.append(k)

        d.sort()

        for i in d:
            if i[0] == 'Start':
                if i not in self.prob_transition:
                    self.prob_transition[i] = round((self.count_transition[i] / len(data)), 16)

            else:
                Sum = self.count_partofspeech[i[0]]
                if i not in self.prob_transition:
                    self.prob_transition[i] = round((self.count_transition[i] / Sum), 16)

        pass

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    def simplified(self, sentence):

        parts_of_speech = []
        speech = ''

        partofspeech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']

        for w in sentence:

            if w in self.count_of_words:
                k = 0

                for p in partofspeech:

                    if self.prob_simplified[w, p] > k:
                        k, speech = self.prob_simplified[w, p], p

                parts_of_speech.append(speech)

            else:
                parts_of_speech.append('noun')

        return parts_of_speech

    def hmm_viterbi(self, sentence):
        sentence_length = len(sentence)

        viterbi_table = np.zeros(12 * sentence_length).reshape(12, sentence_length)

        l = sentence_length - 1
        viterbi_path = np.zeros(12 * l).reshape(12, l)

        partofspeech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']

        k = 0

        for i in range(sentence_length):
            for j in range(0, 12):

                if i == 0:
                    prob_emission = math.log(self.prob_emission.get((sentence[i], partofspeech[j]), self.prob_fixed))
                    prob_transition = math.log(self.prob_transition.get(('Start', partofspeech[j]), self.prob_fixed))
                    iword = prob_emission + prob_transition
                    viterbi_table[j][0] = iword

                else:
                    prob_emission = math.log(self.prob_emission.get((sentence[i], partofspeech[j]), self.prob_fixed))
                    transitions = []

                    for num in range(0, 12):
                        trans_prob = math.log(
                            self.prob_transition.get((partofspeech[num], partofspeech[j]), self.prob_fixed))
                        transitions.append(viterbi_table[num][k - 1] + trans_prob)
                    max_transitions = max(transitions)
                    transitions_i = transitions.index(max_transitions)
                    viterbi_path[j][k - 1], viterbi_table[j][k] = transitions_i, prob_emission + max_transitions

            k += 1

        index, viterbi_path = np.argmax(viterbi_table, axis=0)[-1], viterbi_path.astype('int')
        label = [index]

        c = sentence_length - 2
        while c >= 0:
            label.append(viterbi_path[index][c])
            c -= 1

        label = label[::-1]
        pos = [partofspeech[i] for i in label]

        return pos

    def complex_mcmc(self, sentence):

        x = {}
        parts_of_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        simplified_partofspeech = self.simplified(sentence)

        for i in range(500):

            for word in range(len(sentence)):
                probability = []

                for pos in parts_of_speech:
                    if len(sentence) == 1:

                        prob_emission = math.log(self.prob_emission.get((sentence[word], pos), self.prob_fixed))
                        prob_transition = math.log(self.prob_transition.get(('Start', pos), self.prob_fixed))

                        P = [prob_emission + prob_transition]

                        for i in P:
                            probability.append(i)

                    elif word == 0:

                        prob_emission = math.log(self.prob_emission.get((sentence[word], pos), self.prob_fixed))
                        prob_transition = math.log(self.prob_transition.get(('Start', pos), self.prob_fixed))
                        prob_transition_simplified_partofspeech = math.log(
                            self.prob_transition.get((pos, simplified_partofspeech[word + 1]), self.prob_fixed))

                        P = [prob_emission + prob_transition + prob_transition_simplified_partofspeech]

                        for i in P:
                            probability.append(i)

                    elif word == len(simplified_partofspeech) - 1:

                        prob_emission = math.log(self.prob_emission.get((sentence[word], pos), self.prob_fixed))
                        prob_transition = math.log(
                            self.prob_transition.get((simplified_partofspeech[word - 1], simplified_partofspeech[0]),
                                                     self.prob_fixed))
                        prob_emission_simplified_partofspeech = math.log(
                            self.prob_emission.get((sentence[word], simplified_partofspeech[word - 1]),
                                                   self.prob_fixed))
                        prob_transition_simplified_partofspeech = math.log(
                            self.prob_transition.get((pos, simplified_partofspeech[word - 1]), self.prob_fixed))

                        P = [
                            prob_emission + prob_transition + prob_emission_simplified_partofspeech + prob_transition_simplified_partofspeech]

                        for i in P:
                            probability.append(i)

                    else:

                        P = [math.log(self.prob_emission.get((sentence[word], pos), self.prob_fixed))
                             + math.log(self.prob_emission.get((sentence[word - 1], simplified_partofspeech[word - 1]),
                                                               self.prob_fixed))
                             + math.log(self.prob_emission.get((sentence[word], simplified_partofspeech[word - 1]),
                                                               self.prob_fixed))
                             + math.log(self.prob_emission.get((sentence[word + 1], simplified_partofspeech[word]),
                                                               self.prob_fixed))
                             + math.log(self.prob_emission.get((sentence[word + 1], simplified_partofspeech[word + 1]),
                                                               self.prob_fixed))
                             + math.log(
                            self.prob_transition.get((simplified_partofspeech[word - 1], pos), self.prob_fixed))
                             + math.log(
                            self.prob_transition.get((pos, simplified_partofspeech[word + 1]), self.prob_fixed))]

                        for i in P:
                            probability.append(i)

                possible_prob = [math.exp(i) for i in probability]
                Total_sum = sum(possible_prob)

                for i in range(len(possible_prob)):
                    possible_prob[i] = possible_prob[i] / Total_sum

                r_u = random.uniform(0, 1)
                max_value = 0
                possible_prob_len, simplified_partofspeech_len = len(possible_prob), len(simplified_partofspeech)

                for p in range(possible_prob_len):
                    max_value += possible_prob[p]

                    if max_value > r_u:
                        simplified_partofspeech[word] = self.partofspeech[p]
                        break

                for i in range(simplified_partofspeech_len):

                    if (i, simplified_partofspeech[i]) in x:
                        x[i, simplified_partofspeech[i]] += 1
                    else:
                        x[i, simplified_partofspeech[i]] = 1

        labels = []

        for i in range(len(simplified_partofspeech)):

            m = 0
            speech = ''

            for p in self.partofspeech:

                if (i, p) in x and m <= x[i, p]:
                    m, speech = x[i, p], p

            labels.append(speech)
        return labels

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
