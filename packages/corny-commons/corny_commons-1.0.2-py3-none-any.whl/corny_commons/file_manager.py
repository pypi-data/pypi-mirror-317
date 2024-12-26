"""Functionality for creating, reading, updating and deleting cache files."""

# Standard library imports
import json
import os
import shutil
from datetime import datetime


CACHE_DIRECTORY = "cache"


def clear_log_file(filename: str) -> None:
    """Truncates the log file and writes to it a log header to identify when it was started."""
    formatted_time = f"{datetime.now():%Y-%m-%d__%H.%M.%S}"
    log_template = f"START TIMESTAMP {formatted_time} END TIMESTAMP Started log.\n"
    with open(filename + ".log", "w", encoding="UTF-8") as file:
        file.write(log_template)


def log(*raw_message: str, filename="", force: bool = True) -> str:
    """Writes the message to the current log file, and returns the message formatted with the
    current time and proper indentation.
    """
    timestamp = f"{datetime.now():%Y-%m-%d @ %H:%M:%S}: "

    # Adds spaces after each newline so that the actual message is in line with the timestamp.
    message = timestamp + " ".join(map(str, raw_message)).replace(
        "\n", "\n" + " " * len(timestamp)
    )
    with open(filename + ".log", "a", encoding="UTF-8") as file:
        file.write(message + "\n")
    if force:
        print(message)
    return message


def save_active_log_file(filename: str, logs_dir: str = "logs") -> None:
    """Copies the active log file to a new file in the logs directory and clears it."""
    filename += ".log"
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            contents = file.read()
    except FileNotFoundError:
        return
    else:
        if not contents.startswith("START TIMESTAMP "):
            return
    # Extract log creation date from active log
    contents = contents.split(" END TIMESTAMP ", maxsplit=1)
    if isinstance(contents, str):
        return
    log_start_time = contents[0].lstrip("START TIMESTAMP ").rstrip("\n")

    # Copy active log contents to new file
    new_log_filename = os.path.join(logs_dir, log_start_time + ".log")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    with open(new_log_filename, "w", encoding="UTF-8") as file:
        file.write(contents[1])


def read_cache(cache_name: str) -> dict:
    """Returns the cached data if it exists, otherwise an empty dictionary."""
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    filepath = os.path.join(CACHE_DIRECTORY, f"{cache_name}.json")
    if not os.path.isfile(filepath):
        return {}
    with open(filepath, "r", encoding="UTF-8") as file:
        return json.load(file)


def get_cache(
    cache_name: str, force_update: bool, callback_function
) -> tuple[dict, dict]:
    """Attempts to get the cache if it exists and the 'force_update' argument is set to False.

    If the above criteria are not met, the callback function is called and its return value
    is saved as the new cache.

    Arguments:
        cache_name -- the filename of the cache without the .json extension.
        force_update -- a boolean indicating if any existing caches should be updated forcefully.
        callback_function -- a lambda function that generates the new cache.

    Returns a tuple consisting of the cached data and the old cache (defaults to an empty dict).
    """
    cache = read_cache(cache_name)
    log(f"Cache for {cache_name} was {'*not* ' * (not cache)}found.", force=False)
    if not force_update and cache:
        # The cache has no need to be updated.
        return cache, cache
    old_cache = dict(cache)
    cache = callback_function()
    write_cache(cache_name, cache)
    write_cache(cache_name + "_old", old_cache)
    return cache, old_cache


def write_cache(cache_name: str, data: dict) -> None:
    """Serialises the given data and writes it in json format to the cache directory."""
    json_string = json.dumps(data, indent=2, ensure_ascii=False)
    filename = os.path.join(CACHE_DIRECTORY, f"{cache_name}.json")
    with open(filename, "w", encoding="UTF-8") as file:
        file.write(json_string)
    log(f"Wrote cache to '{filename}'.", force=False)


def clear_cache(cache_name: str = None, cache_path: str = None) -> int:
    """Removes all files in the given directory, as well as the directory itself.

    Returns the number of removed files if the directory previously existed, otherwise False.
    """
    files_removed = 0
    cache_path = cache_path or CACHE_DIRECTORY
    if os.path.exists(cache_path):
        if cache_name:
            for is_old in range(2):
                try:
                    filename = cache_name + "_old" * is_old + ".json"
                    os.remove(os.path.join(cache_path, filename))
                    files_removed += 1
                except FileNotFoundError:
                    if not is_old:
                        log(
                            f"Error: The file './{cache_path}/{filename}' does not exist."
                        )
                        return False
            log(f"Successfully removed cache for '{cache_name}'.")
        else:
            files_removed = len(os.listdir(cache_path))
            shutil.rmtree(cache_path)
            log("Successfully cleared cache at directory: ./" + cache_path)
        return files_removed
    log(f"Error: The path './{cache_path}' does not exist.")
    return False


def read_env() -> bool:
    """Reads the .env file in the current directory and sets its contents in the program's memory.

    Returns a boolean indicating if any system environment variables were set as a result of this.
    """
    if not os.path.isfile(".env"):
        log("    --- '.env' file not found in program root directory. ---")
        return False
    return_value = False
    log()
    log("    --- Processing environment variable (.env) file... ---")
    with open(".env", "r", encoding="UTF-8") as file:
        # Loop through each line in file
        for line in file.readlines():
            # Line does not contain a variable assignment
            if "=" not in line:
                continue
            # Extracts environment variable name and value from each line, stripping whitespaces.
            env_name, env_value = [
                s.strip() for s in line.rstrip("\n").split("=", maxsplit=1)
            ]
            # Don't reassign value if already set in memory
            if env_name in os.environ:
                log(
                    f"Environment variable '{env_name}' is already set, ignoring .env assignment."
                )
                continue
            # Actually assign the environment variable value in memory
            os.environ[env_name] = env_value
            log(f"Set environment variable value '{env_name}' to '{env_value}'.")
            # Make the function return True since there was an env set
            return_value = True
    log("    --- Finished processing environment variable files. ---")
    log()
    return return_value
