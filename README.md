# Download Spotify Playlist to folder:

This script downloads music into one of the best audio qualities: **.wav**.

The idea of this program came from the need to download playlist which were already created directly on spotify (which were large).
Everybody uses some kind of websites or apps to download music or videos from youtube, but the problem was that I did not have any download-ready playlists on youtube!
It is really boring and time consuming to recreate spotify playlists on youtube searching each song individually, so the solution was this code which uses the Spotify API to get the metadata of all the songs in a playlist and use those informations to download the same songs from Youtube using the Youtube API.

## How To Use
### 1. Clone the respository

To clone this repoistory using Git, use

```bash
git clone https://github.com/DavidAlexanderMoe/spotify_playlist_to_mp3_folder
```

Alternatively, you can clone this repository directly from github, then open a terminal session and navigate to this folder, using `cd`.

```bash
cd spotify-to-mp3-python/
```

### 2. Setting up Spotify

Go to the Spotify [dashboard](https://developer.spotify.com/dashboard/).  Log in. Once at the Dashboard, click the green button labeled "Create App". Just put "Testing", or whatever you want, for both "App name" and "App description". Make sure to check both agreement boxes and click "Create".

You will see the "Client ID" and "Show client secret" fields on the left: copy and save your Client ID and secret somewhere.
You'll also need your spotify username. 
Other instructions come directly from the program.

### 4. Running

Run in your IDE of chioce or just run in your terminal session, making sure you are in the same working directory of the python script:

```bash
python3 downloader.py
```

If everything goes well, you should see your playlist beginning to download in a folder with the same name.
