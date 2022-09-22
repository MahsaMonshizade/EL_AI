#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math
import copy

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        # change it a little to have each seperately
        result += [['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH) for y in range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }


# return initial probability, transition probability and emission probabilty
def calculate_probs(train_letters, test_letters, train_txt_fname):
    init_prob = {}
    transition_prob = {}
    emission_prob = {}
    f = open(train_txt_fname, 'r')
    for line in f:
        data = list(" ".join([w for w in line.split()]))
        if data:
            if data[0] in init_prob: # calculating that how many times each character being the initial
                init_prob[data[0]] += 1
            else:
                 init_prob[data[0]] = 1
            for char in range(1, len(data)):
                # the transition probability is a dictionary that has charactera as the key and the value f each character is a dictionary containing the number of that how many times each character comes after this soecifi character
                if data[char - 1] in transition_prob:
                    if data[char] in transition_prob[data[char - 1]]:
                        transition_prob[data[char - 1]][data[char]] += 1
                    else:
                        transition_prob[data[char - 1]][data[char]] = 1
                else:
                    transition_prob[data[char - 1]] = {data[char]: 1}
    # convert the numbers into probabilty
    for i in init_prob:
        init_prob[i] /= sum(init_prob[letter] for letter in init_prob)
    for char in transition_prob:
        for nex_char in transition_prob[char]:
            transition_prob[char][nex_char] /= sum(transition_prob[char][nex_char] for nex_char in transition_prob[char])

    # calculate emission probability
    for test_char in range(len(test_letters)):
        emission_prob[test_char] = {}
        for train_char in train_letters:
            b_count, w_count, b_not, w_not = 0, 0, 0, 0
            for char in range(len(test_letters[test_char])):
                if train_letters[train_char][char] == '*' and test_letters[test_char][char] == train_letters[train_char][char]:
                    b_count += 1
                elif train_letters[train_char][char] == '*':
                    b_not += 1
                elif train_letters[train_char][char] == ' ' and test_letters[test_char][char] == train_letters[train_char][char] :
                    w_count += 1
                elif train_letters[train_char][char] == ' ':
                    w_not += 1
                
                emission_prob[test_char][train_char] = math.pow(0.9999, b_count) * math.pow(0.7,w_count) * math.pow(0.3, b_not) * math.pow(0.0001, w_not)
    return init_prob, transition_prob, emission_prob


# This function use viterbi algorithm to find the most probable sequence of characters in the test (MAP)
def hmm_func(test_letters, train_letters, init_prob, transition_prob, emission_prob):
    for i in range(len(test_letters)):
        cur_state = [None] * 128
        for cur_char in (train_letters):
            if i == 0:
                result = -math.log(emission_prob[0][cur_char]) - math.log(init_prob.get(cur_char, math.pow(10, -10))) # log of 0 would be negative inf so put 10**-10 instead
                cur_state[ord(cur_char)] = [result, [cur_char]]
            else:
                res = math.inf
                max_pre = []
                for pre_char in (train_letters):
                    pre_trans_prob= -math.log(transition_prob.get(pre_char, {}).get(cur_char, math.pow(10, -10))) + pre_state[ord(pre_char)][0] # log of 0 would be negative inf so put 10**-10 instead
                    if pre_trans_prob < res:
                        res = pre_trans_prob
                        max_pre = [pre_trans_prob, pre_state[ord(pre_char)][1] + [cur_char]]
            
                result = max_pre[0] - math.log(emission_prob[i][cur_char])
                cur_state [ord(cur_char)] = [result, max_pre[1]]
        pre_state = copy.deepcopy(cur_state)

    res = math.inf
    result = []
    for element in pre_state:
        # since we get the neg log as it says in the lecture we find the minimum value that is equal to find the maximum a posteriori
        if element is not None and element[0]<res:
                res = element[0]
                result = element
    return ''.join(result[1])


# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

init_prob, transition_prob, emission_prob = calculate_probs(train_letters, test_letters, train_txt_fname)

# using the simplified bayes net and use emission probabiltiy to find the most probabl character in the image
simple = ""
for letter in emission_prob:
    simple += "".join(max(emission_prob[letter], key=lambda x: emission_prob[letter][x]))

hmm = hmm_func(test_letters, train_letters, init_prob, transition_prob, emission_prob)

# The final two lines of your output should look something like this:
print("Simple: " + simple)
print("   HMM: " + hmm) 

### get idea from this link: https://github.com/BharathaAravind/Artificial-Intelligence-B551/blob/master/Assignment4/part2/ocr.py