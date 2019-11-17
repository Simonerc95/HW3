#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import index_utils 


# In[ ]:


path = os.getcwd() #the path that we want to save out json files
# call indexing functions
get_vocab_index(path)
get_inverted_index(path)

