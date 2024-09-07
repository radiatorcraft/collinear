# Collinear Scratch v1.1beta

This scripts automates following people using scratch.mit.edu API in Python.

## Features:

* Follows users from a text file containing usernames.
* Allows setting a delay between follow attempts.
* Logs progress and estimated remaining time.
* Provides optional user input for settings or loading from a JSON file.
* Includes a benchmark functionality to estimate processing time (this is mostly for developer debugging).

## Requirements:

* Python 3
* `scratchapi` library (install with `pip install scratchapi`)

## Instructions (v1.1beta and ahead):

1. **Install dependencies:** Run `pip install scratchapi` in your terminal.
2. **Download install.py from the releases tab.**
3. **Run the script!**


## Instructions (Legacy):

1. **Install dependencies:** Run `pip install scratchapi` in your terminal.
2. **Configure Paths:**
	* **log_path**: Should be linked to a text file called log.txt
	* **settings_path**: Should be linked to the settings.json that is provided.
	* **username**: Should include your scratch username that will be used.
	* **password**: Should include your scratch password to the username above.
	* **filename**: Should include the path to the usernames.txt file, a sample of 500 has been provided. However I do have one with over 140k usernames but to avoid malicious purposes I will not be providing it publically.
	* **error_path**: Should provide a path to a .log file called "error.log".
3. **Run the script!**

## Disclaimer
This script is for educational purposes and should not be used maliciously. @radiatorcraft assumes no blame for the malicious use of the script and is not responsible for any damage done by it.

## Support

Contact me on discord: radiatorsharp
    
