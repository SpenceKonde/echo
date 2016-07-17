""" fauxmo_minimal.py - Fabricate.IO

    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".

    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.

    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""

import fauxmo
import logging
import time
import urllib2

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)


#urllib2.urlopen()

fargourl="http://192.168.2.14/api/relay/"

triggers=[
            {"colored lights": 52000},
            {"white lights": 52010},
            {"wizard light": 52020}
]

def setFargoRelay(relay, state):
    if (state):
        urllib2.urlopen(fargourl+str(relay+1)+"/on").read()
    else:
        urllib2.urlopen(fargourl+str(relay+1)+"/off").read()


class fargo_handler(debounce_handler):   
    def initialize(triggers,relaynumber,responder,poller):
        self.relaynumber=relaynumber
        for trig, port in triggers.items():
            fauxmo.fauxmo(trig, responder, poller, None, port, self)

    def act(self,client_address,state):
        print "Fargo Handler "+str(self.relaynumber),state,"from client@", client_address
        if (state):
            urllib2.urlopen(fargourl+str(self.relaynumber+1)+"/on").read()
        else:
            urllib2.urlopen(fargourl+str(self.relaynumber+1)+"/off").read()

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    fargo_handler().initialize(triggers[0],0,u,p)
    fargo_handler().initialize(triggers[1],1,u,p)
    fargo_handler().initialize(triggers[2],2,u,p)
    

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
