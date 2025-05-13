#!/usr/bin/env bash

set -e

CONFIG_PATH="/plex-cleaner/config/config.yaml"

# Only seed if config.yaml does not exist OR is empty (0 bytes)
if [ ! -s "$CONFIG_PATH" ]; then
  mkdir -p /plex-cleaner/config
  cp /plex-cleaner/config.yaml.default "$CONFIG_PATH"
  echo "Seeded default config.yaml into /plex-cleaner/config/"
fi

exec "$@"
