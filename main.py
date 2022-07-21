from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = 'YOUR SPOTIFY CLIENT ID'
SPOTIPY_CLIENT_SECRET = 'YOUR SPOTIFY CLIENT SECRET KEY'

sp = spotipy.Spotify(  # documentation explain everything needed to the "parameters" but using alot of spotify own documentation helps
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt")
)

user_id = sp.current_user()["id"]

date = input("Choose a date to make a top 100 songs playlist, in this format please YYYY-MM-DD: ")
year = date.split("-")[0]  # getting the first parte of the list because of the split 0 is the year
URL = f"https://www.billboard.com/charts/hot-100/{date}"  # URL of the top 100 musics on the date of the input
song_uris = []  # lista of object with all the music will be here, using the documentation on songs URIs
response = requests.get(URL)  # seaching the html of billboard website
website = response.text  # transforming the url response in string

soup = BeautifulSoup(website, "html.parser")  # making a beautiful soup object

song_titles = soup.select(selector="li #title-of-a-story")  # selecting music titles from the object
top_100_song = [song.get_text().strip() for song in song_titles]  # list comprehension transforming in strings

for song in top_100_song:
    result = sp.search(q=f"track:{song} year:{year}", type="track")  # searching the songs
    #print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri) # adding all the items (objects) in the list
    except IndexError:  # in case the music in deleted or dont exist in spofity anymore, to no crash have to use except
        print(f"{song} dont exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(  # creating a playlist with the current user, would be better if the documentation
    #  was more easy to explain where the parameters would go from the start
    user=user_id,
    name=f"{date} Billboard 100",  # name of the playlist, dont really need to be this
    public= False,  # private playlist
    collaborative=False,
    description="Python project playlist")  # description that go in the playlist can be whatever you want

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)  # adding everything to the playlist with the
# id playlist and the list with all songs(objects)
