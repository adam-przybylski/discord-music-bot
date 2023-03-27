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

### Command list
- !join, !j, !J - joins voice channel
- !leave, !l, !L - leaves voice channel
- !play, !p, !P [yt link or search phrase] - plays audio from youtube video. If the bot is currently playing, it adds the song to the queue.
- !pause - pause audio
- !resume - resumes audio
- !replay - replays last played audio
- !search [search phrase] - bot sends URL to first result of youtube search engine
- !queue [yt link or search phrase] - adds song to queue
- !skip - skips song
- !sound, !s, !track, !t, !S, !T [number] - plays chosen local song. If no arguments, bot shows list of sounds.
- !clear_queue, !cq - clears queue
- !help - shows commands description
- !start - starts playing random tracks on a loop
- !stop - stops playing random tracks on a loop
- !random_sound - plays random local track
- !load - loads config



