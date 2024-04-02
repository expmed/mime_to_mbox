import os
import email
from email.policy import default
from mailbox import mbox

# Set your source directory and output file path
source_directory = '/Users/xyz/Downloads/downloaded_mime_mailboxes'
output_dir_name = 'email_output'
current_dir = os.getcwd()
output_dir_path = os.path.join(current_dir, output_dir_name)

print(f"Creating output directory at {output_dir_path} if it doesn't exist...")

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir_path):
    os.makedirs(output_dir_path)

mbox_file_name = 'combined_emails.mbox'
output_mbox_file = os.path.join(output_dir_path, mbox_file_name)

print(f"Preparing to create MBOX file at {output_mbox_file}...")

# Prepare to create an mbox file
mbox = mbox(output_mbox_file)

# Function to extract text content from a part
def get_text_part(part):
    charset = part.get_content_charset() or 'utf-8'  # Default to UTF-8
    content_type = part.get_content_type()
    if content_type == 'text/plain' or content_type == 'text/html':
        payload = part.get_payload(decode=True)
        return payload.decode(charset, errors="replace")
    return ""

# Process each file
for root, _, files in os.walk(source_directory):
    for filename in files:
        filepath = os.path.join(root, filename)
        print(f"Processing file: {filepath}")
        with open(filepath, 'rb') as file:
            msg = email.message_from_binary_file(file, policy=default)
            content = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content += get_text_part(part)
            else:
                content = get_text_part(msg)
            
            # Create a simplified message to add to the mbox
            new_msg = email.message.EmailMessage()
            new_msg.set_content(content)  # Set the concatenated text content
            # Copy headers from original message
            for header in ["From", "To", "Subject", "Date"]:
                if msg[header]:
                    new_msg[header] = msg[header]
            mbox.add(new_msg)
            print(f"Added email to MBOX: Subject: {msg['Subject']}")

mbox.close()
print(f"Conversion complete. Your emails are now in {output_mbox_file}")
