#!/usr/bin/env python
# coding: utf-8

# In[1]:


path = os.getcwd() #The address of directory where Movies.html files exist
movies = get_movieList(path)  #this function will give us list of movies urls in the html file of movies which exist in the path address               
save_html(movies) #this function will save all html pages of movies list


# In[ ]:



           

