# Controller for room based of fauxmo/fauxhue
My room control script is in EchoRoomControl.py - it is specific to my setup, as should be apparent, and not intended for public consumption - but the code can be readily repurposed for other setups without really knowing python, so I suppose it might be useful to others. Whole thing will run on a raspberry pi after just syncing this repo (and installing python if needed). 

I manually kick it off after a reboot and run it in a screen session so that interrupting the ssh session doesn't kill it. 

Based around a fork of the Todd Medema's echo repo, which makes use of the MakerMusings fauxmo library (https://github.com/makermusings/fauxmo ) and the fauxhue extension to said library ( https://github.com/mjg59/fauxmo ). The debounce_handler class has been extended to support Hue devices, and not debounce multiple requests in succession from the same echo (some hue commands result in two requests). Note that it has not been updated from upstream repos in years, nor do I have plans to do this unless something gets changed and fauxmo suddenly stops working. 

# Motivation
The amazon echo has excellent voice recognition (as opposed to the "voice recognition" boards for arduino et al, which seem to have miserable recognition rates). However, none of the devices I want to control are commercial smart home devices - they're all either niche items, or things I've built myself - thus the echo can't natively interact with them. This code runs on a linux system (like a Pi) and acts as a bridge, presenting itself to the Echo as pile of WeMo smart sockets or Phillips Hue bulbs, and then talks to the smart devices via their respective APIs. 
