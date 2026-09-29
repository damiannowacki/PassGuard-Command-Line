> **Note:** the password-cracker estimator currently only runs off of pure math, so it is not entirely accurate because it doesn't account for other reasons a password could be quickly cracked, such as common patterns- which will be added in a future update. 

## A command-line Python security tool that takes in a password and securely:
* **-Checks its strength using the length and pool size**
* **-Checks the haveibeenpwned API to see if there have been any breaches with the password**
* **-Estimates the time it would take the password to be cracked**
* **-More will be added soon**

##Security
The full password never gets sent to the haveibeenpwned API. Instead, it is first hashed and then the first 5 characters are sent, and then when a list is returned, the program goes through the list locally and checks if any match the full password (the hash suffix).

#Instillation
The "requests" library needs to be downloaded before using the program: "pip install requests" in the command line
