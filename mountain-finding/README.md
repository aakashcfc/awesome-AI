# a2
Mountain Finding

Transition Probability: The transition probability P(S_i+1|S_i) of state is calculated by folowing assumptions

If two sates are close to each other then the state is assigned with higher probability else with lower probability
Assuming the mountain ridges lies on top of the image so the states in top of the image is given high probability trans_prob = (total rows -abs(diff between two rows))/sqrt(sum of two rows)
Emission Probability: The Emission Probability of the state P(W|S_i) is calculated by assigning higher probability for a edge strength with higher value. And it returns probable rows with higher image gradient and emission probabilities emis_prob = edge_strength / (sum_of_edge_strength + rows)

Implementation: Method 1: Simple Bayes Net -

We calculate the emission probability for each column of a row and consider the highest value.

Method 2: Viterbi For a particular state, the transition probability for the previous state and emission probability for the current state is considered and the state at the top of the image is given with a higher value by assuming the ridges to be lying on the top of the image. Image gradient is calculated by previous_state_trans_prob * current_state_emis_prob * (total_rows - current_row)^2. For each column, the row with higher image gradient is taken and stored in a list. Once all the columns are computed, we backtrack retrieving the maximum values from each column.

Method 3: When the user inputs one coordinate of the ridge, then the image is split into two parts, and Viterbi is applied to both the parts, the best row for each column will be computed for both the parts using Viterbi and finally we add both the parts together.