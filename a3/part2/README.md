# Part 2
## Case 1: simple Bayes Net  
The emission probability is calculated within each column. Specifically, in j-th column, the probability of i-th pixel is porprotional to the weight of E_ij in j-th column, where E is the edge strength. Intuitively, the it is more likely to choose a pixel with stronger edge.

## Case 2: HMM with Viterbi  
The emission probability is calculated as previous step. For each pixel, the transition probability is calculated by 9 neighbor pixels in previous column. Then take the maximunm value.

## Case 3: HMM with human feedback
The previous two methods have a poor performance when the boundary is vague and changes sharply. Thus, adding a point manually may make the tracking more reasonable. To reach that goal, the elements in the same colunmn with added point are assinged to zero, except for one for added point.

## Result
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
