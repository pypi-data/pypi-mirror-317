from requests import get
import ai_search_api.database as db

# Function to download the content of the file main.py from GitLab and save it in database.txt
def update():
    url_to_copy_page = "https://gitlab.com/neopad/api/-/raw/main/no_search/main.py"
    
    # Perform a GET request to obtain the content from the GitLab site
    response = get(url_to_copy_page)
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Request successful.")
        
        # Extract the content of the page
        page_content = response.text
        
        # Save the content in the file database.py
        with open('ai_search_api.database', 'w') as file:
            file.write(page_content)
        
        print("Content Updated")
    else:
        print(f"Failed request")

update()