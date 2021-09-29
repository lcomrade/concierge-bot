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

import traceback
import configparser
import os
import string
import random
import shutil
from datetime import datetime
import discord

# Read config
config = configparser.ConfigParser()
config.read("./data/config")

botToken = config["bot"]["Token"]
botAdminContacts = config["bot"]["AdminContacts"]
botLocale = config["bot"]["Locale"]

cmdPrefix = config["cmd"]["Prefix"]

roleAdmin = config["role"]["Admin"]
roleReg = config["role"]["Reg"]


# Set bot commands
regCmd = cmdPrefix+"reg"
regCmdLen = len(regCmd)+1

loginCmd = cmdPrefix+"login"
loginCmdLen = len(regCmd)+1

gencodeCmd = cmdPrefix+"gencode"
gencodeCmdLen = len(gencodeCmd)+1

adduserCmd = cmdPrefix+"adduser"
adduserCmdLen = len(adduserCmd)+1

listidCmd = cmdPrefix+"listid"
listidCmdLen = len(listidCmd)

delidCmd = cmdPrefix+"delid"
delidCmdLen = len(delidCmd)+1

setAdminChannelCmd = cmdPrefix+"set-admin-channel"

selfCheckCmd = cmdPrefix+"self-check"

helpCmd = cmdPrefix+"help"


def ReadLocale(lang):
    langFile = os.path.join("./locale", lang)

    print("Load:", langFile)
    with open(langFile, "r") as file:
        global locale
        locale = dict([])

        for line in file.read().splitlines():
            splitLine = line.split(" == ")
            locale[splitLine[0]] = splitLine[1]


    langFileHelp = langFile+"_help"
    print("Load:", langFileHelp)
    with open(langFileHelp, "r") as file:
        global helpTxt

        helpTxt = file.read().format(adduserCmd=adduserCmd, gencodeCmd=gencodeCmd,
        listidCmd=listidCmd, delidCmd=delidCmd,
        setAdminChannelCmd=setAdminChannelCmd,
        selfCheckCmd=selfCheckCmd,
        regCmd=regCmd, loginCmd=loginCmd,
        roleAdmin=roleAdmin,
        roleReg=roleReg,
        botAdminContacts=botAdminContacts)


    # Welcome msg
    if os.path.isfile("./data/welcome"):
        welcomeFile = "./data/welcome"
    else:
        welcomeFile = langFile+"_welcome"

    print("Load:", welcomeFile)
    with open(welcomeFile, "r") as file:
        global welcomeTxt

        welcomeTxt = file.read()


def CheckRole(roleName, roles):
    for role in roles:
        if role.name == roleName:
            return True

    return False


def GetTmpCode():
    dt = datetime.now()
    return str(dt.microsecond)


def GenInviteCode():
    codeLetters = string.ascii_uppercase

    inviteCode = ""
    for _ in range(8):
        inviteCode = inviteCode+random.choice(codeLetters)

    return inviteCode


def WriteBase(serverID, nickname, code):
    serverDir = os.path.join("./data/guilds", str(serverID))
    if not os.path.isdir(serverDir):
        os.makedirs(serverDir)

    # Write file
    invitesFile = os.path.join(serverDir, "invites")
    invitesFileTmp = os.path.join(serverDir, "invites.tmp"+GetTmpCode())
    with open(invitesFileTmp, "a") as file:
        file.write(nickname+"####"+code+"\n")

    # Move file
    os.replace(invitesFileTmp, invitesFile)


def ReadBase(serverID):
    invitesFile = os.path.join("./data/guilds", str(serverID), "invites")
    if not os.path.isfile(invitesFile):
        return []

    with open(invitesFile, "r") as file:
        return file.read()


def UseInviteCode(serverID, inviteCode):
    result = False
    nick = ""

    invitesFile = os.path.join("./data/guilds", str(serverID), "invites")
    if not os.path.isfile(invitesFile):
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


    # Write file
    invitesFileTmp = os.path.join("./data/guilds", str(serverID), "invites.tmp"+GetTmpCode())
    with open(invitesFileTmp, "w") as file:
        file.write(newFile)

    # Move file
    os.replace(invitesFileTmp, invitesFile)

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
    serverDir = os.path.join("./data/guilds", str(serverID))
    if not os.path.isdir(serverDir):
        os.makedirs(serverDir)

    with open(os.path.join(serverDir, "admin_channel"), "w") as file:
        file.write(str(channelID)+"\n")


def ReadAdminChannel(serverID):
    adminChannelFile = os.path.join("./data/guilds", str(serverID), "admin_channel")
    if not os.path.isfile(adminChannelFile):
        return 0

    with open(adminChannelFile, "r") as file:
        return int(file.read().splitlines()[0])


def GetErrText(err, description):
    errList = traceback.extract_tb(err.__traceback__)
    errList = traceback.format_list(errList)
    errFormat = ""
    for line in errList:
        errFormat = errFormat + line
    
    errText = """{ERROR}
`{err}`
`{errMsg}`

{tellAboutError}
*{contacts}*
**======**
{description}
    """.format(ERROR=locale["ERROR:"],
    err=errFormat,
    errMsg=str(err),
    tellAboutError=locale["Contact the bot administrator and tell him about the error."],
    contacts=botAdminContacts,
    description=description
    )
    return errText


# BOT
class BotDiscord(discord.Client):
    async def on_ready(self):
        print("Logged on:", self.user)

    async def on_guild_remove(self, guild):
        shutil.rmtree(os.path.join("./data/guilds", str(guild.id)))

    async def on_member_join(self, member):
        try:
            # Send welcome
            await member.send(welcomeTxt)

            # Check user (LOGIN)
            result, userRole, nick = GetTrustedUser(member.id)

            if result == True:
                roles = member.guild.roles
                for role in roles:
                    if role.name == userRole:
                        await member.edit(roles=[role], reason=None)
                        break

                # Editing user rights
                await member.edit(nick=nick, reason=None)

                # Notifications
                await member.send(locale["{nick}, welcome to the {guild} server"].format(nick=nick, guild=member.guild.name))
                
                adminChannel = self.get_channel(ReadAdminChannel(member.guild.id))
                await adminChannel.send(locale["{discordName} logged on the server as {nick}. Role: {role}"].format(discordName=member.name, nick=nick, role=userRole))

                return


            # Check user (REG)
            result, nick = UseInviteCode(member.guild.id, member.name)

            if result == True:
                roles = member.guild.roles
                for role in roles:
                    if role.name == roleReg:
                        await member.edit(roles=[role], reason=None)
                        break

                # Editing user rights
                await member.edit(nick=nick, reason=None)

                # Notifications
                await member.send(locale["{nick}, welcome to the {guild} server"].format(nick=nick, guild=member.guild.name))
                
                adminChannel = self.get_channel(ReadAdminChannel(member.guild.id))
                await adminChannel.send(locale["{discordName} registered on the server as {nick}"].format(discordName=member.name, nick=nick))


        except discord.errors.Forbidden as err:
            adminChannel = self.get_channel(ReadAdminChannel(member.guild.id))
            await adminChannel.send(GetErrText(err, locale["Check the access rights of the bot."]))


    async def on_message(self, message):
        # Ignore this bot messages
        if message.author == self.user:
            return

        # Ignore DM
        if not message.guild:
            await message.channel.send(locale["This bot does not respond to direct messages"])
            return


        try:
            # Read the message
            # ## HELP ##
            if message.content.startswith(helpCmd):
                await message.channel.send(helpTxt)
                return


            # ## REG ##
            if message.content.startswith(regCmd):
                arg = message.content[regCmdLen:]

                # Sinatxis check
                if arg in ("", " "):
                    await message.channel.send(helpTxt)
                    return


                result, nick = UseInviteCode(message.guild.id, arg)

                if result == True:
                    roles = message.guild.roles
                    for role in roles:
                        if role.name == roleReg:
                            await message.author.edit(roles=[role], reason=None)
                            break

                    # Editing user rights
                    await message.author.edit(nick=nick, reason=None)
                    await message.delete()

                    # Notifications
                    await message.author.send(locale["{nick}, welcome to the {guild} server"].format(nick=nick, guild=message.guild.name))
                    
                    adminChannel = self.get_channel(ReadAdminChannel(message.guild.id))
                    await adminChannel.send(locale["{discordName} registered on the server as {nick}"].format(discordName=message.author.name, nick=nick))

                else:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["wrong secret word"])

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

                    # Editing user rights
                    await message.author.edit(nick=nick, reason=None)
                    await message.delete()

                    # Notifications
                    await message.author.send(locale["{nick}, welcome to the {guild} server"].format(nick=nick, guild=message.guild.name))
                    
                    adminChannel = self.get_channel(ReadAdminChannel(message.guild.id))
                    await adminChannel.send(locale["{discordName} logged on the server as {nick}. Role: {role}"].format(discordName=message.author.name, nick=nick, role=userRole))

                else:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["you are not a trusted user"])

                return


            # ## GENCODE ##
            if message.content.startswith(gencodeCmd):
                arg = message.content[gencodeCmdLen:]

                # Sinatxis check
                if arg in ("", " "):
                    await message.channel.send(helpTxt)
                    return

                # Role check
                if CheckRole(roleAdmin, message.author.roles) == False:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["permission denied"])
                    return

                # Channel check
                if ReadAdminChannel(message.guild.id) != message.channel.id:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["this is not bot administration channel"])
                    return


                for line in arg.split(";; "):
                    inviteCode = GenInviteCode()
                    WriteBase(message.guild.id, line, inviteCode)

                    await message.channel.send(message.guild.name+": "+gencodeCmd+" "+line+" : "+inviteCode)


            # ## ADDUSER ##
            if message.content.startswith(adduserCmd):
                arg = message.content[adduserCmdLen:]

                # Sinatxis check
                if arg in ("", " "):
                    await message.channel.send(helpTxt)
                    return

                # Role check
                if CheckRole(roleAdmin, message.author.roles) == False:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["permission denied"])
                    return

                # Channel check
                if ReadAdminChannel(message.guild.id) != message.channel.id:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["this is not bot administration channel"])
                    return


                for line in arg.split(";; "):
                    WriteBase(message.guild.id, line, line)

                    await message.channel.send(message.guild.name+": "+adduserCmd+" "+line)

                return


            # ## LIST ##
            if message.content.startswith(listidCmd):
                # Role check
                if CheckRole(roleAdmin, message.author.roles) == False:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["permission denied"])
                    return

                # Channel check
                if ReadAdminChannel(message.guild.id) != message.channel.id:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["this is not bot administration channel"])
                    return

                listID = ReadBase(message.guild.id)
                if listID != [] and listID != "":
                    await message.channel.send(listID)

                else:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["ID list is empty"])

                return


            # ## DELID ##
            if message.content.startswith(delidCmd):
                arg = message.content[delidCmdLen:]

                # Sinatxis check
                if arg in ("", " "):
                    await message.channel.send(helpTxt)
                    return

                # Role check
                if CheckRole(roleAdmin, message.author.roles) == False:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["permission denied"])
                    return

                # Channel check
                if ReadAdminChannel(message.guild.id) != message.channel.id:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["this is not bot administration channel"])
                    return


                for line in arg.split(";; "):
                    result, nick = UseInviteCode(message.guild.id, line)
                    if result == True:
                        await message.channel.send(message.guild.name+": "+delidCmd+" "+line)

                    else:
                        await message.channel.send(message.guild.name+": "+delidCmd+" "+line+": "+locale["not found"])

                return


            # ## set-admin-channel ##
            if message.content.startswith(setAdminChannelCmd):
                # Role check
                if CheckRole(roleAdmin, message.author.roles) == False:
                    await message.channel.send("<@"+str(message.author.id)+">, "+locale["permission denied"])
                    return

                WriteAdminChannel(message.guild.id, message.channel.id)
                await message.channel.send(locale["Channel {channelName} is now used for {selfUser} bot administration"].format(channelName=message.channel.name, selfUser=str(self.user)))

                return


            # ## self-check ##
            if message.content.startswith(selfCheckCmd):
                # Checking the existence of admin channel
                adminChannelChk = "NOT FOUND"
                if ReadAdminChannel(message.guild.id) != 0:
                    adminChannelChk = "OK"

                # Checking access rights
                selfReadMessages = "PERMISSION DENIED"
                selfSendMessages = "PERMISSION DENIED"
                selfManageMessages = "PERMISSION DENIED"
                selfManageNicks = "PERMISSION DENIED"
                selfManageRoles = "PERMISSION DENIED"
                
                selfRole = message.guild.self_role.permissions
                if selfRole.administrator == True:
                    selfReadMessages = "OK"
                    selfSendMessages = "OK"
                    selfManageMessages = "OK"
                    selfManageNicks = "OK"
                    selfManageRoles = "OK"

                else:
                    if selfRole.read_messages == True:
                        selfReadMessages = "OK"
                        
                    if selfRole.send_messages == True:
                        selfSendMessages = "OK"

                    if selfRole.manage_messages == True:
                        selfManageMessages = "OK"

                    if selfRole.manage_nicknames == True:
                        selfManageNicks = "OK"
                        
                    if selfRole.manage_roles == True:
                        selfManageRoles = "OK"
                
                # Checking the existence of roles
                roleRegChk = "NOT FOUND"
                roleAdminChk = "NOT FOUND"

                roles = message.guild.roles
                for role in roles:
                    if role.name == roleReg:
                        roleRegChk = "OK"

                    if role.name == roleAdmin:
                        roleAdminChk = "OK"

                    if roleRegChk == "OK" and roleAdminChk == "OK":
                        break


                await message.channel.send("""
**## PERMISSIONS ##**
**[{readMessages}]** Read messages
**[{sendMessages}]** Send messages
**[{manageMessages}]** Manage messages
**[{manageNicks}]** Manage nicknames
**[{manageRoles}]** Manage roles

**## CHANNELS ##**
**[{adminChannelChk}]** Admin channel

**## ROLES ##**
**[{roleRegChk}]** User role ({roleReg})
**[{roleAdminChk}]** Admin role ({roleAdmin})
                """.format(
                readMessages=selfReadMessages,
                sendMessages=selfSendMessages,
                manageMessages=selfManageMessages,
                manageNicks=selfManageNicks,
                manageRoles=selfManageRoles,
                adminChannelChk=adminChannelChk,
                roleRegChk=roleRegChk,
                roleReg=roleReg,
                roleAdminChk=roleAdminChk,
                roleAdmin=roleAdmin))

                return


        except discord.errors.Forbidden as err:
            await message.channel.send(GetErrText(err, locale["Check the access rights of the bot."]))


# Main
if __name__ == "__main__":
    ReadLocale(botLocale)

    intents = discord.Intents.default()
    intents.members = True

    client = BotDiscord(intents=intents)
    client.run(botToken)
