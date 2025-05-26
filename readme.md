# Spotify Playlist Shuffler

## Why?

Spotify built in shuffle sucks and it's been a hot topic for years in the Spotify forums, yet nothing acceptable have been made.

## Features
- Handles playlists of unlimited size.
- Can shuffle from one playlist (source) to another (destination).
- Easily shuffle multiple playlist by passing .cfg-file as argument.
- Limit amount of songs copied from source.
- Add a playlist as filter to remove unwanted songs in destination playlist (keeping source playlist intact).

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

## Config file
[APPDATA]  
CLIENT_ID=**Your client ID from step 2 above**  
CLIENT_SECRET=**Your client secret from step 2 above**  
REDIRECT_URI=https://example.com/redirect  
SCOPE=playlist-modify-public playlist-modify-private  
REFRESH_TOKEN=**Your refresh token from step 6 above**  

[PLAYLIST]  
FROM_ID=**Your source playlist ID from step 4 above**  
TO_ID=**Your destination playlist ID from step 4 above**  
WANTED_AMOUNT=**Either "ALL" (all capital) or an integer/number equal or larger than zero.**  
UNWANTED_ID=**Either "NONE" (all capital) or the playlist ID with unwanted songs that you want filtered (ID found as instructed in step 4 above)**

## Run
### Cronjob Example:
0 4 * * * /usr/bin/python3 /home/user/scripts/Shuffler/shuffler.py playlist-A.cfg  
1 4 * * * /usr/bin/python3 /home/user/scripts/Shuffler/shuffler.py playlist-B.cfg  
2 4 * * * /usr/bin/python3 /home/user/scripts/Shuffler/shuffler.py playlist-C.cfg

## Notes
There's not much of error catching in this code so be sure to fill in all required info in the config file.
