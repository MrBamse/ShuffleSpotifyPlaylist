# Spotify Playlist Shuffler

## Why?

Spotify built in shuffle sucks and it's been a hot topic for years in the Spotify forums, yet nothing acceptable have been made.

## Features
- Handles playlists of unlimited size.
- Can shuffle from one playlist (source) to another (destination).
- Easily shuffle multiple playlist by passing .cfg-file as argument.

## Requirements

 - [A Spotify account](https://spotify.com/)
 - Python 3.x
 - [Spotipy](https://github.com/plamere/spotipy)

## Usage

1. Login with your Spotify account and create an app (found under dashboard) here: https://developer.spotify.com/
2. Copy "Client ID" and "Client Secret".
3. Add any URL as Redirect URL (under Edit Settings).
4. Go to https://open.spotify.com/ and click the playlist you want to shuffle (if you want to use one playlist as source and another as destination/shuffled then do this step twice).
5. Make note of the playlist ID in the URL.
6. Go to https://spotify-refresh-token-generator.netlify.app/ and get a "refresh token" (mark scopes "playlist-modify-public" and "playlist-modify-private").
7. Populate config.cfg with your data and you are GOOD TO GO! :)

## Run
### Cronjob Example:
0 4 * * * /usr/bin/python3 /home/user/scripts/Shuffler/shuffler.py playlist-A.cfg
1 4 * * * /usr/bin/python3 /home/user/scripts/Shuffler/shuffler.py playlist-B.cfg
2 4 * * * /usr/bin/python3 /home/user/scripts/Shuffler/shuffler.py playlist-C.cfg
