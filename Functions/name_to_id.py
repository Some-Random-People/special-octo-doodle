import requests


# Converts a username to a user id
def name_to_id(name: str):
    request = requests.get(f"https://osu.ppy.sh/users/{name}")
    return request.url.replace("https://osu.ppy.sh/users/", "")
