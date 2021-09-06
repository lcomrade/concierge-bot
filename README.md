[![License](https://img.shields.io/github/license/lcomrade/concierge-bot?style=flat-square)](https://github.com/lcomrade/concierge-bot/blob/main/LICENSE)

**concierge-bot** is a Discord bot that acts as a concierge.
It lets members onto the Discord server by correct niks or by invite codes.

## Using
### Prepare bot
```
# Installing dependencies
pip3 install --no-cache-dir -r requirements.txt

# Creating config (./data/config)
python3 ./configure.py

# Running
python3 ./main.py
```

### Setting up the Discord server
1. Add a bot to the Discord server
2. Create the administrator role that you specified during preparing
3. Create a channel that only administrators can read
4. Assign yourself to this role
5. Send a command to the admin channel: `/set-admin-channel`
6. To find out all the available commands, use the help: `/help`.

## Bugs and Suggestion
If you find a bug or have a suggestion, create an Issue [here](https://github.com/lcomrade/concierge-bot/issues)
