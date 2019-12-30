# %%
import sys
import os
import numpy
import spotipy
import spotipy.util as util
import pandas as pd
import pickle
scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-private'
client_id = '1c4e52b850ef400c985c051b42af8e94'
client_secret = '7094d54d0a434c57a0402741ffa1e03b'
redirect_uri = 'http://localhost:8888/callback/'
# check arguments

username = 'swamsaur'


if not os.path.exists('.cache-' + username):
    print('A webpage will be launched, it will probably say not found, just copy and paste the link into the terminal')
token = util.prompt_for_user_token(
    username, scope, client_id, client_secret, redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
else:
    sys.exit('Bad token')
#%%

pls = sp.user_playlists(username, limit=50, offset=0)
cvc_uri = [pl['uri'] for pl in pls['items'] if pl['name'] == 'CVC_TOP'][0]
#%%

def get_data(os, lim=100):
    res=[]
    results = sp.user_playlist_tracks(
        username, cvc_uri, limit=lim, offset=os)
    for item in results['items']:
        track = item['track']['name']
        track_uri = item['track']['uri']
        album = item['track']['album']['name']
        album_uri = item['track']['album']['uri']
        audio_features = sp.audio_features(track_uri)[0]
        out_dict = {'track': track, 'track_uri': track_uri,
                    'album': album, 'album_uri': album_uri}
        out_dict = {**out_dict, **audio_features}
        for art in item['track']['artists']:
            out_dict['artist'] = art['name']
            out_dict['artist_uri'] = art['uri']
            gen = sp.artist(art['uri'])['genres']
            out_dict['genre'] = gen[0] if len(gen) > 0 else '.'
            res.append(out_dict)
    return(res, os+lim)


data=[]
os=0
maxrun=0

while os > 204:
    chunk, os = get_data(os)
    data+=chunk
    print(f'completed {str(os)} tracks')

# %%
 
 
#%%
df=pd.DataFrame.from_dict(data)
df.to_csv('data/CVC_metadata.csv.gz', index=False)

# %%

