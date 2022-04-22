
import lastfm
import myconfig

auth = {}
auth['api'] = myconfig.LASTFM_API
auth['secret']= myconfig.LASTFM_SECRET
auth['user_token'] = myconfig.LASTFM_TOKEN

print(lastfm.authorize(auth))
