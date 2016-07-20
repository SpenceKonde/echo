import time

class debounce_handler(object):
    """Use this handler to keep multiple Amazon Echo devices from reacting to
       the same voice command.
    """
    DEBOUNCE_SECONDS = 0.3

    def __init__(self):
        self.lastEcho = time.time()
        self.lastAddress="0.0.0.0" 
        
    def on(self, client_address):
        if self.debounce(client_address):
            return True
        return self.act(client_address, True)

    def off(self, client_address):
        if self.debounce(client_address):
            return True
        return self.act(client_address, False)

    def act(self, client_address, state):
        pass
    def debounce(self,client_address):
        """If multiple Echos are present, the one most likely to respond first
           is the one that can best hear the speaker... which is the closest one.
           Adding a refractory period to handlers keeps us from worrying about
           one Echo overhearing a command meant for another one.
           We also have to check the client address - if it's the same one that sent the last
           message, it's gotta be something different (ex, hue bulb is off, and you
           say "Alexa, set (hue bulb name) to 50 percent" - this will result in
           on() and dim() being called in rapid succession. 
        """
        if (((time.time() - self.lastEcho)  < self.DEBOUNCE_SECONDS) and (self.lastAddress != client_address)):
            return True

        self.lastEcho = time.time()
        self.lastAddress = client_address
        return False

class debounce_handler_hue(object):
    """Use this handler to keep multiple Amazon Echo devices from reacting to
       the same voice command.
    """
    DEBOUNCE_SECONDS = 0.3

    def __init__(self):
        self.lastEcho = time.time()
        self.lastAddress="0.0.0.0" 

    def on(self, bulb, client_address):
        if self.debounce(client_address):
            return True
        return self.act(bulb,client_address, True)

    def off(self, bulb, client_address):
        if self.debounce(client_address):
            return True
        return self.act(bulb,client_address, False)

    def act(self, bulb, client_address,state):
        pass
    def dim(self,bulb,client_address,value):
        if self.debounce(client_address):
            return True
        return self.act(bulb,client_address,value)
    def debounce(self,client_address):
        """If multiple Echos are present, the one most likely to respond first
           is the one that can best hear the speaker... which is the closest one.
           Adding a refractory period to handlers keeps us from worrying about
           one Echo overhearing a command meant for another one.
           We also have to check the client address - if it's the same one that sent the last
           message, it's gotta be something different (ex, hue bulb is off, and you
           say "Alexa, set (hue bulb name) to 50 percent" - this will result in
           on() and dim() being called in rapid succession. 
        """
        if (((time.time() - self.lastEcho)  < self.DEBOUNCE_SECONDS) and (self.lastAddress != client_address)):
            return True

        self.lastEcho = time.time()
        self.lastAddress = client_address
        return False

