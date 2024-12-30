import pandas as pd
import os

# Load CSV data
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'location_data.csv')
    return pd.read_csv(data_path)

def iniknumber(number):
    """Parse the input code and return information."""
    if len(number) != 16:
        return {"error": "Invalid code length. Must be 16 digits."}

    # Load data
    df = load_data()

    # Extract components
    prov_code = number[:2]
    kab_code = f"{number[:2]}.{number[2:4]}"
    kec_code = f"{number[:2]}.{number[2:4]}.{number[4:6]}"
    day = int(number[6:8])
    month = int(number[8:10])
    year = int(number[10:12]) + (1900 if int(number[10:12]) > 50 else 2000)
    seq_number = number[12:]

    # Lookup names
    province = df[df["Code"] == prov_code]["Name"].values[0] if not df[df["Code"] == prov_code].empty else "Unknown Province"
    kabupaten = df[df["Code"] == kab_code]["Name"].values[0] if not df[df["Code"] == kab_code].empty else "Unknown Kabupaten"
    kecamatan = df[df["Code"] == kec_code]["Name"].values[0] if not df[df["Code"] == kec_code].empty else "Unknown Kecamatan"

    # Return results as a dictionary
    return {
        "Province": province,
        "Kabupaten": kabupaten,
        "Kecamatan": kecamatan,
        "Birth Date": f"{day:02d}-{month:02d}-{year}",
        "Sequence Number": seq_number
    }

