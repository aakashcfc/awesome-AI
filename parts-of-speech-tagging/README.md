# a2
#Edited by Aakash Sarnobat
Part 1: Part-of-speech Tagging

1. Formulation of problem
This is the classic part-of-speech (POS) tagging problem in Natural Language Processing (NLP).
The training and testing data are composed of sentences with their corresponding true POS labels.
So the goal is to mark every word in a sentence with its part of speech (reference: a3 manual).

2. Design and implementation
This problem can be solved using Bayes Nets, and the a3 manual has already provided 3 methods:
Method 1: Simplified Model
In this simple Bayes model, each word or tag in a sentence is independent from others. So, the
posterior probability P(S|W) will only include prior probabilities of tags P(S) and conditional
probabilities of words given each tag P(W|S). The factorization is easily just multiplying due to
mutual independence. And the maximization is then simply maximizing on each word. For each hidden
variable S, prior probabilities are calculated by the occurance of each tag divided by total
occurance, and the conditional probabilities are from the occurance of each word in each tag.
Method 2: HMM
Figure 1(a) shows a typical representation of Hidden Markov Model (HMM) which is very suitable to
solve this POS tagging problem. Each hidden variable S is now dependent on its parent node. So,
transitional probabilities and initial probabilities are introduced and will replace the prior
probabilities mentioned above in method 1. Factorization is similar but given conditional independence.
And the maximization is performed by using the Viterbi algorithm. In addition, transitional probabilities
are learned by the frequency of how each POS tag is followed by another tag in the training data.
Method 3: Complex For each tag value, we calculate joint probability keeping the other tags as is. We also calculate the number of iterations and the samples to be discarded. We then check which tag appears the most number of times in the given sequence. Probability of a state: The probability of a state is calculated taking into account the emission probability and probability of two previous states. Probability for a sentence can be given as: [P(t1)p(w1|t1)][P(w2|t2)P(t2|t1)].....[P(wn|tn)*P(tn|tn-1,tn-2)] where t-> tag and w -> word The complex probability is calculated as P(t3|t1,t2)

3. Problems, assumptions, simplifications and design decisions
(1) Laplace Smoothing
A common but deadly problem in Bayes inference is the lots of zeros in prior, emission/conditional
and transition probabilities. It is inappropriate to assume these cases never happen, and such extreme
probabilities can cause the failure of algorithm as well, like the logarithm of zero for example.
One way to solve this is using Laplace Smoothing which assigns a very low probability to each zero.
Alpha is an empirical parameter of laplace smoothing, which determines how smooth the output is.
This implementation followed a commonly used alpha value of 1.
(2) Dealing with unknown words
Another issue is how to deal with the new words in testing data which are not included in training set.
That is, when making predictions using testing data, there are no probabilities available for these
words. There are several articles online discussing this issue, but I just chose to ignore them
when calculating posterior probabilities from conditional/emission probabilities. So the corresponding
POS label will just be the majority tag. This assumption can lead to errors in some cases, but the
overall accuracy is already quite satisfying.