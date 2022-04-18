#!/bin/sh
# Set up as a system service

PWD=`pwd`
ME=`whoami`

cat > bluos-scrobbler.service << EOF
FILE="[Unit]
Description=BluOS Scrobbler
After=multi-user.target

[Service]
Type=simple
Restart=always
Environment=PYTHONUNBUFFERED=1
User=$ME
ExecStart=/usr/bin/python3 $PWD/bluos-scrobbler.py
StandardOutput=journal+console
StandardError=journal+console

[Install]
WantedBy=multi-user.target
EOF

sudo cp bluos-scrobbler.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bluos-scrobbler.service
sudo systemctl restart bluos-scrobbler.service

rm bluos-scrobbler.service

# To follow the output:
# journalctl -f -u bluos-scrobbler.service
