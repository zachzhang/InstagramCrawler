from instagram.client import InstagramAPI

access_token = "4368742458.1677ed0.6937b64a153742858a273c3377acba92"
client_secret = "0a6bac6acd6b482bbff3c1cfc80528e0"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)
recent_media, next_ = api.user_recent_media(user_id="userid", count=10)
for media in recent_media:
   print media.caption.text