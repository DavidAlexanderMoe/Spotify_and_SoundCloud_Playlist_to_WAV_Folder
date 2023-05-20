# Download Spotify Playlist to local folder

<<<<<<< HEAD
The idea of this program came from the need to download playlist which were already created directly on spotify (which were large).
Everybody uses some kind of websites or apps to download music or videos from youtube, but my problem was that i did not have any download-ready playlists on youtube!
It was really boring and time consuming to recreate my spotify playlists on youtube (i needed to search each single song and add it to the new youtube playlist), so I thought i could use the Spotify API to get the metadata of all the songs in a playlist and use those informations to download the same songs from Youtube using the Youtube API!
=======
Uses the Spotify API to get the metadata of the songs in a playlist given the playlist's URI and uses those information to download the same songs from Youtube using the Youtube API.
>>>>>>> 4a4245295674c486c13e14ba4ce3c6dd63967ecb

## How To Use
### 1. Clone the respository

To clone this repoistory using Git, use

```bash
git clone https://github.com/DavidAlexanderMoe/spotify_playlist_to_mp3_folder
```

Alternatively, you can clone this repository, open a terminal session and navigate to this folder, using `cd`.

```bash
cd spotify-to-mp3-python/
```

### 2. Setting up Spotify

Go to the Spotify [dashboard](https://developer.spotify.com/dashboard/).  Log in. Once at the Dashboard, click the green button labeled "Create App". Just put "Testing", or whatever you want, for both "App name" and "App description". Make sure to check both agreement boxes and click "Create".

You should see this:

![Spotify App Screen](https://miro.medium.com/max/1400/1*8c7agz6nxmez9-bm2NFCxQ.jpeg)

You will see the "Client ID" and "Show client secret" fields on the left: copy and save your Client ID and secret somewhere.
You'll also need your spotify username. 
Instructions to find the URI are directly in the program.

### 4. Running

Run in your terminal session, making sure you are in the same working directory of the python script:

```bash
python3 spotify_to_mp3.py
```

If all goes well, you should see your playlist beginning to download in a folder with the same name.