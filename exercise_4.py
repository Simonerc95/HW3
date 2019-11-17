# Algorithmic question
## Longest Palindromic Subsequence

# Given a string S, a subsequence s is obtained by combining characters in their order of appearance in S, whatever their position. The longest palindromic subsequence could be found checking all subsequences of a string, but that would take a running time of O(2^n). Here's an implementation of this highly time-consuming recursive algorithm.

# In[862]:


def toolongpalindromic(S):
    maxlen = 0
    if len(S) <= 1:
        return(len(S))
    if S[0]==S[-1]:
        maxlen += 2 + toolongpalindromic(S[1:-1])
    else:
        maxlen += max(toolongpalindromic(S[:-1]), toolongpalindromic(S[1:]))
    return(maxlen)


# toolongpalindromic('dataminingsapienza')


# import time
# st = time.time()
# toolongpalindromic('dataminingsapienza')
# time.time()-st


# To solve this problem in a polynomial time we can use dynamic programming, with which we check only the extreme characters of each substring, and if they are identical we add 2 to the length of the longest palindromic subsequence found between the extremes of the current substring, otherwise it keeps the greatest of the palindromic subsequences found in substrings of the current subsequence.
# In order to do this, we store the length of all palindromic subsequences and their position in a square array A of size n (the length of S), in which rows and columns are respectively the starting and ending positions of substrings built with consecutive characters of S, where A_{i, i+j}, 0<i< n,0<j<n-i is the length of the longest palindromic subsequence in the substring S[i,i+j]. Starting on the main diagonal, we store lengths of subsequences of 1 charachter, which are palindromic since they "start and end" with the same character. Initializing the array with an identity matrix, we can then proceed for substrings of length >1, checking if the extremes are identical. If that's the case, we add 2 to the element one position down and one left of the current position, which means that we are adding the 2 extremes to the letter count of the longest palindromic sequence found between the extremes (for subsequences of length 2, the 0's below the main diagonal of the identity matrix will be the starting values, since for those subsequences there's 0 elements between the extremes). If the extremes are different, we take the highest value between the element 1 position down and the one that's 1 position left the current one, which means that the current substring of lengthj inherits the longest palindromic subsequence count from the two overlapping substrings of length j-1 that built it, the first starting from the leftmost and the second ending at the rightmost character of the current substring. 


# With dynamic programming, the algorithm keeps memory of the longest palindromic subsequences for substrings of growing length, until the full length of S is reached, for which the same procedure is applied. The final result, i.e. the length of the longest palindromic subsequence in the substring of length n (S itself), is obtained in the upper-right position of A, A_{0,n}.

### The solution obtained through dynamic programming has a running time of the order of O(n)^2.


# Defining a function to get substring of length l from the string S
def substrings(S, l):
    L = []
    for i in range(len(S)-l+1):
        L.append(S[i:i+l])
    return(L)

def longestpalindromic(S):
    arr = np.identity(len(S), dtype='int')
    for j in range(1,len(S)):
        strings = subsstrings(S, j+1)
        for i in range(len(S)-j):
            s = strings[i]
            if s[0] == s[-1]:
                arr[i][i+j] = arr[i+1][i+j-1]+2
            else:
                arr[i][i+j] = max(arr[i+1][i+j],arr[i][i+j-1])
    return arr[0][-1]


# longestpalindromic('dataminingsapienza')

# st = time.time()
# longestpalindromic('dataminingsapienza')
# time.time()-st

