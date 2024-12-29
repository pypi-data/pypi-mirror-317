import pandas as pd
from astropy.io import fits
import os

def xlsx_to_fits(input_file, output_file):
    """
    Convert an XLSX file to a FITS file.

    Parameters:
        input_file (str): Path to the input XLSX file.
        output_file (str): Path to the output FITS file.
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file {input_file} does not exist.")

    # Read the Excel file using pandas
    try:
        data = pd.read_excel(input_file, sheet_name=None)  # Read all sheets
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file: {e}")

    # Create a list of HDUs
    hdu_list = [fits.PrimaryHDU()]  # Primary HDU

    for sheet_name, df in data.items():
        # Create a BinTableHDU from DataFrame
        hdu = fits.BinTableHDU.from_columns([
            fits.Column(name=col, array=df[col].values, format="A" if df[col].dtype == object else "E")
            for col in df.columns
        ])
        hdu.header['EXTNAME'] = sheet_name  # Set the sheet name as the extension name
        hdu_list.append(hdu)

    # Write to the FITS file
    hdul = fits.HDUList(hdu_list)
    hdul.writeto(output_file, overwrite=True)

    print(f"Successfully converted {input_file} to {output_file}.")
