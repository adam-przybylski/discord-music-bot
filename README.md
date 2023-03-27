# discord-music-bot
Discord bot which is able to play local music files and music from yotube.

### Requirements
- Python 3.8 or higher and pip
- discord.py library
- discord.py[voice] library

On Linux environments, installing voice requires getting the following dependencies:
- libffi
- libnacl
- python3-dev

More details [here](https://discordpy.readthedocs.io/en/stable/intro.html)

Other requirements:
- dotenv [library](https://pypi.org/project/python-dotenv/)

### config.json description
The bot can block songs whose title contains keywords selected by user. For example, if you don't like Harry Styles songs you can write "Harry Styles" in "forbidden" section, so bot will not play any song that has "Harry Styles" in a title.

After trying to play banned song bot sends "[forbidden keyword] [message]" message. You can insert your own message in forbidden_mess section.

Section "sounds" contains list of titles of local music files. To add new local music files you have to:
1. Create folder named "tracks".
2. Paste song to this folder (the song file must have .mp3 extension).
3. Add song title (without extension) in "sounds" section.

!start commands enables playing random local music files on loop. "sound_loop_sleep_time" is a time beetween playing two tracks (in seconds).

The bot is able to react to chosen keywords with specific message. In "answers" section insert "keyword":"answer".

"activity status" - status of bot seen on Discord


