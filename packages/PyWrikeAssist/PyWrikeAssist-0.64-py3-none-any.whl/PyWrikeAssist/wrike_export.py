import requests
import json
import time
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from bs4 import BeautifulSoup
import pandas as pd
import os
from PyWrike.gateways import OAuth2Gateway1
from PyWrike import (
    validate_token,
    authenticate_with_oauth2,
    get_all_spaces,
    get_space_id_from_name,
    get_all_folders,
    get_titles_hierarchy,
    get_custom_statuses,
    create_custom_status_mapping,
    get_custom_fields,
    create_custom_field_mapping,
    get_tasks_for_folder,
    get_tasks_details,
    clean_html,
    get_user_details,
    process_space_data    
)

# Updated main function
def export_excel():
    user_cache = {}
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

    access_token = config_df.at[0, "Token"]
    space_name = config_df.at[0, "Space to extract data from"]

    # Handle case when `space_name` is empty or NaN
    if pd.isna(space_name) or space_name.strip() == "":
        space_name = None

    # Validate the token
    if not validate_token(access_token):
        wrike = OAuth2Gateway1(excel_filepath=excel_file)
        access_token = wrike._create_auth_info()
        print(f"New access token obtained: {access_token}")

    # Fetch all spaces
    spaces_response = get_all_spaces(access_token)

    # Handle blank space name
    if not space_name:
        for space in spaces_response:
            space_id = space["id"]
            space_title = space["title"]
            print(f"Processing space: {space_title}")
            process_space_data(space_id, space_title, access_token)
    else:
        space_id = get_space_id_from_name(space_name, spaces_response)
        if not space_id:
            print(f"Space with name '{space_name}' not found.")
            exit()
        process_space_data(space_id, space_name, access_token)

if __name__ == "__export_excel__":
    export_excel()