# Obfuscation Techniques on Python-based Malware, DD2525 Project
USE AT YOUR OWN RISK, THIS WILL DOWNLOAD THE FILES SPECIFIED IN ```malware.json``` TO YOUR COMPUTER.

A WINDOWS VM IS RECOMMENDED. 
## How to use

Run ```uv sync```

Add your free Virustotal API key to the .env file like this: ```API_KEY=a4b3...``` (sign up here https://www.virustotal.com/gui/sign-in)

Add desired malware to be tested in ```malware.json```

Run ```uv run clone_malware.py```

Run ```uv run run_test.py```

See the results in the generated ```data.json``` file

(in case that virustotal is slow and hasnt completed analysis)

Run ```uv run .\Virustotal\virustotal_scripts.py``` to fetch updated results

## Requirements
* Windows (only tested platform)
* Python 3.11
* UV installed
* Git
