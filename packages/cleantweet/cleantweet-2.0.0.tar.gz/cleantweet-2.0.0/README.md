CleanTweet version 0.1.1

CleanTweet helps in Natural Language Processing tasks especially in the area of preprocessing and cleaning your data 
fetched from the Twitter API Backend.

Installation <br/>
pip install cleantweet <br/>
Get Started <br/>
How to clean your Twitter Object:

Example 1: If the text file containing the Twitter JSON Data is in the same directory as project files.

!pip install cleantweet <br/>
from cleantweet import CleanTweet <br/>
import nltk <br/>
nltk.download('punkt')

### Instantiate the CleanTwitter Object
data = CleanTweet('sample_text.txt')

### Call the clean method
print(data.clean())

Example 2: When the above is not the case.

!pip install cleantweet <br/>
from cleantweet import CleanTweet <br/>
import nltk <br/>
nltk.download('punkt')
# import the os module
import os

### Instantiate the CleanTwitter Object
data = CleanTweet(os.path.join('./nameoffolder', 'sampling.txt'))

### Call the clean method
print(data.clean())

In this first version, the method clean() would only preprocess and clean the Twitter Object's default parameters which 
are the id and text.