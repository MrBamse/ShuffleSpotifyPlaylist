#!/home/mrbamse/.local/pipx/venvs/spotipy/bin/python3

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
unpackedSongIDList = []
songIDList = []
storedPlaylist = {}

#Download playlist

#Do an initial save of the first songs in the playlist
# storedPlaylist[0] = spotify.playlist_items(fromPlaylistURI, offset=0)
# lastResponseLength = len(storedPlaylist[0]['items'])
# totalListLength = lastResponseLength
# print ("Saving part 0 (" + str(lastListLength) + " items)")

#Save all songs from the playlist
nrOfParts = 0
lastResponseLength = 100 #Just to kick the while loop off
totalListLength = 0
while lastResponseLength == 100:
  storedPlaylist[nrOfParts] = spotify.playlist_items(fromPlaylistURI, offset=totalListLength)
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

#Populate the new list with songs in a random order
print ("Shuffle by popping")
while len(unpackedSongIDList):
  #print ("Shuffle by popping remaining: " + str(len(unpackedSongIDList)) + " songs")
  songIDList.append(unpackedSongIDList.pop(random.randrange(len(unpackedSongIDList))))

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

#Upload the rest as
start = 0
end = 0
while  end < totalListLength:
  end += 100
  if end > totalListLength:
    end = totalListLength
  print ("Uploading " + str(start+1) + ":" + str(end))
  if start == 0:
    spotify.playlist_replace_items(toPlaylistURI, songIDList[start:end])
  else:
    spotify.playlist_add_items(toPlaylistURI, songIDList[start:end])
  start = end

# #Upload one part as 'replace' first so we get a clean start
# start = 0
# end = len(storedPlaylist[0]['items'])
# print ("Uploading " + str(start+1) + ":" + str(end))
# spotify.playlist_replace_items(toPlaylistURI, songIDList[start:end])

# #Upload the rest as
# currentPart = 1
# while  currentPart <= nrOfParts:
#   start += len(storedPlaylist[currentPart-1]['items'])
#   end += len(storedPlaylist[currentPart]['items'])
#   if currentPart == nrOfParts:
#     end += 1
#     print ("Uploading " + str(start+1) + ":" + str(end-1))
#   else:
#     print ("Uploading " + str(start+1) + ":" + str(end))
#   spotify.playlist_add_items(toPlaylistURI, songIDList[start:end])
#   currentPart += 1

#New way to upload
# print ("Uploading first section to replace list")
# subSectionOfPlaylist = random.choices(songIDList, k=100)
# spotify.playlist_replace_items(toPlaylistURI, subSectionOfPlaylist)

# while len(songIDList) >= 100:
#   print ("Uploading the rest")
#   subSectionOfPlaylist = random.choices(songIDList, k=100)

# if len(songIDList) > 0 & len(songIDList) < 100:
#   print ("Uploading last few songs")
#   subSectionOfPlaylist = random.choices(songIDList, k=(len(songIDList)))

# print ("Done!")
