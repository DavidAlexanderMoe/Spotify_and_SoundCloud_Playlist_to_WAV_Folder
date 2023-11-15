<div align="center">

# Download Spotify and SoundCloud Playlists to a folder of WAV files:
  
### This script downloads music into .WAV - 1536 kbps.
 
</div>

![image](https://github.com/DavidAlexanderMoe/Spotify_and_SoundCloud_Playlist_to_WAV_Folder/assets/122370567/6c8e8dce-f7fd-4fe7-88ee-bc6544e19744)

The idea of this program came from the need to download playlist which were already created directly on spotify or soundcloud (which were large).
Everybody uses some kind of websites or apps to download music or videos from youtube, but the problem was that I did not have any download-ready playlists on youtube!
It is really boring and time consuming to recreate spotify playlists on youtube searching each song individually, so the solution was this code which uses the Spotify and SoundCloud API to get the metadata of all the songs in a playlist and use those informations to download the same songs from Youtube using the Youtube API.

**To download SoundCloud playlists you just need to clone the repository and have the URL of the playlist, while for downloading Spotify playlists you need to setup Spotify following these next steps.**

## How To Use
### 1. Clone the respository

To clone this repoistory using Git, use:

```bash
git clone https://github.com/DavidAlexanderMoe/Spotify_and_SoundCloud_Playlist_to_WAV_Folder
```

### 2. Setting up Spotify

Go to the Spotify [dashboard](https://developer.spotify.com/dashboard/).  Log in. Once at the Dashboard, click the green button labeled "Create App". Just put "Testing", or whatever you want, for both "App name" and "App description". Make sure to check both agreement boxes and click "Create".

You will see the "Client ID" and "Show client secret" fields on the left: copy and save your Client ID and secret somewhere.
You'll also need your spotify username. 
Other instructions come directly from the program.

### 4. Running
Run in your IDE of chioce or just run in your terminal session, making sure you are in the same working directory of the python script.

```bash
python downloader.py
```

If everything goes well, you should see your playlist beginning to download in a folder with the same name.

**Note that some songs, especially soundcloud files, can lead to forbidden access with a consequent non-successful download.**
**Other songs could be difficult to find in WAV quality, so if that was the case just change che best audio setting in the ydl_opts from WAV to mp3**
