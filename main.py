import time
import argparse
import yaml
from plexapi.server import PlexServer


# Load configuration from YAML file
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


# Connect to Plex server using baseurl and token
def connect_plex(baseurl, token):
    return PlexServer(baseurl, token)


# Delete empty collections in specified libraries
def delete_empty_collections(plex, libraries):
    for lib_name in libraries:
        section = plex.library.section(lib_name)
        for collection in section.collections():
            if not collection.items():
                print(f"Deleting empty collection: {collection.title}")
                collection.delete()


# Delete empty playlists from Plex server
def delete_empty_playlists(plex):
    for playlist in plex.playlists():
        if not playlist.items():
            print(f"Deleting empty playlist: {playlist.title}")
            playlist.delete()


# Main entry point for the script
def main(args=None):
    parser = argparse.ArgumentParser(
        description="Delete empty Plex collections and playlists."
    )
    parser.add_argument(
        "--once", action="store_true", help="Run cleanup once and exit."
    )
    opts = parser.parse_args(args)

    # Load config and connect to Plex
    config = load_config()
    plex = connect_plex(config["PLEX_BASEURL"], config["PLEX_TOKEN"])

    # Cleanup logic for collections and playlists
    def run_cleanup():
        if config.get("DELETE_COLLECTIONS", True):
            for lib_type in ["movies", "shows"]:
                libs = config.get("LIBRARIES", {}).get(lib_type, [])
                delete_empty_collections(plex, libs)
        if config.get("DELETE_PLAYLISTS", True):
            delete_empty_playlists(plex)

    # Run once or interval mode
    if opts.once:
        run_cleanup()
        print("Cleanup complete. Exiting.")
    else:
        interval_hours = float(config.get("INTERVAL_HOURS", 1))
        print(
            f"Interval mode enabled. Will run cleanup every {interval_hours} hour(s). Waiting for the first interval..."
        )
        while True:
            time.sleep(interval_hours * 3600)
            run_cleanup()
            print(f"Cleanup complete. Waiting {interval_hours} hour(s) for next run...")


if __name__ == "__main__":
    main()
