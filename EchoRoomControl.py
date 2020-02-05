""" EchoRoomControl.py 
    This is the room control script used to controll the lighting and other systems 
    at my appartment. The devices controlled are a Fargo R8 relay unit and192.1 several 
    pingpong light systems ( https://github.com/SpenceKonde/AzzyProjects/tree/master/Animate ) running on ESP8266's 

"""

import fauxmo
import logging
import time
import urllib2

from debounce_handler import debounce_handler
from debounce_handler import debounce_handler_hue

logging.basicConfig(level=logging.DEBUG)


#urllib2.urlopen()

fargourl="http://192.168.2.14/api/relay/"

triggers={"fargo":[
            {"trig":{"colored": 52000},"relay":0},
            {"trig":{"white light": 52010},"relay":1},
            {"trig":{"wizard": 52020},"relay":2},
            {"trig":{"tentacle": 52030},"relay":3},
            {"trig":{"desk": 52040},"relay":4},
            {"trig":{"air filter": 52050},"relay":5}
        ],"generic":[
            {"trig":{"pong":52100},"on":"http://192.168.2.21/load.php?index=1","off":"http://192.168.2.21/load.php?index=0"},
            #{"trig":{"pong":52200},"on":"http://192.168.2.17/send4.cmd?message=1E40FF00","off":"http://192.168.2.17/send4.cmd?message=1E400000"},
            {"trig":{"stairs":52201},"on":"http://192.168.2.17/send4.cmd?message=1E40FF01","off":"http://192.168.2.17/send4.cmd?message=1E400001"},
            {"trig":{"salt":52202},"on":"http://192.168.2.17/send4.cmd?message=1E40FF00","off":"http://192.168.2.17/send4.cmd?message=1E400000"},
            {"trig":{"exit":52203},"on":"http://192.168.2.17/send4.cmd?message=1E41FF01","off":"http://192.168.2.17/send4.cmd?message=1E410001"},
            {"trig":{"dab rig":52204},"on":"http://192.168.2.17/send4.cmd?message=1E40FF02","off":"http://192.168.2.17/send4.cmd?message=1E400002"},
            {"trig":{"cans":52204},"on":"http://192.168.2.17/send8.cmd?message=2858000000FFFF","off":"http://192.168.2.17/send8.cmd?message=28580000000000"},
            #{"trig":{"clock":52150},"on":"http://192.168.2.16/code.run?code=nixs=1;uplcd();","off":"http://192.168.2.16/code.run?code=nixs=0;uplcd();"}
        ],"pong":[
            #{"trig":{"corner lights":52110},"ip":"192.168.2.138"},
        ]
    }

values={0:"0",2:"1",5:"2",7:"3",10:"4",12:"5",15:"6",17:"7",20:"8",22:"9",25:"10",27:"11",30:"12",32:"13",35:"14",37:"15",40:"16",42:"17",45:"18",48:"19",51:"20",53:"21",56:"22",58:"23",61:"24",63:"25",66:"26",68:"27",71:"28",73:"29",76:"30",78:"31",81:"32",83:"33",86:"34",88:"35",91:"36",94:"37",97:"38",99:"39",102:"40",104:"41",107:"42",109:"43",112:"44",114:"45",117:"46",119:"47",122:"48",124:"49",127:"50",129:"51",132:"52",134:"53",137:"54",139:"55",142:"56",144:"57",147:"58",150:"59",153:"60",155:"61",158:"62",160:"63",163:"64",165:"65",168:"66",170:"67",173:"68",175:"69",178:"70",181:"71",183:"72",186:"73",188:"74",191:"75",193:"76",196:"77",198:"78",201:"79",204:"80",206:"81",209:"82",211:"83",214:"84",216:"85",219:"86",221:"87",224:"88",226:"89",229:"90",232:"91",234:"92",237:"93",239:"94",242:"95",244:"96",247:"97",249:"98",252:"99",255:"100"}

class hue_handler(debounce_handler_hue):
    def act(self,bulb,client_address,state):
        print "hue handler for bulb ",bulb," from client ",client_address," set to ",state
        return True
class pong_handler(debounce_handler_hue):
    def initialize(self,triggers,ip,responder,poller):
        self.destip=ip
        for trig, port in triggers.items():
            fauxmo.fauxhue(trig,u,p,None,port,self).add_bulb(trig)
    def act(self,bulb,client_address,state):
        print "hue handler for bulb ",bulb," from client ",client_address," set to ",state
        if (state is True):
            #print "true"
            #print "http://"+self.destip+"/on.cmd"
            resp=urllib2.urlopen("http://"+self.destip+"/on.cmd")
            code=resp.getcode()
            resp.read()
            if (code==200):
                return True
            else:
                return False
        elif (state is False):
            #print "false"
            #print "http://",self.destip,"/off.cmd"
            resp=urllib2.urlopen("http://"+self.destip+"/off.cmd")
            code=resp.getcode()
            resp.read()
            if (code==200):
                return True
            else:
                return False
        else:
            val=values[state]
            #print val
            #print "http://"+self.destip+"/setScene.cmd?scene="+val
            resp=urllib2.urlopen("http://"+self.destip+"/setScene.cmd?scene="+str(val))
            resp.read()
            if (code==200):
                return True
            else:
                return False
class generic_handler(debounce_handler):
    def initialize(self,triggers,on,off,responder,poller):
        self.onurl=on
        self.offurl=off
        for trig, port in triggers.items():
            fauxmo.fauxmo(trig, responder, poller, None, port, self)


    def act(self,client_address,state):
        print "Generic Handler ",state,"from client@", client_address
        if (state):
            resp=urllib2.urlopen(self.onurl)
            code=resp.getcode()
            resp.read()
        else:
            resp=urllib2.urlopen(self.offurl)
            code=resp.getcode() 
            resp.read()
        if (code==200):
            return True
        else:
            return False


class fargo_handler(debounce_handler):   
    def initialize(self,triggers,relaynumber,responder,poller):
        self.relaynumber=relaynumber
        for trig, port in triggers.items():
            fauxmo.fauxmo(trig, responder, poller, None, port, self)

    def act(self,client_address,state):
        print "Fargo Handler "+str(self.relaynumber),state,"from client@", client_address
        if (state):
            resp=urllib2.urlopen(fargourl+str(self.relaynumber+1)+"/on")
            code=resp.getcode()
            resp.read()
        else:
            resp=urllib2.urlopen(fargourl+str(self.relaynumber+1)+"/off")
            code=resp.getcode()
            resp.read()
        if (code==200):
            return True
        else:
            return False

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    for triglist in triggers["fargo"]:
        fargo_handler().initialize(triglist["trig"],triglist["relay"],u,p)
    for triglist in triggers["generic"]:
        generic_handler().initialize(triglist["trig"],triglist["on"],triglist["off"],u,p)
    for triglist in triggers["pong"]:
        pong_handler().initialize(triglist["trig"],triglist["ip"],u,p)
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
