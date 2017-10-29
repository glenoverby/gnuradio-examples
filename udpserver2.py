#!/usr/bin/env python2
#
# This combines a GNU Radio graph for receiving from OsmoSDR (tested with
# a LimeSDR) and sending the data to JACK for eventual use by dttsp.
# It provides a simple usbsoftrock-compatible server for controling gr-osmosdr
#
# usbsoftrock commands:
#	get ptt
#	get key
#	get freq
#	get tone
#	get si570_multiplier
#	get local_multiplier
#	set ptt on | off
#	set bpf on | off
#	set freq value
#	set tone value
#	set local_multiplier value
#
# Add:
#	[sg]et rfgain
#	[sg]et ifgain
#	[sg]et bbgain
#	[sg]et antenna
#
# By declaring variables in gnuradio-companion, it will create functions for
# setting and getting those values.
#

import socketserver
import dttsprx3

class srUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def command(self, txt):
        global tb
        words = txt.split()
        print "command", words

        if words[0] == "get":
            if words[1] == "ptt":
                return "0"
            elif words[1] == "freq":
                f = tb.get_frequency()
                return "{0}".format(f)
            elif words[1] == "rfgain":
                g = tb.get_rfgain()
                print "get rfgain", g
                return "{0}".format(g)
            elif words[1] == "tone":
                return "0"
            else:
                return "unknown subcommand {0}".format(words[1])
        elif words[0] == "set":
            if words[1] == "ptt":
                return "0"
            elif words[1] == "freq":
                f = float(words[2])
                f *= 1000000
                print "set freq", f
                #r = tb.get_frequency()
                r = tb.set_frequency(f)
                return "{0}".format(r)
            elif words[1] == "rfgain":
                g = float(words[2])
                print "set rfgain", g
                r = tb.set_rfgain(g)
                return "{0}".format(r)
            elif words[1] == "rfgain":
                g = float(words[2])
                print "set rfgain", g
                r = tb.set_rfgain(g)
                return "{0}".format(r)
            elif words[1] == "tone":
                return "0"
            else:
                return "unknown subcommand {0}".format(words[1])
        else:
            return "unknown command {0}".format(words[0])

    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        #print "{} wrote ".format(self.client_address[0]), 
        # "{} bytes command".format(len(self.request[0]))
        #print(data)
        reply = self.command(str(data))
        socket.sendto(bytes(reply), self.client_address)

if __name__ == "__main__":
    #HOST, PORT = "localhost", 9999
    HOST, PORT = "localhost", 19004
    srserver = socketserver.UDPServer((HOST, PORT), srUDPHandler)

    global tb
    #tb = dttsprx3.top_block_cls()
    tb = dttsprx3.dttsprx3()
    tb.start()
    print "freq", tb.get_frequency()
    #tb.set_frequency(144038000)
    print "topblock started, now srserver"
    srserver.serve_forever()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

