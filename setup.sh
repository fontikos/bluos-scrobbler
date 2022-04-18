#!/bin/sh
# Set up as a system service
sudo cp bluos-scrobbler.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bluos-scrobbler.service
sudo systemctl restart bluos-scrobbler.service

# To follow the output:
# journalctl -f -u bluos-scrobbler.service
