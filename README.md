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

1. Pull the image:

   ```bash
   docker pull ghcr.io/prince25/plex-cleaner:main
   ```

2. Run the container (mount a folder to edit the config file):

   ```bash
   docker run -v ./plex-cleaner:/plex-cleaner/config ghcr.io/prince25/plex-cleaner:main
   ```

#### Option 2: Docker Compose (recommended)

1. Create a `docker-compose.yml` file:

   ```yaml
   version: "3"
   services:
     plex-cleaner:
       image: ghcr.io/prince25/plex-cleaner:main
       container_name: plex-cleaner
       restart: unless-stopped
       depends_on:
         - plex
       volumes:
         - ./plex-cleaner:/plex-cleaner/config
   ```

2. Run with Docker Compose:

   ```bash
   docker-compose up -d
   ```

## Configuration

You need to create a `config.yaml` file in the `/config` directory with your Plex server details and preferences. For convenience, you can edit the example `config.yaml` in the project root and place it in the `/config` directory.

Use this template:

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

The application will wait until this file is created and properly configured before proceeding.

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

1. The container starts and creates the `config` directory if it doesn't exist
2. You need to create and place the `config.yaml` file in the mounted config directory (you can copy and edit the example file from the project root)
3. If you use the default Plex token, the script will pause and wait for your edit
4. The script checks every 30 seconds for the config file or for changes when a default token is found
5. Changes to interval hours or other settings are picked up automatically between runs

The container will automatically clean up empty collections and playlists based on your configuration.

## Technologies Used

- [Python](https://www.python.org/)
- [PlexAPI](https://github.com/pushingkarmaorg/python-plexapi)
- [PyYAML](https://pyyaml.org/)
- [Docker](https://www.docker.com/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
