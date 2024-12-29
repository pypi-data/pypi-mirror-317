import os

def main():
    os.system('mkdir -p /tmp/imess')

    # Get messages
    os.system('cp ~/Library/Messages/chat.db /tmp/imess/chat.db')
    if not os.path.exists('/tmp/imess/chat.db'):
        print("Error: Failed to copy chat.db to /tmp/imess/chat.db. Try manually running this command yourself:`cp ~/Library/Messages/chat.db /tmp/imess/chat.db`.")
        exit(1)

    # Get contacts (NOTE: You may need to give permission to the script to access your contacts)
    os.system('osascript create_vcf.scpt')
    if not os.path.exists('/tmp/imess/contacts.vcf'):
        print("Error: Failed to create contacts.vcf. Try manually creating a .vcf file and saving it to `/tmp/imess/contacts.vcf`. Or make sure the Terminal that you are running this script from has Permission to access your Contacts.")
        exit(1)

    print("Success!")

if __name__ == "__main__":
    main()