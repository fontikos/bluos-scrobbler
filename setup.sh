#!/bin/sh
# Set up as a system service
sudo cp bluos-scrobbler.service /etc/systemd/system/
sudo systemctl daemon-reload
systemctl enable bluos-scrobbler.service
sudo systemctl restart bluos-scrobbler.service
