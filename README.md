# Steam Trade Notifier
![](https://img.shields.io/twitter/url/https/github.com/Arafo/Steam-Trade-Notifier.svg?style=social)

Send an e-mail notification when a Steam trade offer is accepted or received.

Documentation URL:
https://developer.valvesoftware.com/wiki/Steam_Web_API/IEconService

## Usage

### Python (Windows)
- Start a command prompt as an administrator and paste this:<br/><pre>SCHTASKS /Create /ST 08:00 /ET 23:59 /RU "SYSTEM" /TN SteamTradeNotifier /SC minute /MO 3 /TR "PYTHON_PATH SCRIPT_PATH"</pre>

##### Other commands
- Show task:<br/><pre>SCHTASKS /query /TN "SteamTradeNotifier"</pre>
- Delete task:<br/><pre>SCHTASKS /delete /TN "SteamTradeNotifier"</pre>

### Google Apps Script
