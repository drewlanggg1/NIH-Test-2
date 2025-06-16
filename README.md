# NIH-Test-2

This repository contains a helper script for extracting principal investigator (PI) information from NIH project JSON files and generating common academic email permutations.

## Usage

1. Install requirements (pandas is needed):
   ```bash
   pip install pandas
   ```
2. Run the script with a path to the JSON file:
   ```bash
   python generate_pi_emails.py path/to/response.json --output nih_pi_emails.csv
   ```
   The output CSV will include the PI name, institution, project title, project detail URL, and generated email permutations.

The script also includes a placeholder function for future email validation integrations (e.g., using Hunter API or SMTP checks).
