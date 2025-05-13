import time
import argparse
import yaml
import sys
import os
from plexapi.server import PlexServer


# Load configuration from YAML file
def load_config(path="config/config.yaml"):
    """Load configuration from YAML file and check for default values."""

    # Make sure config directory exists
    config_dir = os.path.dirname(path)
    if not os.path.exists(config_dir):
        try:
            print(f"Creating config directory at: {config_dir}")
            os.makedirs(config_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating config directory: {e}")

    # Keep checking for config file existence and proper configuration
    while True:
        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)

            # If we got here, the file exists, but check if token has been updated
            if config.get("PLEX_TOKEN") == "your-plex-token":
                print(f"Warning: Default Plex token detected in config file.")
                print(f"Please edit {path} with your actual Plex server details")
                print(
                    "Waiting for config to be updated... (checking every 30 seconds)\n"
                )
                time.sleep(30)
                continue  # Try again after waiting

            # If we got here, file exists and token is not default
            break

        except FileNotFoundError:
            print(f"Error: Config file not found at '{path}'")
            print(f"Please create {path} with your Plex server details")
            print(
                "Waiting for config file to be created... (checking every 30 seconds)\n"
            )
            time.sleep(30)
            continue  # Try again after waiting

        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML in config file: {e}")
            print("Please fix the YAML syntax in your config file")
            print("Waiting for config to be fixed... (checking every 30 seconds)\n")
            time.sleep(30)
            continue  # Try again after waiting

        except Exception as e:
            # Just try again if there's any error (e.g. file is being edited)
            print(f"Error reading config: {e}")
            print("Waiting for config to be available... (checking every 30 seconds)\n")
            time.sleep(30)
            continue  # Try again after waiting

    print("Valid config found! Continuing with script...")

    # Validate required keys
    required_keys = ["PLEX_BASEURL", "PLEX_TOKEN", "LIBRARIES"]
    for key in required_keys:
        if key not in config:
            print(f"Error: '{key}' is missing from config file.")
            sys.exit(1)

    # Validate LIBRARIES is a dict of lists
    if not isinstance(config["LIBRARIES"], dict) or not all(
        isinstance(v, list) for v in config["LIBRARIES"].values()
    ):
        print("Error: 'LIBRARIES' must be a dictionary of lists in config file.")
        sys.exit(1)

    # Validate DELETE_COLLECTIONS and DELETE_PLAYLISTS are bool if present
    for key in ["DELETE_COLLECTIONS", "DELETE_PLAYLISTS"]:
        if key in config and not isinstance(config[key], bool):
            print(f"Error: '{key}' must be a boolean (true/false) in config file.")
            sys.exit(1)

    # Validate INTERVAL_HOURS is a positive number if present
    if "INTERVAL_HOURS" in config:
        try:
            if float(config["INTERVAL_HOURS"]) <= 0:
                raise ValueError()
        except Exception:
            print("Error: 'INTERVAL_HOURS' must be a positive number in config file.")
            sys.exit(1)

    return config


# Connect to Plex server using baseurl and token
def connect_plex(baseurl, token):
    return PlexServer(baseurl, token)


# Delete empty collections in specified libraries
def delete_empty_collections(plex, libraries):
    for lib_name in libraries:
        try:
            section = plex.library.section(lib_name)
        except Exception as e:
            print(f"Warning: Could not access library '{lib_name}': {e}")
            continue
        for collection in section.collections():
            try:
                if not collection.items():
                    print(f"Deleting empty collection: {collection.title}")
                    collection.delete()
            except Exception as e:
                print(
                    f"Warning: Could not process collection '{getattr(collection, 'title', 'Unknown')}': {e}"
                )


# Delete empty playlists from Plex server
def delete_empty_playlists(plex):
    try:
        playlists = plex.playlists()
    except Exception as e:
        print(f"Warning: Could not retrieve playlists: {e}")
        return
    for playlist in playlists:
        try:
            if not playlist.items():
                print(f"Deleting empty playlist: {playlist.title}")
                playlist.delete()
        except Exception as e:
            print(
                f"Warning: Could not process playlist '{getattr(playlist, 'title', 'Unknown')}': {e}"
            )


# Top-level cleanup function now handles reloading config and deleting items
def run_cleanup():
    config = load_config()
    try:
        plex = connect_plex(config["PLEX_BASEURL"], config["PLEX_TOKEN"])
    except Exception as e:
        print(f"Error: Could not connect to Plex server: {e}")
        return
    try:
        if config.get("DELETE_COLLECTIONS", True):
            for lib_type in ["movies", "shows"]:
                libs = config.get("LIBRARIES", {}).get(lib_type, [])
                delete_empty_collections(plex, libs)
        if config.get("DELETE_PLAYLISTS", True):
            delete_empty_playlists(plex)
    except Exception as e:
        print(f"Unexpected error during cleanup: {e}")


# Main entry point for the script
def main(args=None):
    parser = argparse.ArgumentParser(
        description="Delete empty Plex collections and playlists."
    )
    parser.add_argument(
        "--once", action="store_true", help="Run cleanup once and exit."
    )
    opts = parser.parse_args(args)

    # Run once or interval mode
    if opts.once:
        run_cleanup()
        print("Cleanup complete. Exiting.")
    else:
        # Initial read to get starting interval
        config = load_config()
        interval_hours = float(config.get("INTERVAL_HOURS", 24))
        print(
            f"Interval mode enabled. Will run cleanup every {interval_hours} hour(s)..."
        )

        try:
            # Main loop - run first, then wait each time
            while True:
                run_cleanup()
                print(
                    f"Cleanup complete. Waiting {interval_hours} hour(s) for next run...\n"
                )
                time.sleep(interval_hours * 3600)
                # Reload config to get the latest interval
                config = load_config()
                interval_hours = float(config.get("INTERVAL_HOURS", 24))
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting.")


if __name__ == "__main__":
    main()
