import os
import difflib
import ai_search_api.database as no

result = []
req = ''
# Path to the "books" folder
books_path = "books"

def run():
    # Check if the "books" folder exists
    if os.path.exists(books_path) and os.path.isdir(books_path):
        # List of folders in the "books" folder
        books_folders = sorted([folder for folder in os.listdir(books_path) if os.path.isdir(os.path.join(books_path, folder))])
        
        if books_folders:
            for folder in books_folders:
                #print(folder)
                pass
        else:
            print("No results found")
    else:
        print("No results found")

    # Ask the user to input folder names (separated by commas)
    folders_to_open = req.lower().split()

    # Dictionary to keep track of the content of already printed files
    printed_file_content = {}

    # Iterate through the entered folder names
    for folder_name in folders_to_open:
        folder_name = folder_name.strip()  # Remove extra white spaces
        if folder_name not in no.search:
            # Find the most similar folders
            matches = difflib.get_close_matches(folder_name, books_folders, n=len(books_folders), cutoff=0.5)

            # Check if matches were found
            if matches:
                for match in matches:        

                    # Check if the folder exists inside the "books" folder
                    folder_path = os.path.join(books_path, match)
                    if os.path.exists(folder_path) and os.path.isdir(folder_path):
                        # List of files in the specified folder
                        file_list = sorted([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])

                        if file_list:
                            for file_name in file_list:
                                file_path = os.path.join(folder_path, file_name)
                                
                                # Read the content of the file
                                with open(file_path, 'r') as file:
                                    file_content = file.read()
                                
                                # Check if the content of the file has already been printed
                                if file_content not in printed_file_content.values():
                                    result.append(file_content)
                                    # Update the dictionary of printed file contents
                                    printed_file_content[file_name] = file_content
                        else:
                            print('Page not found')
                    else:
                        print('Page not found')
            else:
                if 'https://www.' in folder_name:
                    impare.save_website_text(folder_name)
                else:
                    pass

                if 'http://www.' in folder_name:
                    impare.save_website_text(folder_name)
                else:
                    pass

                if 'website' in folder_name:
                    impare.save_website_text('http://www.' + folder_name)
                else:
                    pass
