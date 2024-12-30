# TaxSEA_in_python project

This package is a version of TaxSEA but build in python. 

## Installation

```bash
pip install TaxSEA_in_python
```

## Usage

```python
from TaxSEA_in_python import get_IDs

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum'] # Input must be a list.

# Converting bacterial names into NCBI ID
bacterial_ID = get_IDs.NCBI(bacteria) 

# Finding the Taxons correspond to those bacterial names.
bacterial_taxon = get_IDs.Taxon(bacteria)
print(bacterial_taxon)
```
"""