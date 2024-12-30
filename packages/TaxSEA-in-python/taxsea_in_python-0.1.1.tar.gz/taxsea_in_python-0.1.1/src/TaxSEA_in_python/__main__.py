import os
import sys

if not __package__:
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

from NCBI_ID_grab import IDfind

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum']
IDfind.NCBI_ID(bacteria)