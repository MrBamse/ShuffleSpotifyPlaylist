from os import path
import random
import spotipy
import configparser
import sys

scriptPath = path.dirname(path.realpath(__file__))
cachePath = scriptPath+'/accesstokencache'

config = configparser.ConfigParser()
config.read(scriptPath+'/'+sys.argv[1])

spotify = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        client_id=config.get('APPDATA', 'CLIENT_ID'),
        client_secret=config.get('APPDATA', 'CLIENT_SECRET'),
        redirect_uri=config.get('APPDATA', 'REDIRECT_URI'),
        scope=config.get('APPDATA', 'SCOPE'),
        cache_path=cachePath,
        open_browser=False
    )
)

client_id=config.get('APPDATA', 'CLIENT_ID'),
client_secret=config.get('APPDATA', 'CLIENT_SECRET'),
redirect_uri=config.get('APPDATA', 'REDIRECT_URI'),

#Refreshes access token using refresh token.
#Maybe save date of last refresh and only refresh if > than X days?
refreshaccesstoken=spotipy.oauth2.SpotifyOAuth(client_id=config.get('APPDATA', 'CLIENT_ID'), client_secret=config.get('APPDATA', 'CLIENT_SECRET'), redirect_uri=redirect_uri, scope=config.get('APPDATA', 'SCOPE'), cache_path=cachePath, open_browser='false')
refreshaccesstoken.refresh_access_token(config.get('APPDATA', 'REFRESH_TOKEN'))

fromPlaylistURI = config.get('PLAYLIST', 'FROM_ID')
toPlaylistURI = config.get('PLAYLIST', 'TO_ID')
songIDList = []
myStore = {}

#Do an initial save of the first songs in the playlist
myStore[0] = spotify.playlist_items(fromPlaylistURI, offset=0)
listLength = len(myStore[0]['items'])
control = len(myStore[0]['items'])
print ("Saving part 0 (" + str(len(myStore[0]['items'])) + "items)")

#Save all songs from the playlist
nrOfParts = 0
while control == 100:
  nrOfParts += 1
  myStore[nrOfParts] = spotify.playlist_items(fromPlaylistURI, offset=listLength)
  control = len(myStore[nrOfParts]['items'])
  listLength += len(myStore[nrOfParts]['items'])
  print ("Saving part " + str(nrOfParts) + " (" + str(len(myStore[nrOfParts]['items'])) + "items)")
print ("A total of " + str(listLength) + " items found")

#Loop through each iteration of the stored list and save the songs in a list instead.
currentPart = 0
while  currentPart <= nrOfParts:
  print ("Unpacking part " + str(currentPart))
  for song in myStore[currentPart]['items']:
    #Create a list with track-IDs (cant preserve any other data, that I know of.
    songIDList.append(song['track']['id'])

  currentPart += 1

#Shuffle the shit
print ("Shuffling")
random.shuffle(songIDList)

#Upload one part as 'replace' first so we get a clean start
start = 0
end = len(myStore[0]['items'])
print ("Uploading " + str(start+1) + ":" + str(end))
spotify.playlist_replace_items(toPlaylistURI, songIDList[start:end])

#Upload the rest as 'add'
currentPart = 1
while  currentPart <= nrOfParts:
  start += len(myStore[currentPart-1]['items'])
  end += len(myStore[currentPart]['items'])
  if currentPart == nrOfParts:
    end += 1
    print ("Uploading " + str(start+1) + ":" + str(end-1))
  else:
    print ("Uploading " + str(start+1) + ":" + str(end))
  spotify.playlist_add_items(toPlaylistURI, songIDList[start:end])
  currentPart += 1
