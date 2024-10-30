# Description: python command line script to retrieve windows owners details for prompted file types when passed path variable at runtime via command line arg
import os
import win32security
import argparse

def get_file_owner(file_path):
    try:
        # Get the security descriptor for the file
        sd = win32security.GetFileSecurity(file_path, win32security.OWNER_SECURITY_INFORMATION)
        
        # Get the owner's SID (Security Identifier)
        owner_sid = sd.GetSecurityDescriptorOwner()
        
        # Convert SID to a readable name
        name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
        
        # Return the owner in the format "DOMAIN\Username"
        return f"{domain}\\{name}"
    except Exception as e:
        print(f"Error retrieving owner for {file_path}: {e}")
        return "Unknown Owner"

def main():
    # Parse the command-line argument
    parser = argparse.ArgumentParser(description="Get file owner information from specified file types in a directory.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing files.")
    args = parser.parse_args()

    # Directory specified in command line
    folder_path = args.folder_path
    
    # Prompt user for file extensions
    extensions = input("Enter file extensions to search for (e.g., .pdf, .txt), separated by commas: ").split(',')
    extensions = [ext.strip().lower() for ext in extensions]  # Clean and lower-case extensions
    
    # Output file saved in the folder where script is run
    output_file = os.path.join(os.getcwd(), 'file_owners.txt')
    file_owner_data = []

    # Loop through the specified folder and process files with the specified extensions
    for file_name in os.listdir(folder_path):
        if any(file_name.lower().endswith(ext) for ext in extensions):
            file_path = os.path.join(folder_path, file_name)
            
            # Print each file name as it's processed
            print(f"Processing file: {file_name}")
            
            owner = get_file_owner(file_path)
            file_owner_data.append((file_name, owner))

    # Write results to the output file
    with open(output_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write("Filename\tOwner\n")
        for file_name, owner in file_owner_data:
            txt_file.write(f"{file_name}\t{owner}\n")

    print(f"File owner information saved to: {output_file}")

# Run the script
if __name__ == "__main__":
    main()
