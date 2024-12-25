import os
import shutil
import subprocess
import random
from requests import get
import ai_search_api.update_database

# Function to download the content of the file main.py from GitLab and save it in database.txt
def api_data():
    url_to_copy_page = "https://gitlab.com/neopad/api/-/raw/main/data/data.json"
    
    # Perform a GET request to obtain the content from the GitLab site
    response = get(url_to_copy_page)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful.")
        
        # Extract the page content as a JSON object
        page_content = response.json()  # Use .json() to convert content into a dictionary
        
        print("Content Updated: " + str(page_content))
        
        # Return the value of the "version" key in the dictionary
        return page_content["version"]
    else:
        print(f"Failed request")
        return None  # Return None in case of error

# Call the function to get the version from the API
data_api = api_data()
if data_api:
    print(f"Version obtained: {data_api}")
else:
    print("Unable to obtain the version.")

# Function to delete a folder if it exists
def delete_folder(folder):
    if os.path.exists(folder):
        print(f"Deleting existing folder: {folder}")
        shutil.rmtree(folder)

# Function to clone the repository and copy the 'books' folder
def clone_and_copy_books(repo_url, dest_dir):
    # Delete the 'books' folder if it exists
    delete_folder(dest_dir)

    # Temporary name for the cloning folder
    temp_dir = f"temp_repo/{data_api}"

    # Clone the GitLab repository into the temporary folder
    print("Cloning the repository...")
    subprocess.run(["git", "clone", repo_url, temp_dir])

    # Check if the 'books' folder exists in the cloned repository
    books_dir = os.path.join(temp_dir, "books")
    if os.path.exists(books_dir):
        print("Copying the 'books' folder to the destination...")
        shutil.copytree(books_dir, dest_dir)
    else:
        print("Error: the 'books' folder does not exist in the repository.")

# GitLab repository URL
repo_url = "https://gitlab.com/neopad/api.git"  # Repository URL
dest_dir = "books"  # Local destination folder

# Run the function to clone and copy the files
if data_api:  # Ensure that the version has been successfully obtained
    clone_and_copy_books(repo_url, dest_dir)
else:
    print("Unable to proceed with cloning without a valid version.")
