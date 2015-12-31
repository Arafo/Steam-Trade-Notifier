CREAR
SCHTASKS /Create /ST 08:00 /ET 23:59 /RU "SYSTEM" /TN SteamTradeNotifier /SC minute /MO 3 /TR "E:\Archivos de programa\Python34\python C:\Users\Rafa\Desktop\SteamTradeNotifier\steam-trade-notifier.py"
VER
SCHTASKS /query /TN "SteamTradeNotifier"
BORRAR
SCHTASKS /delete /TN "SteamTradeNotifier"

Ejecutar CMD como administrador para hacer cambios