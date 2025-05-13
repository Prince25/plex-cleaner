# Plex Cleaner

A simple Python utility to automatically delete empty collections and playlists from your Plex server. It can be run locally or inside a Docker container at user-defined intervals.

## Installation & Setup

### Local Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Prince25/plex-cleaner
   cd plex-cleaner
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Docker Installation

#### Option 1: Basic Docker

1. Build the image:

   ```bash
   docker build -t plex-cleaner .
   ```

2. Run the container (mount your config file):

   ```bash
   docker run -v $(pwd)/config.yaml:/app/config.yaml plex-cleaner
   ```

#### Option 2: Docker Compose (recommended)

1. Create a `docker-compose.yml` file:

   ```yaml
   version: "3"
   services:
     plex-cleaner:
       image: plex-cleaner:latest
       container_name: plex-cleaner
       restart: unless-stopped
       volumes:
         - ./config.yaml:/app/config.yaml
   ```

2. Run with Docker Compose:

   ```bash
   docker-compose up -d
   ```

## Configuration

Edit the `config.yaml` file with your Plex server details and preferences:

```yaml
PLEX_BASEURL: "http://your-plex-server:32400"
PLEX_TOKEN: "your-plex-token"
LIBRARIES:
  movies: ["Movies", "4K Movies"]
  shows: ["TV Shows"]
DELETE_COLLECTIONS: true
DELETE_PLAYLISTS: true
INTERVAL_HOURS: 24
```

### Finding your Plex token

Follow the official guide to retrieve your X-Plex-Token:
https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

## Usage

### Local Usage

#### One-time run

```bash
python main.py --once
```

#### Interval mode (runs continuously)

```bash
python main.py
```

### How It Works in Docker

1. The container starts with a default `config.yaml` file
2. If the default Plex token is detected, the script will pause and wait
3. You can edit the mounted `config.yaml` file with your real settings
4. The script checks every 60 seconds for changes and continues when a valid token is found
5. Changes to interval hours or other settings are picked up automatically between runs

The container will automatically clean up empty collections and playlists based on your configuration.

## Technologies Used

- [Python](https://www.python.org/)
- [PlexAPI](https://github.com/pushingkarmaorg/python-plexapi)
- [PyYAML](https://pyyaml.org/)
- [Docker](https://www.docker.com/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
