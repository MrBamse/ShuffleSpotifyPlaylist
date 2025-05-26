from os import path
import random
import spotipy
import configparser
import sys

def downloadPlaylist(fromPlaylistID):
  nrOfParts = 0
  lastResponseLength = 100 #Just to kick the while loop off
  totalListLength = 0
  unpackedSongIDList = []
  storedPlaylist = {}

  #Save all songs from the playlist
  while lastResponseLength == 100:
    storedPlaylist[nrOfParts] = spotify.playlist_items(fromPlaylistID, offset=totalListLength)
    lastResponseLength = len(storedPlaylist[nrOfParts]['items'])
    totalListLength += lastResponseLength
    print ("Saving part " + str(nrOfParts+1) + " (" + str(lastResponseLength) + " items)")
    nrOfParts += 1
  print ("A total of " + str(totalListLength) + " items found")

  #Loop through each iteration of the stored list and save the songs in a list instead.
  currentPart = 0
  while  currentPart < nrOfParts:
    print ("Unpacking part " + str(currentPart+1))
    for song in storedPlaylist[currentPart]['items']:
      #Create a list with track-IDs (cant preserve any other data, that I know of.
      unpackedSongIDList.append(song['track']['id'])
      #print (song['track']['id'])
    currentPart += 1
  return unpackedSongIDList

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

fromPlaylistID = config.get('PLAYLIST', 'FROM_ID')
toPlaylistID = config.get('PLAYLIST', 'TO_ID')
wantedAmount = config.get('PLAYLIST', 'WANTED_AMOUNT')
unwantedPlaylistID = config.get('PLAYLIST', 'UNWANTED_ID')
songIDList = []
fromPlaylist = []
unwantedPlaylist = []

#Download playlists
fromPlaylist = downloadPlaylist(fromPlaylistID)
if unwantedPlaylistID != "NONE":
  unwantedPlaylist = downloadPlaylist(unwantedPlaylistID)

#Remove unwanted songs
if unwantedPlaylistID != "NONE":
  for songID in unwantedPlaylist:
    fromPlaylist.remove(songID)

#Make sure wantedAmount is reasonable
print(wantedAmount)
if wantedAmount == "ALL":
  print("1")
  wantedAmount = len(fromPlaylist)
elif wantedAmount.isdigit() and wantedAmount.isdigit() < len(fromPlaylist):
  wantedAmount = int(wantedAmount)
elif wantedAmount.isdigit() and wantedAmount.isdigit() > len(fromPlaylist):
  wantedAmount = len(fromPlaylist)
else:
  wantedAmount = 0

#Populate the new list with songs in a random order
print ("Shuffle by popping")
for x in range(wantedAmount):
  songIDList.append(fromPlaylist.pop(random.randrange(len(fromPlaylist))))

#Shuffle the shit
print ("Shuffling once")
random.shuffle(songIDList)
print ("Shuffling twice")
random.shuffle(songIDList)
print ("Shuffling thrise?")
random.shuffle(songIDList)
print ("Shuffling quaize??")
random.shuffle(songIDList)
print ("Shuffling fize???")
random.shuffle(songIDList)

#Upload the songs
start = 0
end = 0
while  end < len(songIDList):
  end += 100
  if end > len(songIDList):
    end = len(songIDList)
  print ("Uploading " + str(start+1) + ":" + str(end))
  if start == 0:
    spotify.playlist_replace_items(toPlaylistID, songIDList[start:end])
  else:
    spotify.playlist_add_items(toPlaylistID, songIDList[start:end])
  start = end

