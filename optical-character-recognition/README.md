# a3

Reading Text

Our aim is to detect text string from the test image given as the input. For this we divide the test images into small sub images. These sub images are then passed to our modelled network after which the prediction of the input image is carried out. For our implementation we assume each letter has same width and height. We have an text string with n characters , so we have n observed variables O1....On and n hidden variables l1....ln

Implementation:-

1.Simple Bayes Net

Here we are comparing the two letters from input and training data pixel by pixel and taking the weighted sum for it. We take into account the maximum weighted sum value for a particular letter and consider that for our prediction.

2.Viterbi algorithm

We first calculate the transition probability from one pixel to another. After this we start filling the columns of the matrix with initial probabilities calculated by matching pixels. We also find the emission probability using the transition probability and previous value. We go on column wise carrying forward the path with highest value until we reach the last column. Once we reach the last column we backtrack and find the corresponding letter with the maximum value.