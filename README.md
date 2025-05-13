# Plex Cleaner

A simple Python utility to automatically delete empty collections and playlists from your Plex server. It can be run locally or inside a Docker container at user-defined intervals.

## Installation 

1. Clone the repository:

   ```bash
   git clone https://github.com/Prince25/plex-cleaner
   cd plex-cleaner
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit the `config.yaml` file with your Plex server details and preferences:

```yaml
PLEX_BASEURL: "http://your-plex-server:32400"
PLEX_TOKEN: "your-plex-token"
LIBRARIES:
  movies: ["Movies"]
  shows: ["TV Shows"]
DELETE_COLLECTIONS: true
DELETE_PLAYLISTS: true
INTERVAL_HOURS: 1
```

### Finding your Plex token

Follow the official guide to retrieve your X-Plex-Token:
https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

## Usage

### Local (one-time run)

```bash
python main.py --once
```

### Local (interval mode)

```bash
python main.py
```

### Docker

1. Build the image:

   ```bash
   docker build -t Plex Cleaner .
   ```

2. Run the container (mount your config file):

   ```bash
   docker run -v $(pwd)/config.yaml:/app/config.yaml Plex Cleaner
   ```

The container will sleep for the defined interval before each cleanup.

## Technologies Used

- [Python](https://www.python.org/)
- [PlexAPI](https://github.com/pushingkarmaorg/python-plexapi)
- [PyYAML](https://pyyaml.org/)
- [Docker](https://www.docker.com/)
