#!/bin/sh
# Follow the system service journal

journalctl -f -u bluos-scrobbler.service
