#!/usr/bin/python3

import os

configDir = "./data"
configFile = configDir+"/config"

if __name__ == "__main__":
    print("Bot Token can be obtained from the Discord Developer Portal: https://discord.com/developers/applications")
    while True:
        token = input("Discord bot token: ")
        if token == "":
            print("A token cannot be empty")
        else:
            break
    
    print("")
    print("")


    print("Users with this role can use the commands for administrators.")
    adminRole = input("Administrator role (Administrator): ")
    if adminRole == "":
        adminRole = "Administrator"
    print("")
    print("")


    print("This role will be assigned to the user after registration.")
    regRole = input("User role (User): ")
    if regRole == "":
        regRole = "User"
    print("")
    print("")


    print("Each command will begin with this prefix.")
    print("This is to avoid conflict between multiple bots.")
    cmdPrefix = input("Discord bot token (/): ")
    if cmdPrefix == "":
        cmdPrefix = "/"
    print("")
    print("")


    print("These contacts will appear in the help and error message.")
    print("This will help people contact you in case of problems.")
    print("Example contact information: Jon Dyson <mymail@example.com>")
    botAdminContacts = input("Bot administrator contacts: ")
    print("")
    print("")


    print("The localization only affects the messages you send to Discord.")
    print("List of available localizations:")
    print(os.listdir("./locale"))
    botLocale = input("Locale (en_US): ")
    if botLocale == "":
        botLocale = "en_US"
    print("")
    print("")


    # Write
    if not os.path.isdir(configDir):
        os.makedirs(configDir)

    with open(configFile, "w") as file:
        file.write('[bot]\n')
        file.write('Token = '+token+'\n')
        file.write('AdminContacts = '+botAdminContacts+'\n')
        file.write('Locale = '+botLocale+'\n')
        file.write('\n')
        file.write('[cmd]\n')
        file.write('Prefix = '+cmdPrefix+'\n')
        file.write('\n')
        file.write('[role]\n')
        file.write('Admin = '+adminRole+'\n')
        file.write('Reg = '+regRole+'\n')

    print("Config file:", configFile)
