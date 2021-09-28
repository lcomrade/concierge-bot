[![Docker Hub](https://img.shields.io/docker/v/lcomrade/concierge-bot?sort=date&style=flat-square)](https://hub.docker.com/r/lcomrade/concierge-bot)
[![License](https://img.shields.io/github/license/lcomrade/concierge-bot?style=flat-square)](https://github.com/lcomrade/concierge-bot/blob/main/LICENSE)

**Concierge Bot** is a Discord bot that acts as a concierge.
It lets members onto the Discord server by correct nicks or by invite codes.

## Using
### Bot installation
```
# Installing Docker
apt install docker docker.io

# Creating a data dir
mkdir -p /opt/concierge-bot/data/

# Configuration
docker run -i -t -v /opt/concierge-bot/data:/bot/data lcomrade/concierge-bot python /bot/configure.py
```

### Getting the bot token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click to the `New Application` button
3. Go to the `BOT` tab
4. Click to the `Add Bot` button
5. Scroll down to the `Privileged Gateway Intents` section
6. Enable `Server Members Intent`
7. The bot token is available on this page above

### Setting up the Discord server
1. Add a bot to the Discord server
2. Create the administrator role that you specified during installation
3. Create the user role that you specified during installation
4. Add administrator role to yourself
5. Create a channel that only administrators can read
6. Send a command to the administration channel: `/set-admin-channel`
7. To find out all the available commands, use the help: `/help`

## Documentation
- [Global configuration](https://github.com/lcomrade/concierge-bot/blob/main/docs/global_configuration.md)
- [datamod.sh tool](https://github.com/lcomrade/concierge-bot/blob/main/docs/datamod_tool.md)
- [Creating localization files](https://github.com/lcomrade/concierge-bot/blob/main/docs/create_locale.md)

## Bugs and Suggestion
If you find a bug or have a suggestion, create an Issue [here](https://github.com/lcomrade/concierge-bot/issues)
