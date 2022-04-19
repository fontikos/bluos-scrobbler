# BluOS Scrobbler

A simple Python-based Last.fm scrobbler for BluOS.

## Configuration

Fill in `myconfig-example.py` and rename it to `myconfig.py`.

### Last.fm Variables

For the `LASTFM_*` variables, detailed istructions are available in the [Last.fm API documentation](https://www.last.fm/api).

In summary, you first need to apply for an API key [here](https://www.last.fm/api/account/create). Providing only an application name in the form is sufficient. You will then receive an API key and secret that you need to copy in `LASTFM_API` and `LASTFM_SECRET` respectively.

The next step is to obtain a session key. For that you will first need to obtain an authorization token. You can follow the instructions [here](https://github.com/huberf/lastfm-scrobbler). In short, go to http://www.last.fm/api/auth?api_key={YOUR_API_KEY}&cb=http://localhost:5555 after you make sure nothing is running at port 5555. Click "Allow Access" and copy the token from the resulting URL (e.g. http://localhost:5555/?token={TOKEN_YOU_WANT}). Copy the token in `LASTFM_TOKEN`.

Finally, run:

`$ python3 ./lastfm-session-key.py`

This will print an XML response which will contain the session key within the `<key>` tags. Copy the session key in `LASTFM_SESSION_KEY`. Note that the session key never expires, so you only need to do this once.

### BluOS Variables

Update the `BLUOS_IP` with the IP address of your BluOS device. `BLUOS_PORT` is the port number of the service.

You can read more at the [BluOS API](https://bluos.net/wp-content/uploads/2020/06/Custom-Integration-API-v1.0.pdf).

### Other Configuration Variables

The variable `SCROBBLE_AFTER` defines the seconds of playtime after which a new song will be scrobbled. 

The variable `SCROBBLE_SERVICES` defines the services that will be scrobbled. Only Tidal and the local library (LocalMusic) have been tested, but it should be extendable to others.


## Execution

The script can be executed as follows:

`python3 ./bluos-scrobbler.py`

Note that in case of songs with multiple artists that have an artist tag of the form `artist1, artist2, artist3`, the script will scrobble it with only the first artist. Similarly the script will remove any "(Remastered)" information from the track and album title.


## Installation as a Service

In a Linux environment, such as a Raspberry Pi, you can install it to run as a service by executing:

`./install-as-service.sh`

## Acknowledgements

The Last.fm library, `lastfm.py` is based on the [lastfm-scrobbler](https://github.com/huberf/lastfm-scrobbler).
