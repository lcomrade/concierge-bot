#!/usr/bin/python3
'''
  Copyright 2021 Leonid Maslakov

  License: GPL-3.0-or-later

  This file is part of concierge-bot.

  concierge-bot is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  concierge-bot is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with concierge-bot.  If not, see <https://www.gnu.org/licenses/>.
'''

import configparser
import os
import string
import random
import shutil
import discord

# Read config
config = configparser.ConfigParser()
config.read("./data/config")

# Set bot commands
regCmd = config["cmd"]["Prefix"]+"reg"
regCmdLen = len(regCmd)+1

loginCmd = config["cmd"]["Prefix"]+"login"
loginCmdLen = len(regCmd)+1

gencodeCmd = config["cmd"]["Prefix"]+"gencode"
gencodeCmdLen = len(gencodeCmd)+1

adduserCmd = config["cmd"]["Prefix"]+"adduser"
adduserCmdLen = len(adduserCmd)+1

listidCmd = config["cmd"]["Prefix"]+"listid"
listidCmdLen = len(listidCmd)

delidCmd = config["cmd"]["Prefix"]+"delid"
delidCmdLen = len(delidCmd)+1

setAdminChannelCmd = config["cmd"]["Prefix"]+"set-admin-channel"
setAdminChannelCmdLen = len(setAdminChannelCmd)

fullEraseDataCmd = config["cmd"]["Prefix"]+"FULL-ERASE-DATA"
fullEraseDataCmdLen = len(fullEraseDataCmd)

helpCmd = config["cmd"]["Prefix"]+"help"

helpTxt = '''
**Usage:** COMMAND [ARGUMENTS]...

*Administrator commands:*
**'''+adduserCmd+'''** INTERNAL_NICKNAME_1;; INTERNAL_NICKNAME_2...
    Adds a user to the guest list, and his INTERNAL_NICKNAME will be used during registration

**'''+gencodeCmd+'''** INTERNAL_NICKNAME_1;; INTERNAL_NICKNAME_2...
    Generates a random code, after registration the user will be renamed according to his INTERNAL_NICKNAME

**'''+listidCmd+'''**
    Outputs the IDs of users who are allowed to register. Format: INTERNAL_NICKNAME####SECRET_WORD

**'''+delidCmd+'''** SECRET_WORD_1;; SECRET_WORD_2;; SECRET_WORD_3...
    Deletes the invitation.

**'''+setAdminChannelCmd+'''**
    Sets the current channel as a channel for administration commands. There can only be 1 such channel.

**'''+fullEraseDataCmd+'''**
    Deletes information about this Discord server from the server on which the bot is running.
    If you just kick the bot from the server this information will not be deleted.

*User commands:*
**'''+regCmd+'''** SECRET_WORD
The secret word should be given to you by the administrator.
It can be an internal nickname or a randomly generated code.

**'''+loginCmd+'''**
Allows a trusted user to log in without requiring a secret word.
The list of trusted users is defined by the bot administrator globally.

*Roles:*
**'''+config["role"]["Admin"]+'''** - user with this role can configure the bot
**'''+config["role"]["Reg"]+'''** - this role is assigned to the user after successful registration

Bot administrator contacts:
*'''+config["bot"]["AdminContacts"]+'''*
'''

def CheckRole(roleName, roles):
    for role in roles:
        if role.name == roleName:
            return True

    return False


def GenInviteCode():
    codeLetters = string.ascii_uppercase

    inviteCode = ""
    for i in range(8):
        inviteCode = inviteCode+random.choice(codeLetters)

    return inviteCode


def WriteBase(serverID, nickname, code):
    serverDir = os.path.join("./data", str(serverID))
    if not os.path.isdir(serverDir):
        os.makedirs(serverDir)
    
    with open(os.path.join(serverDir, "invites"), "a") as file:
        file.write(nickname+"####"+code+"\n")


def ReadBase(serverID):
    serverDir = os.path.join("./data", str(serverID))
    if not os.path.isfile(serverDir+"/"+"invites"):
        return []
    
    with open(os.path.join(serverDir, "invites"), "r") as file:
        return file.read()
    

def UseInviteCode(serverID, inviteCode):
    result = False
    nick = ""

    serverDir = os.path.join("./data", str(serverID))
    invitesFile = os.path.join(serverDir, "invites")
    if not os.path.isfile(serverDir+"/"+"invites"):
        return result, nick


    newFile = ""
    with open(invitesFile, "r") as file:
        for line in file.read().splitlines():
            splitLine = line.split("####")
            
            if splitLine[1] == inviteCode:
                result = True
                nick = splitLine[0]
                
            else:
                newFile = newFile+line+"\n"


    with open(invitesFile, "w") as file:
        file.write(newFile)

    return result, nick


def GetTrustedUser(userID):
    userIDStr = str(userID)

    if not os.path.isfile("./data/trusted_users"):
        return False, "", ""

    with open("./data/trusted_users", "r") as file:
        for line in file.read().splitlines():
            splitLine = line.split("####")

        if splitLine[0] == userIDStr:
            return True, splitLine[1], splitLine[2]

    return False, "", ""


def WriteAdminChannel(serverID, channelID):
    serverDir = os.path.join("./data", str(serverID))
    if not os.path.isdir(serverDir):
        os.makedirs(serverDir)

    with open(os.path.join(serverDir, "admin_channel"), "w") as file:
        file.write(str(channelID)+"\n")


def ReadAdminChannel(serverID, channelID):
    serverDir = os.path.join("./data", str(serverID))
    adminChannelFile = os.path.join(serverDir, "admin_channel")
    if not os.path.isfile(adminChannelFile):
        return ""

    with open(adminChannelFile, "r") as file:
        return int(file.read().splitlines()[0])


# BOT
class BotDiscord(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)
    
    async def on_message(self, message):
        # Ignore DM messages
        if not message.guild:
            return
    
        # Ignore this bot messages
        if message.author == self.user:
            return


        # Read the message
        # ## HELP ##
        if message.content.startswith(helpCmd):
            await message.channel.send(helpTxt)
            return

        
        # ## REG ##
        if message.content.startswith(regCmd):
            arg = message.content[regCmdLen:]
            
            # Sinatxis check
            if arg == "" or arg == " ":
                await message.channel.send(helpTxt)
                return

            
            result, nick = UseInviteCode(message.guild.id, arg)
            
            if result == True:
                roles = message.guild.roles
                for role in roles:
                    if role.name == config["role"]["Reg"]:
                        await message.author.edit(roles=[role], reason=None)
                        break

                await message.author.send(nick+", welcome to the "+message.guild.name+" server")
                await message.author.edit(nick=nick, reason=None)

            else:
                await message.channel.send("<@"+str(message.author.id)+">, wrong secret word")

            return

        # ## LOGIN ##
        if message.content.startswith(loginCmd):
            result, userRole, nick = GetTrustedUser(message.author.id)

            if result == True:
                roles = message.guild.roles
                for role in roles:
                    if role.name == userRole:
                        await message.author.edit(roles=[role], reason=None)
                        break

                await message.author.send(nick+", welcome to the "+message.guild.name+" server")
                await message.author.edit(nick=nick, reason=None)

            else:
                await message.channel.send("<@"+str(message.author.id)+">, you are not a trusted user")

            return

        
        # ## GENCODE ##
        if message.content.startswith(gencodeCmd):
            arg = message.content[gencodeCmdLen:]
            
            # Sinatxis check
            if arg == "" or arg == " ":
                await message.channel.send(helpTxt)
                return

            # Role check
            if CheckRole(config["role"]["Admin"], message.author.roles) == False:
                await message.channel.send("<@"+str(message.author.id)+">, permission denied")
                return

            # Channel check
            if ReadAdminChannel(message.guild.id, message.channel.id) != message.channel.id:
                await message.channel.send("<@"+str(message.author.id)+">, this is not bot administration channel")
                return


            for line in arg.split(";; "):
                inviteCode = GenInviteCode()
                WriteBase(message.guild.id, line, inviteCode)

                await message.channel.send(message.guild.name+": "+gencodeCmd+" "+line+" : "+inviteCode)


        # ## ADDUSER ##
        if message.content.startswith(adduserCmd):
            arg = message.content[adduserCmdLen:]
            
            # Sinatxis check
            if arg == "" or arg == " ":
                await message.channel.send(helpTxt)
                return

            # Role check
            if CheckRole(config["role"]["Admin"], message.author.roles) == False:
                await message.channel.send("<@"+str(message.author.id)+">, permission denied")
                return

            # Channel check
            if ReadAdminChannel(message.guild.id, message.channel.id) != message.channel.id:
                await message.channel.send("<@"+str(message.author.id)+">, this is not bot administration channel")
                return


            for line in arg.split(";; "):
                WriteBase(message.guild.id, line, line)
                
                await message.channel.send(message.guild.name+": "+adduserCmd+" "+line)

            return


        # ## LIST ##
        if message.content.startswith(listidCmd):
            # Role check
            if CheckRole(config["role"]["Admin"], message.author.roles) == False:
                await message.channel.send("<@"+str(message.author.id)+">, permission denied")
                return

            # Channel check
            if ReadAdminChannel(message.guild.id, message.channel.id) != message.channel.id:
                await message.channel.send("<@"+str(message.author.id)+">, this is not bot administration channel")
                return

            listID = ReadBase(message.guild.id)
            if listID != []:
                await message.channel.send(listID)

            else:
                await message.channel.send("<@"+str(message.author.id)+">, ID list is empty")

            return


        # ## DELID ##
        if message.content.startswith(delidCmd):
            arg = message.content[delidCmdLen:]
            
            # Sinatxis check
            if arg == "" or arg == " ":
                await message.channel.send(helpTxt)
                return

            # Role check
            if CheckRole(config["role"]["Admin"], message.author.roles) == False:
                await message.channel.send("<@"+str(message.author.id)+">, permission denied")
                return

            # Channel check
            if ReadAdminChannel(message.guild.id, message.channel.id) != message.channel.id:
                await message.channel.send("<@"+str(message.author.id)+">, this is not bot administration channel")
                return


            for line in arg.split(";; "):
                result, nick = UseInviteCode(message.guild.id, line)
                if result == True:
                    await message.channel.send(message.guild.name+": "+delidCmd+" "+line)

                else:
                    await message.channel.send(message.guild.name+": "+delidCmd+" "+line+": not found")

            return


        # ## set-admin-channel ##
        if message.content.startswith(setAdminChannelCmd):
            # Role check
            if CheckRole(config["role"]["Admin"], message.author.roles) == False:
                await message.channel.send("<@"+str(message.author.id)+">, permission denied")
                return

            WriteAdminChannel(message.guild.id, message.channel.id)
            await message.channel.send("Channel **"+message.channel.name+"** is now used for **"+str(self.user)+"** bot administration")

            return


        # ## full-erase-data ##
        if message.content.startswith(fullEraseDataCmd):
            # Role check
            if CheckRole(config["role"]["Admin"], message.author.roles) == False:
                await message.channel.send("<@"+str(message.author.id)+">, permission denied")
                return

            # Channel check
            if ReadAdminChannel(message.guild.id, message.channel.id) != message.channel.id:
                await message.channel.send("<@"+str(message.author.id)+">, this is not bot administration channel")
                return

            try:
                shutil.rmtree(os.path.join("./data", str(message.guild.id)))
                await message.channel.send("**Information** about Discord server "+message.guild.name+" has been completely **removed** from the "+str(self.user)+" bot server")

            except Exception as err:
                await message.channel.send(str(err))
                await message.channel.send("**ERROR: Discord server information could not be deleted. Contact the bot administrator and ask him to delete the information manually.**")


# Main
if __name__ == "__main__":
    client = BotDiscord()
    client.run(config["bot"]["Token"])
