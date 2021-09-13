# Theory
## Change locale
The locale is controlled by the parameter in the `./data/config`. Read more at `./docs/global_configuration.md`. Example:
```
[bot]
# The localization only affects the messages you send to Discord.
# The localization files are stored in the ./locale dir
Locale = en_US
```

## Localization files
All localization files are stored in the `./locale/` directory.

Two localization files are created for each language: `./locale/LOCALE` and `./locale/LOCALE_help`. Example: `./locale/en_US` and `./locale/en_US_help`

The program will exit with an error if:
 - One of the files of the selected locale is missing
 - There is one line missing from the main locale file
 - One line of the main locale file is missing one of the parameters in brackets (`{}`)

## Localization file format
### ./locale/LOCALE
The main localization file has the following format:

```
LINE == TRANSLATION
LINE == TRANSLATION
```

### ./locale/LOCALE_help
This file contains help for the bot in MarkDown format. If necessary, you can screen Discord MarkDown using `\`.


# Practice
**1.** Start by copying the locale files:

```
cp ./locale/en_US ./locale/LOCALE
cp ./locale/en_US_help ./locale/LOCALE_help
```

**2.** Edit the translation in the files.

**3.** Now you can specify the name of your locale in the bot's config and use.
