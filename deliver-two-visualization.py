import json

likes = json.load(open('./playlists/likes.json'))

likes_df = extract_df(todict(likes), ['title','publishedAt','videoPublishedAt'])



