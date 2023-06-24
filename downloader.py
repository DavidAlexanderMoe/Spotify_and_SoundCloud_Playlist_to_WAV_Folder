# Downloads a Spotify playlist into a folder of MP3 tracks

# Import dependencies
import os
import spotipy
import spotipy.oauth2 as oauth2
import yt_dlp
from youtube_search import YoutubeSearch
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from sclib import SoundcloudAPI
import multiprocessing

# # import environment variable dependencies
# from dotenv import load_dotenv
# load_dotenv()

def write_tracks(text_file: str, tracks: dict):
    # Writes the information of all tracks in the playlist to a text file. 
    # This includes the name, artist, and spotify URL. Each is delimited by a comma.
    with open(text_file, 'w+', encoding='utf-8') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['external_urls']['spotify']
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    csv_line = track_name + "," + track_artist + "," + track_url + "\n"
                    try:
                        file_out.write(csv_line)
                    except UnicodeEncodeError:  # Most likely caused by non-English song names
                        print("Track named {} failed due to an encoding error. This is \
                            most likely due to this song having a non-English name.".format(track_name))
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results, check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break

def write_playlist(username: str, playlist_id: str):
    results = spotify.user_playlist(username, playlist_id, fields='tracks,next,name')
    playlist_name = results['name']
    text_file = u'{0}.txt'.format(playlist_name, ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}.'.format(results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)
    return playlist_name

# reference .txt file for soundcloud playlist
def create_reference_file(playlist_url, reference_file):
    api = SoundcloudAPI()
    playlist = api.resolve(playlist_url)

    # Create a text file to write the track names
    premiere_list = ["PREMIERE", "Premiere", "[PREMIERE]", "[Premiere]"]
    with open(reference_file, 'w', encoding='utf-8') as file:
        for track in playlist.tracks:
            if any(prem in track.artist for prem in premiere_list):
                artist_ls = track.artist.split()
                # remove premiere from title to search on YouTube with no problems
                del artist_ls[0]
                filename = f'{" ".join(artist_ls)} - {track.title}'
            else:
                filename = f'{track.artist} - {track.title}'
            file.write(filename + '\n')

def find_and_download_songs_spotify(reference_file: str):
    TOTAL_ATTEMPTS = 10
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            temp = line.split(",")
            name, artist = temp[0], temp[1]
            text_to_search = artist + " - " + name
            best_url = None
            attempts_left = TOTAL_ATTEMPTS
            while attempts_left > 0:
                try:
                    results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
                    best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
                    break
                except IndexError:
                    attempts_left -= 1
                    print("No valid URLs found for {}, trying again ({} attempts left).".format(
                        text_to_search, attempts_left))
            if best_url is None:
                print("No valid URLs found for {}, skipping track.".format(text_to_search))
                continue
            # Run you-get to fetch and download the link's audio
            print("Initiating download for {}.".format(text_to_search))
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([best_url])

def find_and_download_songs_soundcloud(reference_file):
    TOTAL_ATTEMPTS = 10
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            temp = line.strip().split(" - ")
            if len(temp) != 2:
                print("Invalid format: ", line.strip())
                continue
            name, artist = temp[1], temp[0]
            text_to_search = f"{artist} - {name}"
            best_url = None
            attempts_left = TOTAL_ATTEMPTS
            while attempts_left > 0:
                try:
                    results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
                    best_url = "https://www.youtube.com{}".format(results_list[0]['url_suffix'])
                    break
                except IndexError:
                    attempts_left -= 1
                    print("No valid URLs found for {}, trying again ({} attempts left).".format(
                        text_to_search, attempts_left))
            if best_url is None:
                print("No valid URLs found for {}, skipping track.".format(text_to_search))
                continue
            # Run yt-dlp to fetch and download the link's audio
            print("Initiating download for {}.".format(text_to_search))
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([best_url])
                

# Multiprocessed implementation of find_and_download_songs
# This method is responsible for manging and distributing the multi-core workload
def multicore_find_and_download_songs(reference_file: str, cpu_count: int):
    # Extract songs from the reference file
    
    lines = []
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            lines.append(line)

    # Process allocation of songs per cpu
    number_of_songs = len(lines)
    songs_per_cpu = number_of_songs // cpu_count

    # Calculates number of songs that dont evenly fit into the cpu list
    # i.e. 4 cores and 5 songs, one core will have to process 1 extra song
    extra_songs = number_of_songs - (cpu_count * songs_per_cpu)

    # Create a list of number of songs which by index allocates it to a cpu
    # 4 core cpu and 5 songs [2, 1, 1, 1] where each item is the number of songs
    #                   Core 0^ 1^ 2^ 3^
    cpu_count_list = []
    for cpu in range(cpu_count):
        songs = songs_per_cpu
        if cpu < extra_songs:
            songs = songs + 1
        cpu_count_list.append(songs)

    # Based on the cpu song allocation list split up the reference file
    index = 0
    file_segments = []
    for cpu in cpu_count_list:
        right = cpu + index
        segment = lines[index:right]
        index = index + cpu
        file_segments.append(segment)
    
    # Prepares all of the seperate processes before starting them
    # Pass each process a new shorter list of songs vs 1 process being handed all of the songs
    processes = []
    segment_index = 0
    for segment in file_segments:
        p = multiprocessing.Process(target = multicore_handler, args=(segment, segment_index,))
        processes.append(p)
        segment_index = segment_index + 1

    # Start the processes
    for p in processes:
        p.start()

    # Wait for the processes to complete and exit as a group
    for p in processes:
        p.join()

# Just a wrapper around the original find_and_download_songs method to ensure future compatibility
# Preserves the same functionality just allows for several shorter lists to be used and cleaned up
def multicore_handler(reference_list: list, segment_index: int):
    # Create reference filename based off of the process id (segment_index)
    reference_filename = "{}.txt".format(segment_index)
    
    # Write the reference_list to a new "reference_file" to enable compatibility
    with open(reference_filename, 'w+', encoding='utf-8') as file_out:
        for line in reference_list:
            file_out.write(line)

    # Call the original find_and_download method
    find_and_download_songs_spotify(reference_filename)    

    # Clean up the extra list that was generated
    if(os.path.exists(reference_filename)):
        os.remove(reference_filename)


# This is prompt to handle the multicore queries
# An effort has been made to create an easily automated interface
# Autoeneable: bool allows for no prompts and defaults to max core usage
# Maxcores: int allows for automation of set number of cores to be used
# Buffercores: int allows for an allocation of unused cores (default 1)
def enable_multicore(autoenable=False, maxcores=None, buffercores=1):
    native_cpu_count = multiprocessing.cpu_count() - buffercores
    if autoenable:
        if maxcores:
            if(maxcores <= native_cpu_count):
                return maxcores
            else:
                print("Too many cores requested, single core operation fallback")
                return 1
        return multiprocessing.cpu_count() - 1
    multicore_query = input("Enable multiprocessing (Y or N): ")
    if multicore_query not in ["Y","y","Yes","YES","YEs",'yes']:
        return 1
    core_count_query = int(input("Max core count (0 for allcores): "))
    if(core_count_query == 0):
        return native_cpu_count
    if(core_count_query <= native_cpu_count):
        return core_count_query
    else:
        print("Too many cores requested, single core operation fallback")
        return 1


# re-organize the files
def reorganize_mp3_files(folder_name):
    folder_path = "C:/Users/david/Desktop/spotify-to-mp3-python-master/"+str(folder_name)
    # loop through all files in the directory
    for filename in os.listdir(folder_path):
        # check if the file is an mp3 file
        if filename.endswith(".wav"):
            if " - " in filename:
                artist, title = filename.split(" - ")[0], filename.split(" - ")[1]
                title = title[:-18]
                new_filename = f"{title} - {artist}.wav"
            else:
                title = filename.split(" - ")[0][:-18]
                new_filename = f"{title}.wav"
            # rename the file
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))


# # load environment variables
# id = os.getenv("CLIENT_ID")
# secret = os.getenv("CLIENT_SECRET")
# user = os.getenv("USER")

if __name__ == "__main__":
    # input for spotify or soundcloud
    website = input("Do you want to download a Spotify of Soundcloud playlist? \nEnter 1 for spotify and 2 for soundcloud: ")
    if int(website) == 1:
        # Parameters   
        client_id = input('Client id: ')
        client_secret = input('Client secret: ')
        username = input('Username:')

        # inputs
        start = input("\nPlaylist URI (type 'help' to get instructions on how to find the URI): ")
        if start == 'help':
            print("\nGo to the playlist you want to download -> ... -> Share -> Hold Ctrl button -> Copy URI \n")
            playlist_uri = input("Right click on the mouse to paste here the URI: ")
            playlist_uri = playlist_uri.split(":")[2]
        else:
            playlist_uri = start.split(":")[2]
        if playlist_uri.find("https://open.spotify.com/playlist/") != -1:
            playlist_uri = playlist_uri.replace("https://open.spotify.com/playlist/", "")
        
        # define multicore
        print("\nType 'Y' and '0' at next steps to correctly download music.")
        multicore_support = enable_multicore(autoenable=False, maxcores=None, buffercores=1)

        # spotify API
        auth_manager = oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        spotify = spotipy.Spotify(auth_manager=auth_manager)
        playlist_name = write_playlist(username, playlist_uri)
        reference_file = "{}.txt".format(playlist_name)

        # Create the playlist folder
        if not os.path.exists(playlist_name):
            os.makedirs(playlist_name)
        os.rename(reference_file, playlist_name + "/" + reference_file)
        os.chdir(playlist_name)

        # Enable multicore support
        if multicore_support > 1:
            multicore_find_and_download_songs(reference_file, multicore_support)
        else:
            find_and_download_songs_spotify(reference_file)

        # re-organize files
        reorganize_mp3_files(playlist_name)

        print("Operation complete.")

    elif int(website) == 2:
        playlist_url = input("\nPlaylist url: ")
        playlist_name = playlist_url.split("/")[-1]
        reference_file = f'{playlist_name}.txt'
        # Create the playlist folder
        if not os.path.exists(playlist_name):
            os.makedirs(playlist_name)
        os.chdir(playlist_name)
        # Create the reference file
        create_reference_file(playlist_url, reference_file)
        # Download songs
        find_and_download_songs_soundcloud(reference_file)
        # Reorganize files
        reorganize_mp3_files(playlist_name)
        print("Operation complete.")
    else:
        print("Stop and run the program again putting either 1 or 2 in the input.")        
