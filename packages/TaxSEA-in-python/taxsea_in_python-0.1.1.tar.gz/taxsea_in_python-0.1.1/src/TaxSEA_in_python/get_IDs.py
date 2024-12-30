# Convering bacterial name into NCBI_ID: 
# 2 main methods, find local source, if does exist or come out as NULL, then search for online sources (NCBI website)

import pandas as pd
import requests
import re
import importlib.resources
import pickle

def NCBI(bacterial_list):
    """
    """
    def load_database():
        with importlib.resources.files("NCBI_ID_grab.data").joinpath("Local_NCBI_db.csv").open("r") as f:
            return pd.read_csv(f, dtype={'NCBI_IDs': str})

    def find_NCBI_ID_from_NAME(bacterial_name, df=load_database()):
        """
        To find a NCBI_ID given a bacterial name
        Input: bacterial name (str)
        Output: ID (str)
        """
        try:
            # Finding the ID of given species:
            ID = df.loc[df['Species'] == bacterial_name, 'NCBI_IDs'].iloc[0]
            return ID
        except IndexError:
            raise IndexError(f"Bacterial name '{bacterial_name}' not found in the database.")
        
    def find_NCBI_ID_from_name_ONLINE(bacterial_name):
        """

        """
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        esearch_url = f"{base_url}esearch.fcgi?db=taxonomy&term={requests.utils.quote(bacterial_name)}&retmode=xml"
            
        # Retrieve the XML data
        response = requests.get(esearch_url)
        xml_data = response.text
            
        # Extract the taxonomy ID using regex
        id_match = re.findall(r"<Id>(\d+)</Id>", xml_data)
            
        # Return the taxonomy ID
        if id_match:
            return id_match[0]
        else:
            print(f"Warning: No taxonomy ID found for taxon: {bacterial_name}")
            return None
        
    bacterial_id_dict = {}
    for bacteria in bacterial_list:
        try:
            # Attempt to find the NCBI ID locally
            id = find_NCBI_ID_from_NAME(bacteria)
            bacterial_id_dict[bacteria] = id
            # print(f"Found local ID for {bacteria}: {id}")
            
        except IndexError:
            # If not found locally, fetch it online
            id = find_NCBI_ID_from_name_ONLINE(bacteria)
            bacterial_id_dict[bacteria] = id
            # print(f"Fetched online ID for {bacteria}: {id}")
    return bacterial_id_dict



TAXON_IDs = "/home/cong_pham/TAXsea_project/R_in_Python/TaxSEA_DB.plk"

def Taxon(taxon_to_fetch):   
    """
    To find the taxon group that match the NCBI id
    Input: bacterial_names 
    Output: a dictionary of Taxon that matches to the NCBI ids of those bacteria
    """
    def open_pkl(file_location):
        with open(file_location, "rb") as file:
            loaded_data = pickle.load(file)
        return loaded_data

    bacterial_ids = NCBI(taxon_to_fetch)
    
    TAXON_IDs_dicts = open_pkl(TAXON_IDs)
    # print(TAXON_IDs_dicts)

    matching_dict = {Taxon_name: ncbi_ids for Taxon_name, ncbi_ids in TAXON_IDs_dicts.items() 
                     if any(ids in ncbi_ids for ids in bacterial_ids.values())}

    return matching_dict    

