#!/usr/bin/env python
# coding: utf-8

# # Featurization for Machine Learning

# In[1]:


import pyrfume
molecules = pyrfume.load_data('my_data/molecules.csv')  # Load the data we created in the last chapter
cids = molecules.index.tolist()


# Many applications, such as predictive models, propose that molecular structure of an odorant is causal to neural activity or behavior (a reasonable proposition).  Training these models requires that each molecule be represented by a vector of predictors, or features, which in some way describe the structure quantitatively.  Traditionally the chemoinformatic feature-calculation software called [Dragon](https://chm.kode-solutions.net/pf/dragon-7-0/) has been used for this, but since Dragon is commercial software this creates challenges for replication and reproducibility.  Some have found that open source feature-calculation packages such as [Mordred](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-018-0258-y) perform as or nearly as well.  
# 
# Feature-calculation on molecules involves several steps including 1) expression of structure in a standard representation (such as SMILES or InChi), 2) conversion of that structure to a molecule object in memory (e.g. [rdkit](https://www.rdkit.org/) Mol), 3) addition of hydrogens (omitted from the SMILES by design), removal of salts, etc. 4) embedding in 3 dimensions (without violating steric or electostatic principles), 5) feature calculation on this 3d structure. `Pyrfume` abstracts all of this away into one step.

# In[2]:


smiles = molecules['IsomericSMILES'].tolist()
smiles


# In[3]:


from pyrfume.features import smiles_to_mordred
mordred_features = smiles_to_mordred(smiles)


# The code above implements all of the steps required for featurization (except for obtaining the SMILES string, which was done in Part 2).  One can also obtain a SMILES string directly by calling `pyrfume.odorants.cids_to_smiles`.

# In[4]:


mordred_features


# The `mordred_features` Pandas dataframe has (for the current version of Mordred, installed by `Pyrfume`) 1826 computed physicochemical features for each molecule.  What do these features mean?  That's a question for the computational chemists.  As investigators asking how molecular structure might explain or be represented in brain activity or behavior, we just want a set of predictors with a track record of success in structure-based predictive models.

# It has been shown previously that the physics-based features of Dragon (or of Mordred, which implements similar calculations) are good at predicting some kinds of structure-driven outcomes, but not others.  For example, in [Keller et al 2017 (Science)](https://science.sciencemag.org/content/355/6327/820.abstract) it was shown that such features are good for predicting perceived intensity, but not as good at predicting perceived "bakery" smell.  That paper showed that the latter was better predicted by a template-matching approach -- molecules that smell like "bakery" are best predicted by asking whether they are structurally similar to other molecules known to smell like "bakery".  

# In[ ]:


from pyrfume.features import smiles_to_morgan
morgan_features = smiles_to_morgan(smiles)


# In[ ]:


morgan_features


# The dataframe above contains fragment counts, i.e. the number of times, within each molecule (represented by a SMILES string) that a given sub-molecular pattern (e.g. an acetyl group, a benzene ring, or any other possible substructure) occurs.  Each substructure has a unique "hash", which is simply a long integer that can be resolved to that sub-structure (also called a [fingerprint](https://towardsdatascience.com/a-practical-introduction-to-the-use-of-molecular-fingerprints-in-drug-discovery-7f15021be2b1)).  The larger and more diverse the number of molecules that we want to featurize, the larger the number of potential substructures, so the number of predictors can become quite larger (here since we are only working with 5 molecules, there are only 105 unique substructures, of some maximum size).
# 
# These features can be used directly, but they still don't tell us how similar two molecules are.

# In[ ]:


from pyrfume.features import smiles_to_morgan_sim
morgan_sim_features = smiles_to_morgan_sim(smiles, smiles)


# In[ ]:


morgan_sim_features


# By using `smiles_to_morgan_sim` we have the option of a second argument, which is a list of SMILES to compare the original SMILES to.  The result is a measure of similarity between two molecules, defined as their similarity in substructure counts.
# 
# But rather than restrict the the similarity to only those molecules we want to predict, why not compute the similarity to other known odorous (or non-odorous) molecules?

# In[ ]:


from pyrfume.odorants import all_smiles
reference_smiles = all_smiles()
#smiles_to_morgan_sim(smiles, reference_smiles)


# The code above (after uncommenting the last line) will compute a dataframe of similarities between your molecule of interest and several thousand known odorants curated through the `Pyrfume` project.  This list consists of odorants used in [>40 notable journal articles and industrial databases](http://status.pyrfume.org).  

# Because this list is so large, there is a good chance that all of the molecules you are using for your project are already in it.  This means that the feature values can be computed once and you can simply look them up.  These pre-computed values have already been filtred to remove non-informative (e.g. zero variance) features or features with a large fraction of missing values (some features, especially for Mordred, are only computable for esoteric molecules). Furthermore, the remaining missing values have been filled with [KNN imputation](https://medium.com/@kyawsawhtoon/a-guide-to-knn-imputation-95e2dc496e).  This means that they are "ready to go" for machine learning applications (which typically require finite and non-missing values in all predictors).

# In[ ]:


morgan_sim = pyrfume.load_data('morgan/features_sim.csv', cids=cids)


# In[ ]:


mordred = pyrfume.load_data('mordred/features.csv', cids=cids)


# These files are quite large (thousands of molecules (rows) by thousands of features (columns)), but we've selected only the rows (feature vectors) for the 5 CIDs of interest.

# Because every stored value in `Pyrfume` is indexed by CID, we can access the molecules we care about (that we want to get features for) using CIDs as keys.  We can then join them to produce one final set of features for machine learning applications.

# In[ ]:


features = mordred.join(morgan_sim)
features


# We now have one giant dataframe with all 10000+ features (all physicochemical features for Mordred and all Morgan fingerprint similarity features), indexed by CID.  You are now ready for prediction on targets (receptor activation, glomerular imaging data, PCx firing rates, human perception, animal behavior, etc.) using your favoriate ML framework (scikit-learn, pytorch, etc.)
# 
# `Pyrfume` also supports some additional featurizations (e.g. [NSPDK](https://dtai.cs.kuleuven.be/drupal/software/nspdk)) and is working on supporting more (e.g. from [Graph Convolution Networks](https://arxiv.org/abs/1910.10685) or [Auto-Encoders](https://www.biorxiv.org/content/10.1101/464735v1)).
