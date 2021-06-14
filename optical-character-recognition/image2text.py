#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Aakash Sarnobat(asarnoba),Deepan Elangovan(deelango),Ruhui Chai(ruhchai)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math
CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
TOTAL_PIXELS = CHARACTER_HEIGHT*CHARACTER_WIDTH
alphabet_list= {}

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

alphabetInitialProbability={}
prev_trans, curr_trans= {}, {}

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
# train_img_fname = "D:\\SEM-1\\ElementsOfAI\\deelango-asarnoba-ruhchai-a3-master\\part3\\courier-train.png"
# train_txt_fname  = "D:\\SEM-1\\ElementsOfAI\\deelango-asarnoba-ruhchai-a3-master\\part1\\bc.train"
# test_img_fname   = "D:\\SEM-1\\ElementsOfAI\\deelango-asarnoba-ruhchai-a3-master\\part3\\test-0-0.png"
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

# function to calculate transition probability
def calculateTransition():

    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    with open(train_txt_fname) as text_file:
        lines = [line.strip() for line in text_file]
    for l in range(0,len(lines)):
        for m in range(0,len(lines[l])-1):
            iterator=lines[l][m]+lines[l][m+1]
            if iterator in prev_trans.keys():
                prev_trans[iterator] += 1
            else:
                prev_trans[iterator] = 1
    alphaList = {}
    for l in range(0,len(lines)):
        for m in range(0,len(lines[l])):
            if lines[l][m] in alphaList.keys():
                alphaList[lines[l][m]] += 1
            else:
                alphaList[lines[l][m]] = 1

    keyList = alphaList.keys()
    for l in keyList:
        for m in keyList:
            if l+m in prev_trans.keys() and l+m in alphaList.keys():
                prev_trans[l + m] = prev_trans[l + m] / (alphaList[l] + alphabetInitialProbability[m])
            else:
                prev_trans[l + m] = 10 ** -7

    for l in TRAIN_LETTERS:
        for m in TRAIN_LETTERS:
            if l+m in prev_trans.keys():
                curr_trans[l + m] = prev_trans[l + m]
            else:
                curr_trans[l + m] = 10 ** -5

    for l in TRAIN_LETTERS:
        for m in TRAIN_LETTERS:
            if l+m not in prev_trans.keys():
                prev_trans[l + m]= 10 ** -9

calculateTransition()

#for simple method we take the letter whose pixels match the most
def simple_bayes(train, test):
    key_list = [key for key in train.keys()]
    final_string = ""
    for i in range(0, len(test)):
        prob_total=[]
        curr=0
        prev=0
        for l in train.keys():
             starCount=0
             blankCount=0
             restCount=0
             for j in range(0,25):
                for k in range(0,14):
                    if train[l][j][k] ==  "*" and test[i][j][k]== "*":
                        starCount+=1
                    elif train[l][j][k] == " " and test[i][j][k]==" ":
                        restCount+=1
                    else:
                        blankCount+=1
             s,b,r = 0.8,0.05,0.4
             prob_total.append((starCount * s + blankCount * b + restCount * r) / TOTAL_PIXELS)

        for p in range(0,len(prob_total)):
            if prob_total[p] > curr:
                curr, prev = prob_total[p], p
        final_string = final_string + key_list[prev]
    return final_string

def calculateProbability(current, char_pos):

    star_prob,rest_prob,blank_prob = 1,0,0
    for i in range(0,CHARACTER_HEIGHT):
        for j in range(0,CHARACTER_WIDTH):
            if char_pos[i][j] == "*" and train_letters[current][i][j] == "*":
                star_prob += 1
            elif char_pos[i][j] == " " and train_letters[current][i][j] == " ":
                blank_prob += 1
            elif char_pos[i][j] != train_letters[current][i][j]:
                rest_prob += 1
    c1,c2,c3 = 0.3,0.55,0.1
    total = 0
    total = (blank_prob*c1 + star_prob*c2 + rest_prob*c3) / TOTAL_PIXELS
    return total

#for viterbi we find the initital,transition and emission probabilities and take the max value by backtracking
def viterbi(test_letters):

    first,sec= [],[]
    train_alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    sec = [(math.log(calculateProbability(train_alphas[j], test_letters[0]), 2))
           for j in range(0 , len(train_alphas))]
    first.append(sec)

    for i in range(1 , len(test_letters)):
        sec,tup1,tup2=[],[],[]
        for k in range(0,len(train_alphas)):
            sub,temp = 0,0
            for j in range(0,len(train_alphas)):
                tmp = 0
                iterator = train_alphas[k]+train_alphas[j]
                tmp = first[i-1][j] + math.log(curr_trans[iterator], 2)
                if tmp > sub:
                    sub = tmp
                    temp = j
            sec.append(sub + math.log(calculateProbability(train_alphas[k], test_letters[i]), 2))
            tup1.append(temp)
        tup2.append(tup1)
        first.append(sec)
    final_string = ""
    for i in range(0,len(test_letters)):
        sub = -sys.maxsize
        tmp = 0
        for j in range(0,len(train_alphas)):
            if first[i][j] > sub:
                sub = first[i][j]
                tmp = j
        final_string = final_string + train_alphas[tmp]
    return final_string

# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
print("\n".join([ r for r in train_letters['a'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
print("\n".join([ r for r in test_letters[2] ]))

# The final two lines of your output should look something like this:
print("Simple: " + simple_bayes(train_letters, test_letters))
print("   HMM: " + viterbi(test_letters))

