Chapter 4 Creating your own CobberFetcher

import json
import urllib.request
import urllib.parse
import pubchempy as pcp


def fetch_section_data(cid, section_name):
    """
    Helper function to query PubChem PUG-View API for specific section annotations
    (e.g., 'Physical Description', 'Melting Point', 'Toxicological Information').
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading={urllib.parse.quote(section_name)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    extracted_data = []
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                # Recursively parse nested sections to find value strings
                sections = data.get('Record', {}).get('Section', [])
                for sec in sections:
                    for subsec in sec.get('Section', []):
                        for sub_sub in subsec.get('Information', []):
                            val = sub_sub.get('Value', {})
                            if 'StringWithMarkup' in val:
                                for item in val['StringWithMarkup']:
                                    extracted_data.append(item.get('String'))
    except Exception:
        pass  # Return empty if section isn't available

    return extracted_data


def get_compound_report(compound_name):
    """
    Fetches basic properties, physical data, and toxicity records for any given compound.
    """
    print(f"\n==================== Fetching data for: {compound_name.upper()} ====================")

    # 1. Fetch main compound using pubchempy
    compounds = pcp.get_compounds(compound_name, "name")
    if not compounds:
        print(f"Error: Could not find compound '{compound_name}' on PubChem.")
        return

    compound = compounds[0]
    cid = compound.cid

    # 2. Extract Basic Data
    print("\n--- Basic Identifiers ---")
    print(f"PubChem CID       : {cid}")
    print(f"IUPAC Name        : {compound.iupac_name}")
    print(f"Molecular Formula : {compound.molecular_formula}")
    print(f"Molecular Weight  : {compound.molecular_weight} g/mol")
    print(f"SMILES String     : {compound.canonical_smiles}")
    print(f"XLogP             : {compound.xlogp}")

    # 3. Fetch Experimental Physical Properties via PUG-View
    print("\n--- Physical Properties ---")
    melting_points = fetch_section_data(cid, "Melting Point")
    boiling_points = fetch_section_data(cid, "Boiling Point")
    solubility = fetch_section_data(cid, "Solubility")

    print(f"Melting Point     : {melting_points[0] if melting_points else 'Data not available'}")
    print(f"Boiling Point     : {boiling_points[0] if boiling_points else 'Data not available'}")
    print(f"Solubility        : {solubility[0] if solubility else 'Data not available'}")

    # 4. Fetch Toxicity Data via PUG-View
    print("\n--- Toxicity Data ---")
    toxicity_info = fetch_section_data(cid, "Non-Human Toxicity Values") or fetch_section_data(cid,
                                                                                               "Toxical Information")

    if toxicity_info:
        # Display top 3 toxicological entries (e.g., LD50 values)
        for i, entry in enumerate(toxicity_info[:3], 1):
            print(f"  {i}. {entry}")
    else:
        print("No specific toxicity endpoint records found.")


if __name__ == "__main__":
    get_compound_report("caffeine")

