# part1




Posterior Probabilities:

For Simple model,
P = p(word/tag)*p(tag)

For HMM Model,
P = p(word/tag)*p(tag/pre_tag)

For Complex MCMC model,
P = p(word/tag)*p(tag/prev_tag)*p(next_tag/tag)

Training:

Calculated Words count, Words probability, speech count, speech probability, words associated with parts of speech probability – All these are used to calculate simplified model. Emission probability and transition probability are used for HMM and therefore in Complex MCMC model

Simplified model:

In the training function, I have found all the required probabilities.
Main logic:
For a given word, check the prob_simplified dict and consider the frequency with all parts of speech and take the maximum occurred parts of speech for a particular word

To perform part-of-speech tagging, the most-probable tag s∗i for each word Wi,
s∗i = arg maxsi P (Si = si|W ).

HMM Model:

We use Viterbi and solve this problem using emission and transition probabilities
Transition probability – Probability of change from one parts of speech to other.
P(Tag2/Tag1)
Emission Probability- Probability of Word given tag. If probability is 0, we take lowest probability which is declared in the code
The maximum a posteriori (MAP) labeling for the sentence,
(s∗1, . . . , s∗N ) = arg maxs1,...,sNP (Si = si|W ).

Complex MCMC model:

Using the probability from the Viterbi, I have calculated P(Sn/Sn-1,S0) s∗i = arg maxsi P (Si = si|W ).
Randomly run each time and most of the variables will be independent and probability converges to true posterior when frequencies stop changing.
I have taken default tag as Noun
Using Gibbs method, once the healing period is finished it results in maximum occurred tags for a word in a dict.
This method runs taking random samples hence percentage of accuracy may slightly vary.

Percentages I have noticed when I have executed:

# Part 2
## Case 1: simple Bayes Net  
The emission probability is calculated within each column. Specifically, in j-th column, the probability of i-th pixel is porprotional to the weight of E_ij in j-th column, where E is the edge strength. Intuitively, the it is more likely to choose a pixel with stronger edge.

## Case 2: HMM with Viterbi  
The emission probability is calculated as previous step. For each pixel, the transition probability is calculated by 9 neighbor pixels in previous column. Then take the maximunm value.

## Case 3: HMM with human feedback
The previous two methods have a poor performance when the boundary is vague and changes sharply. Thus, adding a point manually may make the tracking more reasonable. To reach that goal, the elements in the same colunmn with added point are assinged to zero, except for one for added point.

## Result
Upper line is air-ice boundary; lower line is ice-rock boundary.  
#### Image_09
<img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_09/simple.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_09/hmm.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_09/feedback.png'>
<br/>

  
#### Image_16  
<img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_16/simple.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_16/hmm.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_16/feedback.png'>
<br/>

#### Image_23


<img src="https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_23/simple.png">         <img src="https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_23/hmm.png">         <img src="https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_23/feedback.png">

#### Image_30
<img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_30/simple.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_30/hmm.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_30/feedback.png'>
<br/>

#### Image_31
<img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_31/simple.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_31/hmm.png'>         <img src='https://github.iu.edu/cs-b551-fa2021/mmonshiz-moyu-msrilekh-a3/blob/master/part2/output_images/img_31/feedback.png'>
<br/>

## test code
```python
python polar.py 09.png 23 120 55 10
python polar.py 16.png 20 120 46 108
python polar.py 23.png 33 196 92 107
python polar.py 30.png 25 178 81 187
python polar.py 31.png 20 127 60 120
```


# part3

I use bc.train from part1 as a training data to calcualte the initial probabilities and transition probabilities. Also calculate emission probabilities by comparing the obesrved character's pixels with the pixels of each of the character in the image training data. Then I applied both simplified bayes net and viterbi algorithm using these probabilities.
for simplified version I just used the emission probabilities but for hmm Iused viterbi algorithm which used all the initial probabilities, transition probabilties and emission probabilities. 
For emission probabilty I count the number of matched and unmathced pixels seperatly and use different numbers for assuming m pixels are noisy and I come up with the numbers in my code. It seems they work prety good comparing to other numbers. 

since the files are in the folder I run it as below:
$ python3 ./image2text.py test_images/courier-train.png test_images/bc.train test_images/test-0-0.png