# NCBI_id_grab

This package simply convert bacteria into NCBI ids

## Installation

```bash
pip install NCBI_id_grab
```

## Usage

```python
from NCBI_ID_grab import IDfind

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum']
dict_1 = IDfind.NCBI_ID(bacteria)
print(dict_1)
```
"""