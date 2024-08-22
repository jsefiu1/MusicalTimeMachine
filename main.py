from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id="0235a3d30bc240fc9438a495d70cf9b9",
        client_secret="0235a3d30bc240fc9438a495d70cf9b9",
        show_dialog=True,
        cache_path="token.txt"
    )
)

# Prompt user to authorize
print("Please go to the following URL and authorize access:")
auth_url = sp.auth_manager.get_authorize_url()
print(auth_url)

# Enter the URL the user was redirected to
redirected_url = input("Enter the URL you were redirected to: ")

# Parse the redirected URL to extract the authorization code
sp.auth_manager.get_access_token(request=redirected_url)

user_id = sp.current_user()["id"]
print("User ID:", user_id)

# Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print("Playlist created:", playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Songs added to the playlist.")
