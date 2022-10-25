#!/usr/bin/env python
# coding: utf-8

# # Published Data: Working with the Pyrfume Datasets

# In[2]:


import pyrfume


# Whether you want to build predictive models or simply organize data, it is essential to begin integrating across datasets and wherever possible bringing the largest datasets to bear on the problem.  Most breakthroughs [don't come from new algorithms but from new, large datasets](https://academic.oup.com/chemse/article/doi/10.1093/chemse/bjab020/6226923?login=true).

# In[5]:


bushdid_molecules = pyrfume.load_data('bushdid_2014/molecules.csv')
bushdid_molecules.head()


# The above shows the first 5 molecules (all 128 are in the full dataframe) from [Bushdid et al, 2014](https://science.sciencemag.org/content/343/6177/1370.long) which looked at the perceptual discriminability of random mixtures in humans.  Even though this data was not on your disk, `Pyrfume` fell back to loading it remotely; future loads of the same data will come from your disk for speed.  The first thing to note is that the index and the first 5 columns are structured identically to what we generated in [Part 2](./your-data) from our own data.  ALL `Pyrfume` datasets have this structure, whether there were obtained from supplemental figures and tables, excel files or pdfs, industrial databases, books, or papyrus scrolls.  Additional columns (such as the final 4 shown above) may also be present, on case-by-case basis, depending on what the authors chose to include in their source materials.
# 
# What else has the `Pyrfume` project extracted from this data source?

# In[6]:


pyrfume.show_files('bushdid_2014')


# The above shows a manifest of (processed) files available.  Curated file names are simple and memorable (typically, "molecules", "behavior", "stimuli", etc.) which means you will often not even need to examine the manifest before retrieving the files you care about.  Importantly, every data archive contains at least one Python script ([`main.py`](https://github.com/pyrfume/pyrfume-data/blob/master/bushdid_2014/main.py)) which provides the full processing workflow going from the raw data provided in the original data source to the cleaned, standardized, organized and mutually compatible datasets provided by `Pyrfume`.

# In[4]:


bushdid_stimuli = pyrfume.load_data('bushdid_2014/stimuli.csv')
bushdid_behavior = pyrfume.load_data('bushdid_2014/behavior.csv')


# Information about each stimulus (in this case a mixture), including the CID (not provided in the original source data) is given in the stimuli file.

# In[6]:


bushdid_stimuli.head()


# Finally, the human behavioral results for each mixture are provided in the behavior file.  How one chooses to join these tables to produce prediction target or otherwise explore the data is up to individual taste, but with standards in place it is much less work than it would have been with the source data alone!

# In[7]:


bushdid_behavior.head()


# Many other datasets are available now, with several dozen additional datasets ready for release in the next 12 months.  Licensing issues stand in the way of some, but the *Pyrfume* maintainers are working this out. 

# In[8]:


pyrfume.list_archives()

