[![Docker Hub](https://img.shields.io/docker/v/lcomrade/concierge-bot?label=docker&sort=date&style=flat-square)](https://hub.docker.com/r/lcomrade/concierge-bot)
[![Docker Hub Pulls](https://img.shields.io/docker/pulls/lcomrade/concierge-bot?style=flat-square)](https://hub.docker.com/r/lcomrade/concierge-bot)
[![License](https://img.shields.io/github/license/lcomrade/concierge-bot?style=flat-square)](https://github.com/lcomrade/concierge-bot/blob/main/LICENSE)

**Concierge Bot** is a Discord bot that acts as a concierge.
It lets members onto the Discord server by correct nicks or by invite codes.

## Using
### Bot installation
1. Installing Docker:
```
apt install docker docker.io
```
2. Creating a data dir
```
mkdir -p /var/lib/concierge-bot/
```
3. Creating configuration files
```
docker run -i -t -v /var/lib/concierge-bot:/bot/data lcomrade/concierge-bot python /bot/configure.py
```
4. Adding systemd unit
```
rm -f /etc/systemd/system/concierge-bot.service
wget -O '/etc/systemd/system/concierge-bot.service' 'https://raw.githubusercontent.com/lcomrade/concierge-bot/main/init/concierge-bot.service'
systemctl daemon-reload
```
5. Enabling and starting systemd service
```
systemctl enable concierge-bot
systemctl start concierge-bot
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
