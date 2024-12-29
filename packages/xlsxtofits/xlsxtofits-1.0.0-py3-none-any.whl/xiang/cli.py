import argparse
from .converter import xlsx_to_fits

def main():
    """
    Command-line interface for the xlsx_to_fits package.
    """
    parser = argparse.ArgumentParser(description="Convert XLSX files to FITS files.")
    parser.add_argument("input_file", help="Path to the input XLSX file.")
    parser.add_argument("output_file", help="Path to the output FITS file.")

    args = parser.parse_args()

    try:
        xlsx_to_fits(args.input_file, args.output_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

