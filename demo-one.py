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
#import urllib2

from debounce_handler import debounce_handler

logging.basicConfig(level=logging.DEBUG)

#def 


class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"white lights": 52000,
                "colored lights":52001,
                "wizard light":52002,
                "desk lamp":52003,
                "tentacle light":52004,
                "air filter":52005,
                "pong one":52010}

    def act(self, client_address, state):
        print "State", state, "from client @", client_address
        return True

class fargo_relay_0(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"white lights": 52000}

    def act(self, client_address, state):
        print "White Lights", state, "from client @", client_address
        return True


class fargo_relay_1(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"colored lights": 52010}

    def act(self, client_address, state):
        print "Colored Lights", state, "from client @", client_address
        return True

class fargo_relay_2(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    TRIGGERS = {"wizard light": 52020}

    def act(self, client_address, state):
        print "Wizard Light", state, "from client @", client_address
        return True

def initializeHandler(handler):
    for trig, port in handler.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, handler)

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    initializeHandler(fargo_relay_0)
    initializeHandler(fargo_relay_1)
    initializeHandler(fargo_relay_2)
    

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
