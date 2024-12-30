# Testing the package for small size
from TaxSEA_in_python import get_IDs

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum'] # Input must be a list.

# Converting bacterial names into NCBI ID
bacterial_ID = get_IDs.NCBI(bacteria) 

# Finding the Taxons correspond to those bacterial names.
bacterial_taxon = get_IDs.Taxon(bacteria)
print(bacterial_taxon)