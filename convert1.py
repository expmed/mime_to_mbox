import os
from email.parser import BytesParser
from mailbox import mbox

# Specify the directory containing your MIME-formatted email files
# Change this path to the directory where your emails are located
source_directory = '/Users/xyz/Downloads/downloaded_mime_mailboxes'

# Name of the directory to create in the current directory for the output MBOX file
output_dir_name = 'email_output'

# Get the current working directory
current_dir = os.getcwd()

# Full path for the new output directory
output_dir_path = os.path.join(current_dir, output_dir_name)

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

# Name of the MBOX file to be created inside the new directory
mbox_file_name = 'combined_emails.mbox'

# Full path to the output MBOX file
output_mbox_file = os.path.join(output_dir_path, mbox_file_name)

# Create an mbox file at the specified location
mbox = mbox(output_mbox_file)

# Parser for reading the MIME-formatted email files
parser = BytesParser()

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(source_directory):
    for filename in files:
        filepath = os.path.join(root, filename)
        if os.path.isfile(filepath):
            # Open and parse each MIME email file
            with open(filepath, 'rb') as file:
                try:
                    email = parser.parse(file)
                    # Add the email to the mbox file
                    mbox.add(email)
                except Exception as e:
                    print(f"Skipping file {filepath} due to an error: {e}")

# Close the mbox file to save changes
mbox.close()

print(f"Conversion complete. Your emails are now in {output_mbox_file}")
