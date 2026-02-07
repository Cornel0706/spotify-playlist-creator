import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date

clientID = "3614615e49c64e3ba524b72a03384e21"
clientSecret = "e14454b57d6b4892ab10bd8c1d5c2977"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=clientID,
        client_secret=clientSecret,
        show_dialog=True,
        cache_path="token.txt",
        username="Cornel"
    )
)
user_id = sp.current_user()["id"]

# date = input("Which year do you want to travel to ? Type the date in YYYY-MM-DD format: ")  We cannot use input beacuse you need to pay to see the top 100 from other dates then today.

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get("https://www.billboard.com/charts/hot-100/", headers=header)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

top_100 = []
songs_names = soup.select("li ul li h3")
for song in songs_names:
    song_name = song.getText().strip()
    top_100.append(song_name)



today = date.today()
fromatted_date = today.strftime("%Y-%m-%d")
year =  fromatted_date.split("-")[0]

song_uris = []
for songs in top_100:
    result = sp.search(q=f"track:{songs} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{songs} doesn't exist in Spotify. Skipped.")



playlist = sp.user_playlist_create(
    user = user_id, name = f"Top 100 Songs Today {fromatted_date}",
    public = False,
    description = "Top 100 songs from Billboard")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Playlist created successfully!")


