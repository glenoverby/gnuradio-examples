# gnuradio-examples

This is a collection of GNU Radio Companion flow graphs that I use with
either a Lime SDR or a Hackrf.

I'm providing both the .grc files and an image of the flowgraph.
I hope this "future proofs" these flowgraphs against changes to the .grc file format.
I'm doing this because I've found many flowgraphs on people's blogs, etc. that
are no longer readable by gnuradio-companion

My goal is to get data in and out of the dttsp SDR. Dttsp's I/O is through
the JACK audio connection kit at normal audio transfer rates (48khz, 96khz,
192khz).
These flowgraphs are intended to connect the LimeSDR to JACK, by providing
decimation and interpolatoin to and from a 48khz bandwidth signal.


* lime-TX-1 transmits a sine wave generated at 48khz and resampled to
6.72mhz.
This uses an output sample rate that is an even multiple of the input sample
rate of 48khz. This means the Rational Resampler only interpolates.
The LimeSDR board has a minimum transmit low-pass filter of 5mhz.
If that is not met, this error message is produced on start-up:
```
 [ERROR] setBandwidth(Tx, 0, 1.44 MHz) Failed - Tx lpf(1.44 MHz) out of range 5-40 MHz and 50-130 MHz
```
Further discussion of this is here: (https://discourse.myriadrf.org/t/simple-sinewave-strangeness/1443/5)

* lime-TX-2 transmits a sine wave generated at the output rate of 8mhz.

* lime-RX-1 receives and decimates the signal to 48khz

* dttsprx3 is a no-GUI receiver that decimates the 8.016MHz input signal to 48khz and routes it to JACK
* udpserver runs dttsprx3 and provides a control server compatible with the
usbsoftrock tool run in daemon mode.
With this, I am able to use sdr-shell (and similar tools).
* dttsprxtx1 is a no-GUI transmitter and receiver similar to dttsprx3.
* gnoise1 transmits the output of the Gaussian noise source with as wide of a bandwidth as possible.
I use this to test filters by transmitting into them with this flowgraph and
looking at the filter's output on a spectrum analyzer.

I've found that the receivers consume an entire core on my system
(Intel Core i5 Sandybridge), and the transmitters will consume BOTH cores.

