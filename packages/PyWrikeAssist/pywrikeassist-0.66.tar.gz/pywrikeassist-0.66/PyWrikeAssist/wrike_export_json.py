import requests
import json
import pandas as pd
import os
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_all_spaces,
    get_space_id_from_name,
    get_all_folders_json,
    save_to_json,
    process_space
)

# Main function to execute the export
def export_json():
    # Load configuration
    excel_file = input("Enter the path to the Excel file: ")
    if not os.path.isfile(excel_file):
        print("File does not exist. Please check the path.")
        exit()
    
    try:
        config_df = pd.read_excel(excel_file, sheet_name="Config", header=1)
    except Exception as e:
        print(f"Failed to read Excel file: {e}")
        exit()

    # Extract token and space name from the Config sheet
    access_token = config_df.at[0, "Token"]
    space_name = config_df.at[0, "Space to extract data from"]

    # Validate token
    if not validate_token(access_token):
        client_id = config_df.at[0, "Client ID"]
        client_secret = config_df.at[0, "Client Secret"]
        redirect_url = config_df.at[0, "Redirect URI"]
        access_token = authenticate_with_oauth2(client_id, client_secret, redirect_url)

    # Fetch all spaces
    spaces_response = get_all_spaces(access_token)

    # Determine if exporting for all spaces
    if pd.isna(space_name) or space_name.strip() == "":
        space_name = None

    if not space_name:
        # Process all spaces
        for space in spaces_response:
            process_space(space, access_token)
    else:
        # Process specific space
        space_id = get_space_id_from_name(space_name, spaces_response)
        if not space_id:
            print(f"Space with name '{space_name}' not found.")
            exit()
        process_space({"id": space_id, "title": space_name}, access_token)

# Execute main function if file is run as a script
if __name__ == "__export_json__":
    export_json()