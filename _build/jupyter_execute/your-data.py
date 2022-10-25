#!/usr/bin/env python
# coding: utf-8

# # Standardizing Your Own Molecules

# You may already have your own data, and you would like to link the odorants you've used in one dataset with those from other datasets, or simply be able to do analyses that require your odorants to be well-descibed or featurized. This section will walk you through the logic of standardizing odorant (molecule) identifiers. For researchers interested in contributing their data to the `Pyrfume-Data` repository, see [Part 1](./design-scheme) for a comprehensive overivew of the arhive design standards.

# In[1]:


import pandas as pd
import pyrfume


# `Pyrfume` operates under the principle that the proper identifier for a single odorant molecule (e.g. d-Limonene) is the PubChem compound ID ([440917](https://pubchem.ncbi.nlm.nih.gov/compound/440917)), for a single (known) mixture (e.g. light mineral oil) is the PubChem substance ID ([402315722](https://pubchem.ncbi.nlm.nih.gov/substance/402315722)).
# - A PubChem compound ID uniquely identifies a molecular structure (unlike a CAS registry number).
# - A given structure resolves to only one PubChem ID (unlike a SMILES string which depends on implementation).
# - [PubChem](https://pubchem.ncbi.nlm.nih.gov/) itself is indexed by these IDs and provides a wealth of additional records covering experimental data, computable properties, safety information, and other externally linked data.
# 
# In order to get access to all of this information, and to link the *same molecule* across datasets, the first step is to obtain PubChem IDs (henceforth, CIDs) for the molecules in question.

# In[2]:


names = ['d-limonene', '98-86-2', '(+)-carvone', 'CCCCCC=O', 'GXANMBISFKBPEX-ARJAWSKDSA-N']


# Above we have 5 different molecules, represented with a mix of names (with different annotations), CAS numbers, SMILES strings, and InChiKeys.  Your data may use one of these formats, or a mix of them, or some other format entirely.  The [PubChem exchange identifier](https://pubchem.ncbi.nlm.nih.gov/idexchange/idexchange.cgi) service can do a good job of converting between (some of) these format, or identifying potential CIDs.  `Pyrfume` does the extra work of auto-identifying the current identifier, checking for alternative conversions, and providing information about names that did not match or had multiple matches.

# In[5]:


from pyrfume import get_cids
cids = get_cids(names)


# The process above can be a little bit slow (resolving only a few identifers per second) because the PubChem database itself is not indexed by most of these (only CIDs and InChiKeys).  Still, it returns a dictionary of unique identifiers (CIDs) for each original identifier:

# In[4]:


cids


# Which looks a bit nicer as a Pandas series:

# In[9]:


cids = pd.Series(cids)
cids


# Now that you have unique identifiers, you can access a lot more information:

# In[10]:


from pyrfume import from_cids
info = from_cids(cids.values)


# That part was quite fast and scales very well, because PubChem is indexed by CID.  `Pyrfume` runs this in batches of 100 CIDs, and each batch takes about 1 second.

# In[12]:


molecules = pd.DataFrame(info).set_index('CID')
molecules


# The above contains the original set of molecules, indexed by CID, but also containing some other useful identifiers that (unlike CAS or InChiKey) actually tell you something about the molecule in question just by looking at them.  The "IsomericSMILES" columns is standardized SMILES string computed using the same software (on PubChem) for every molecule.  The "[IUPACName](https://en.wikipedia.org/wiki/IUPAC_nomenclature_of_organic_chemistry)" is similarly, a standardized nomenclature for molecle names.  "name" is simply the most common name (sometimes a trade name) of the molecule, as you might see it in a publication.  CID, IsomericSMILES, and IUPACName, all uniquely describe the molecule.  If you have multiple datasets from multiple sources, and you want to integrate them together, you can use stock Pandas functions for merging and/or concatenating data. 
# 
# This representation for a set of molecules will recur again and again in [Part 5](./published-data), when looking at external datasets.

# Now that you have the molecules from your data in a standard format, save them to disk for future use:

# In[13]:


pyrfume.save_data(molecules, 'my_data/molecules.csv')


# You can load them back again with:

# In[ ]:


molecules = pyrfume.load_data('my_data/molecules.csv')


# You can change the location that `Pyrfume` uses for its (local copy of) the data archives with `pyrfume.set_data_path`.
