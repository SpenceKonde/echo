### NOTES FOR ECHO ROOM CONTROL CONFIGURATION

Root is in /home/pi/echo, files copied to Z:/echo_to_pi, cp /mnt/scratch/echo_to_pi/* /home/pi/echo - first attempt may fail if scratch isn't already automounted, but trying again will work. 

Always check existing screen session before restarting

Restart with

screen python EchoRoomControl.py