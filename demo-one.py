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

def setFargoRelay(relay, state):
    if (state):
        urllib2.urlopen(fargourl+str(relay+1)+"/on").read()
    else:
        urllib2.urlopen(fargourl+str(relay+1)+"/off").read()


class fargo_relay_0(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"white lights": 52000}
    
    

    def act(self, client_address, state):
        print "White Lights", state, "from client @", client_address
        setFargoRelay(0,state)
        return True



class fargo_relay_1(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"colored lights": 52010}

    def act(self, client_address, state):
        print "Colored Lights", state, "from client @", client_address
        setFargoRelay(1,state)
        return True

class fargo_relay_2(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"wizard light": 52020}

    def act(self, client_address, state):
        print "Wizard Light", state, "from client @", client_address
        setFargoRelay(2,state)
        return True

def initializeHandler(responder,poller,handler):
    for trig, port in handler.TRIGGERS.items():
        fauxmo.fauxmo(trig, responder, poller, None, port, handler)

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    initializeHandler(u,p,fargo_relay_0())
    initializeHandler(u,p,fargo_relay_1())
    initializeHandler(u,p,fargo_relay_2())
    

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
