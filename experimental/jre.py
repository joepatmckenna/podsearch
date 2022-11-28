# # import spotipy
# import savify
# import base64
# import requests

# spotify for developers
# client_id = ""
# client_secret = ""

# token = base64.b64encode(":".join(
#     (client_id, client_secret)).encode()).decode()

# token_response = requests.post(
#     "https://accounts.spotify.com/api/token",
#     headers={
#         "Authorization": f"Basic {token}",
#         "Content-Type": "application/x-www-form-urlencoded"
#     },
#     data={"grant_type": "client_credentials"},
# )
# token_response = token_response.json()
# authorization = f"{token_response['token_type']} {token_response['access_token']}"

# show_id = "4rOoJ6Egrf8K2IrywzwOMk"  # JRE

# url = f"https://api.spotify.com/v1/shows/{show_id}"
# show_response = requests.get(
#     url,
#     headers={
#         "Authorization": authorization,
#         "Content-Type": "application/json"
#     },
#     params={"market": "US"},
# )
# show = show_response.json()
# episodes = show["episodes"]

# for episode in episodes["items"]:
#     print(
#         episode["name"],
#         episode["release_date"],
#         episode["id"],
#         episode["duration_ms"],
#     )
# from savify.logger import Logger

# # savify_client = savify.Savify(
# #     api_credentials=(client_id, client_secret),
# #     quality=savify.types.Quality.BEST,
# #     download_format=savify.types.Format.MP3,
# #     path_holder=savify.utils.PathHolder(downloads_path="/Users/joe/Downloads"),
# #     group="%artist",
# # )
# # savify_client.download(episode["external_urls"]["spotify"])

# print(episode["external_urls"]["spotify"])

# # spotify_client = spotipy.Spotify(
# #     auth_manager=spotipy.oauth2.SpotifyClientCredentials(
# #         client_id="b9f9f83dc5cf4444abb02bd3198a5f14",
# #         client_secret="ee4071c6d0fc4fc19b3d3753ab85f8f3",
# #     ))

# # jre_show_id = "spotify:show:4rOoJ6Egrf8K2IrywzwOMk"
# # jre_show_id = "http://open.spotify.com/show/4rOoJ6Egrf8K2IrywzwOMk"

# # jre_episodes = spotify_client.show_episodes(jre_show_id)

# # search_results = spotify_client.search("Joe Rogan Experience")

# # for episode in search_results["tracks"]["items"]:
# #     # print(type(episode))
# #     # print(episode.keys())
# #     # print(type(episode["album"]))
# #     # break

# # uri = "https://open.spotify.com/episode/1v884aTc6iNDpUmtfUCuHd"
# # features = spotify_client.audio_features(uri)
