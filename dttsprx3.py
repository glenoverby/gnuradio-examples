#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Dttsprx3
# Generated: Sun Oct 29 11:55:00 2017
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import time


class dttsprx3(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Dttsprx3")

        ##################################################
        # Variables
        ##################################################
        self.output_rate = output_rate = 48000
        self.samp_rate = samp_rate = output_rate*167
        self.rfgain = rfgain = 1
        self.ifgain = ifgain = 0
        self.frequency = frequency = 144380000
        self.bbgain = bbgain = 0
        self.antenna = antenna = "LNAL"

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'addr=driver=lime,soapy=0' )
        self.osmosdr_source_0_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0_0.set_center_freq(frequency, 0)
        self.osmosdr_source_0_0.set_freq_corr(0, 0)
        self.osmosdr_source_0_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0_0.set_gain_mode(False, 0)
        self.osmosdr_source_0_0.set_gain(rfgain, 0)
        self.osmosdr_source_0_0.set_if_gain(ifgain, 0)
        self.osmosdr_source_0_0.set_bb_gain(bbgain, 0)
        self.osmosdr_source_0_0.set_antenna(antenna, 0)
        self.osmosdr_source_0_0.set_bandwidth(0, 0)
          
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(int(samp_rate/output_rate), firdes.low_pass(
        	1, samp_rate, output_rate/2, 32768, firdes.WIN_BLACKMAN, 6.76))
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0 = audio.sink(48000, '', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.audio_sink_0, 1))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.osmosdr_source_0_0, 0), (self.low_pass_filter_0_0, 0))    

    def get_output_rate(self):
        return self.output_rate

    def set_output_rate(self, output_rate):
        self.output_rate = output_rate
        self.set_samp_rate(self.output_rate*167)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.output_rate/2, 32768, firdes.WIN_BLACKMAN, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.output_rate/2, 32768, firdes.WIN_BLACKMAN, 6.76))

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.osmosdr_source_0_0.set_gain(self.rfgain, 0)

    def get_ifgain(self):
        return self.ifgain

    def set_ifgain(self, ifgain):
        self.ifgain = ifgain
        self.osmosdr_source_0_0.set_if_gain(self.ifgain, 0)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_source_0_0.set_center_freq(self.frequency, 0)

    def get_bbgain(self):
        return self.bbgain

    def set_bbgain(self, bbgain):
        self.bbgain = bbgain
        self.osmosdr_source_0_0.set_bb_gain(self.bbgain, 0)

    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.osmosdr_source_0_0.set_antenna(self.antenna, 0)


def main(top_block_cls=dttsprx3, options=None):

    tb = top_block_cls()
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
