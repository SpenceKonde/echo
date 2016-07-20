# Fauxmo library and code to use it for controlling smart appliances

This is a fork of the Todd Medema's echo repo, which makes use of the MakerMusings fauxmo library (https://github.com/makermusings/fauxmo ) and the fauxhue extension to said library ( https://github.com/mjg59/fauxmo ). The debounce_handler class has been extended to support Hue devices, and not debounce multiple requests in succession from the same echo (some hue commands result in two requests)



# Motivation
The amazon echo has excellent voice recognition (as opposed to the "voice recognition" boards for arduino et al, which seem to have miserable recognition rates). However, none of the devices I want to control are commercial smart home devices - they're all either niche items, or things I've built myself - thus the echo can't natively interact with them. This code runs on a linux system (like a Pi) and acts as a bridge, presenting itself to the Echo as pile of WeMo smart sockets or Phillips Hue bulbs, and then talks to the smart devices via their respective APIs. 

I hope that the code here will be useful as inspiration/guidance to someone working on a similar project. 
