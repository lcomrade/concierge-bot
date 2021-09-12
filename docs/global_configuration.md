All global files are located in the root of the folder `./data`

## ./data/config
This is the main bot configuration file. This file can be created with `./configure.py`

Format: `ini`

```
[bot]
# Bot Token can be obtained from the Discord Developer Portal: https://discord.com/developers/applications
Token = DISCORD_BOT_TOKEN_HERE

# These contacts will appear in the help and error message.
# This will help people contact you in case of problems.
AdminContacts = Jon Dyson <mymail@example.com>

# The localization only affects the messages you send to Discord.
# The localization files are stored in the ./locale dir
Locale = en_US

[cmd]
# Each command will begin with this prefix.
# This is to avoid conflict between multiple bots.
Prefix = /

[role]
# Users with this role can use the commands for administrators.
Admin = Administrator

# This role will be assigned to the user after registration.
Reg = User
```

## ./data/trusted_users
This file is used by the `/login` command.

Format: `custom`

There is an unlimited number of lines in the file, each page is independent of the others.
An example of one line:

```
DISCORD_USER_ID####INTERNAL_ROLE####INTERNAL_NICKNAME
```

File example:

```
123456789000000000####Moderator####Cool Moderator
000012345678900000####Super####Super User
000000000123456789####Moderator####Somebody
```
