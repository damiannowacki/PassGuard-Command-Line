A command-line Python security tool that takes in a password and securely:
-Checks its strength using the length and pool size
-Checks the haveibeenpwned API to see if there have been any breaches with the password
-More will be added soon

The full password never gets sent to the haveibeenpwned API. Instead, it is first hashed and then the first 5 characters are sent, and then when a list is returned, the program goes through the list locally and checks if any match the full password (the hash suffix).

The "requests" library needs to be downloaded before using the program (pip install requests in the command line)
