# import numpy as np
# from numpy import cos, sin, exp, pi

# from collections import deque

# # SPFPM library for fixed point python numbers
# from FixedPoint import FXnum, FXfamily

# # Import for plotting
# from pylab import plot, show, grid, xlabel, ylabel


"""Create plots of signals generated by chirp() and sweep_poly()."""

import numpy as np
from numpy import cos, sin, pi
from scipy.signal.waveforms import chirp, sweep_poly
from scipy.signal import hilbert, decimate

from scipy.fft import fft, ifft

from numpy import poly1d

# TODO remove pylab; no longer recommended
from pylab import figure, plot, show, xlabel, ylabel, subplot, grid, title, \
                    yscale, savefig, clf


import matplotlib.pyplot as plt

import math
import random


FIG_SIZE = (7.5, 3.75)


# f0 = start freq
# f1 = end freq
# t1 = time of sweep
# t_f = fraction to generate
# fs = sample freq
# osf = oversampling factor
def make_linear(f0, f1, t1, t_f, fs, tstart=0.0, osf=1, returnWaveform=False, 
                makeComplex=False, negateFrequency=False, filename=None,  fig_size=FIG_SIZE):
    
    ttot = t1 * t_f     # total time
    n_samps = int(ttot * fs * osf)

    t_samps = np.linspace(tstart, ttot + tstart, n_samps)
    
    f_t = np.linspace(0, ttot, n_samps) # overriden later - FIX
    
    if not makeComplex:
        w = np.linspace(0, ttot, n_samps)         # overriden later - FIX
    else:
        w = [0+0j] * n_samps

    c = (f1 - f0) / t1      # 'chirpyness' (aka alpha)

    #45-5 / t1 = 40 Hz/s

    #-45 - (-5) / t1
    #-5 - (-45) / t1 = 40 / Hz/z  <- when inverting the frequency

    # f(t) = ct + fo
    # ph = ph0 + 2pi (c/2. t^2 + fo.t)

    # Sample period
    ts = 1 / fs

    ph0 = 0     # start phase of the chirp

    pi2 = 2*np.pi
    for i in range(len(t_samps)): 

        # Not used        
        #r_t(i) = d0 + v0*t(i)
        #td(i) = 2*r_t(i)/c
        #Tx(i) = cos(2*pi*(fc*t(i) + slope*t(i)^2/2))
        #w[i] = cos(2*pi*(fc*it(i) - td(i)) + i*\(t(i) - td(i))^2/2))
        # ----------
        
        t = i * ts / osf    # time corresponding to index
                                     # this should be in t_samps.. FIX

        f_t[i] = c*t + f0            # frequency

        if negateFrequency:
            ph = ph0 + pi2 * (c/2 * t*t - f0 * t)
        else:
            ph = ph0 + pi2 * (c/2 * t*t + f0 * t)

        ph_mod = math.fmod(ph, pi2) # phase modulo 2pi
        
        if not makeComplex:
            w[i] = cos(ph_mod)
        else:
            if negateFrequency:
                w[i] = cos(ph_mod) - sin(ph_mod) * 1j
            else:
                w[i] = cos(ph_mod) + sin(ph_mod) * 1j

        # Not needed below, ignore
        #Rx(i) = cos(2*pi*(fc*(t(i) - td(i)) + slope*(t(i) - td(i))^2/2))
        #Mix(i) = Tx(i) * Rx(i)
    
        # Read this post: https://stackoverflow.com/questions/51006591/how-to-concatenate-sine-waves-without-phase-jumps
        # con = math.fmod(2.0 * np.pi * f * CHUNK/RATE + con, 2.0 * np.pi)

        #  a * sin(2π * (f * t + con))

    # ------

    if returnWaveform:
        return w

    figure(1, figsize=fig_size)
    clf()

    subplot(2,1,1)
    plot(t_samps, w)
    tstr = "Linear Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1)
    title(tstr)

    subplot(2,1,2)
    plot(t_samps, f_t, 'g')
    grid(True)
    ylabel('Frequency (Hz)')
    xlabel('time (sec)')


    if filename is None:
        show()
    else:
        savefig(filename)

# note used
def make_quadratic(f0, t1, f1, filename=None, fig_size=FIG_SIZE):
    t = np.linspace(0, t1, 5001)
    w = chirp(t, f0=f0, f1=f1, t1=t1, method='quadratic')

    figure(1, figsize=fig_size)
    clf()

    subplot(2,1,1)
    plot(t, w)
    tstr = "Quadratic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1)
    title(tstr)

    subplot(2,1,2)
    plot(t, f0 + (f1-f0)*t**2/t1**2, 'r')
    grid(True)
    ylabel('Frequency (Hz)')
    xlabel('time (sec)')
    if filename is None:
        show()
    else:
        savefig(filename)

def make_quadratic_v0false(f0, t1, f1, filename=None, fig_size=FIG_SIZE):
    t = np.linspace(0, t1, 5001)
    w = chirp(t, f0=f0, f1=f1, t1=t1, method='quadratic', vertex_zero=False)

    figure(1, figsize=fig_size)
    clf()

    subplot(2,1,1)
    plot(t, w)
    tstr = "Quadratic Chirp, f(0)=%g, f(%g)=%g (vertex_zero=False)" % (f0, t1, f1)
    title(tstr)

    subplot(2,1,2)
    plot(t, f1 - (f1-f0)*(t1-t)**2/t1**2, 'r')
    grid(True)
    ylabel('Frequency (Hz)')
    xlabel('time (sec)')
    if filename is None:
        show()
    else:
        savefig(filename)

def make_logarithmic(f0, t1, f1, filename=None, fig_size=FIG_SIZE):
    t = np.linspace(0, t1, 5001)
    w = chirp(t, f0=f0, f1=f1, t1=t1, method='logarithmic')

    figure(1, figsize=fig_size)
    clf()

    subplot(2,1,1)
    plot(t, w)
    tstr = "Logarithmic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1)
    title(tstr)

    subplot(2,1,2)
    plot(t, f0 * (f1/f0)**(t/t1), 'r')
    # yscale('log')
    grid(True)
    ylabel('Frequency (Hz)')
    xlabel('time (sec)')
    if filename is None:
        show()
    else:
        savefig(filename)

def make_hyperbolic(f0, t1, f1, filename=None, fig_size=FIG_SIZE):
    t = np.linspace(0, t1, 5001)
    w = chirp(t, f0=f0, f1=f1, t1=t1, method='hyperbolic')

    figure(1, figsize=fig_size)
    clf()
    
    subplot(2,1,1)
    plot(t, w)
    tstr = "Hyperbolic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1)
    title(tstr)

    subplot(2,1,2)
    plot(t, f0 * f1 * t1 / ((f0 - f1)*t + f1*t1), 'r')
    grid(True)
    ylabel('Frequency (Hz)')
    xlabel('time (sec)')
    if filename is None:
        show()
    else:
        savefig(filename)

def make_sweep_poly(filename=None, fig_size=FIG_SIZE):
    p = poly1d([0.05, -0.75, 2.5, 5.0])
     
    t = np.linspace(0, t1, 5001)
    w = sweep_poly(t, p)

    figure(1, figsize=fig_size)
    clf()
    
    subplot(2,1,1)
    plot(t, w)
    tstr = "Sweep Poly, $f(t) = 0.05t^3 - 0.75t^2 + 2.5t + 5$"
    title(tstr)

    subplot(2,1,2)
    plot(t, p(t), 'r')
    grid(True)
    ylabel('Frequency (Hz)')
    xlabel('time (sec)')
    if filename is None:
        show()
    else:
        savefig(filename)

def signal_chirp():
    from scipy.signal import chirp, spectrogram
    import matplotlib.pyplot as plt

    t = np.linspace(0, 10, 5001)
    w = chirp(t, f0=6, f1=1, t1=10, method='linear')
    plt.plot(t, w)
    plt.title("Linear Chirp, f(0)=6, f(10)=1")
    plt.xlabel('t (sec)')
    plt.show()

if __name__ == "__main__":

    #signal_chirp()
    #exit()

    # Generate chirp time series
    f0 = 2.5    # MHz
    f1 = 45     # MHz
    tsw = 320   # JORN sweep duration ~320sec
    t_frac = 1  # only produce a portion of the sweep -> but with same sweep rate

    tstart = 6  # start of JORN sweep
                # Note 1: this is combination of:
                #   propagation time to our receiver (in microseconds) - which depends on ionospheric height;
                #   and the delay from a defined UTC epoch time, to the start of the chosen sounder we are
                #   receiving from.
                #
                # Sounders run on a schedule
                # TODO MORE TO COME


    fs = 63     # Sample rate (MSa/s)
    duration = tsw * t_frac
    
    # Sweep/ chirp rate ("chirpyness")
    a = (f1-f0) / tsw

    # Transmit this at a certain time. Using "rect" command from
    # http://www.ece.uah.edu/courses/material/EE710-Merv/Stretch_11.pdf

    T_t = tsw * t_frac  # The duration of the transmitted signal
    T_r = tstart + duration/2 # See Note 1 above

    T_m = 0             # Note 2: The time alignment of the 'heterodyne' i.e. the timing of the swept NCO
                        # m stands for 'mixer/match'
                        # See pdf - T_r and T_m should be close
                        # Set below.

    T_h = 0             # Time *duration* of the heterodyne (i.e. mixing), set below

    # ==================================
    # Timing requirements - see pdf
    # ----------------------------------
    # We want T_rmax + T_t / 2 <= T_m + T_h / 2

    # Requirement for T_h
    # T_h > dT_r + T_t
    # where dT_r = delta_T_r = T_rmax - T_rmin        <- from ionospheric layer heights

    # T_m - T_rmin <= T_r <= T_rmax + T_m
    # Then hs(t) (the heterodyned/ deramped signal) completely overlaps the received signals

    c = 3e8 # speed of light, m/s

    rmax = 1000e3       # max ionospheric height - research the actual heights you care about!
    rmin = 20e3         #

    # Delays for perfect (mirror) reflection off those heights, from transmitter to our receiver
    #
    tx_rx_ground_range = 1234e3     # random number chosen; this needs to determined

    # t = 2R/c
    T_rmax = 2 * np.sqrt((tx_rx_ground_range/2)**2 + rmax**2) / c     # pythagoras
    T_rmin = 2 * np.sqrt((tx_rx_ground_range/2)**2 + rmin**2) / c     # pythagoras
    
    print ("Max range delay %f, min %f" % (T_rmax, T_rmin))
    dT_r = T_rmax - T_rmin

    # FIXME TEMP
    #dT_r = 0

    # Exaggerates the time delay of echoes, since in this sim, we are sampling much slower
    exaggerate_time_delay = 1000

    # Set the duration of the mixing required
    T_h = (dT_r * exaggerate_time_delay) + T_t
    print("Required minimum heterodyne/mixing duration: %f" % T_h)

    # Note: the above will need to be determined experimentally, by changing T_m to match
    #   the transmit time (T_r) of a JORN sounder.
    # It is used here mainly for simulation.

    # Also note; this is dominated almost entirely by the sweep duration, and not the propagation
    #  delays

    # 1] Create the transmit chirp
   
    # Note: This creates a chirp with only positive frequencies;
    #
    # hence, according to the paper, this is already mutiplied by rect(t - T_r / T_t)
    # Where T_t is the transmit duration, here tsw * t_frac and t_r is 0 + T_t/2

    # All these waveforms are generated with 1/(fs * OSF) coarseness
    # In reality, the timing fineness is 1/fs samples worth, approx 1/63e6 sec.
    # In simulation, we remove the x10e6 (all MHz become Hz, all MSa/s become Sa/S)

    OSF =  10    # oversampling factor; basically increases fs

    waveform = make_linear(f0, f1, tsw, t_frac, fs, tstart, OSF, returnWaveform=True) #, 'chirp_linear.png')

    transmit_chirp = waveform                           

    # Apply a test modulation:
    # NOT USED
    samples = int(fs*duration)
    t = np.arange(samples * OSF) / (fs * OSF) + tstart
    #transmit_chirp *= 1 + 0.1 * np.cos(2 * np.pi * t)

    #transmit_chirp *= 0.1


    # Random noise
    #for i in range(len(transmit_chirp)):
#        transmit_chirp[i] *= random.uniform(0.95,1)

    # Additive white noise
    #for i in range(len(transmit_chirp)):
    #    transmit_chirp[i] += 0.25 * random.uniform(0.95,1)

    ########################################
    # Generate heterodyne = mixer waveform.
    
    # Mixer duration is T_h
    # We want same sweep rate, a

    # Mixer start and stop frequency determined by mismatch of Tr and Tm
    # hence mixer start freq:
        
    a_mixer = a

    dT = (T_h - T_t) / 2     # additional time for heterodyne
    
    T_h += 2                 # increase the heterodyne artificially 
                             # - not essential, but allows noise either side of the received waveform to be viewed

    T_m = T_r                   # T_m is to be set according to note 2.
                                # This cannot exceed the absolute value of difference between  
                                # (T_h - T_t) / 2, i.e. dT
                                #
                                

    # Define details of the echoes to be received
    numEchoes = 10

    timerange = abs((T_h - T_t) / 2)  
    timerange = dT/2

    print(timerange)

    # Create an array of random receive times for each echo
    T_rs = [T_r + random.uniform(-timerange, timerange) for i in range(numEchoes+1)]

    Tafter = dT - (T_r-T_m)     # see the figures in the stretch pdf for logic    
    Tbefore = dT + (T_r-T_m)

    # Time before and after each echo, relative to the mixer time

    # Calculate an array of durations
    Tbefore_s = [x - T_m + dT for x in T_rs]

    print(T_rs)
    print(Tbefore_s)
    #print ("Tbefore %f, Tafter %f" % (Tafter, Tbefore))

    # Calculate the start and stop frequencies for the mixer

    fc = (f0 + f1)/2         # centre frequency of transmit sweep

    f_m_sw = (T_h * a_mixer) # swept bandwidth of mixer

    f_m0 = fc - f_m_sw/2     # start freq for mixer
    f_m1 = fc + f_m_sw/2     # stop freq for mixer

    # These compress the pulse
    # mixer_waveform = make_linear(-f_m1, -f_m0, T_h, t_frac, fs, 0, OSF, 
    #                             returnWaveform=True, makeComplex=True, negateFrequency=False)
    # #mixer_waveform = make_linear(-f_m1, -f_m0, T_h, t_frac, fs, 0, OSF, 
    #                             returnWaveform=True, makeComplex=True, negateFrequency=True)
    
    # This allows follow on stretch processing
    mixer_waveform = make_linear(f_m0, f_m1, T_h, t_frac, fs, 0, OSF, 
                                 returnWaveform=True, makeComplex=True, negateFrequency=False)

    #print("%d  %d" % (len(transmit_chirp), len(mixer_waveform)))

    # Expand receive waveform vector and align it according to the offset of T_r and T_m.

    # To align the received and mixing waveforms, we need to use the start times
    # not the centre frequency times, T_r (T_rs) and T_m
    # 
    # They are:  tstart (for the receive waveform) and tm_start:
    tm_start = T_m - T_h/2

    # Determine where to insert the receive waveforms relative to the mixer waveform
    
    print("T_m %f, T_h %f, T_t %f" % (T_m, T_h, T_t))
    print("Tstart %f, tm_start %f" % (tstart, tm_start))

    receive_waveform = [0.0 * len(mixer_waveform)]  # create an empty array

    for tb in Tbefore_s:    # for each 'time before' (tb) in the array Tbefore_s
        Nlead = round(tb * fs * OSF)    # find leading samples
        Ntrail = 0

        # find the difference
        Ndiff = -Nlead - len(transmit_chirp) + len(mixer_waveform)
        # and add it to the end of the wavevform
        Ntrail += Ndiff

        # Pad start with 0s based on the delay between receive and mixer
        single_receive_waveform = np.pad(transmit_chirp, (Nlead, Ntrail), 'constant')
        
        # Attenuate
        #single_receive_waveform *= random.uniform(0.1,0.5)

        # Add noise
        #single_receive_waveform += 0.25 * random.uniform(0.95,1)
        
        # Add this new single receive waveform to the combined receive_waveform
        receive_waveform += single_receive_waveform

    print ("Len receiver %d, len mixer %d" % (len(receive_waveform), len(mixer_waveform)))

    # Separate real and imaginary for demodulating/ filtering etc
    # FIXME: use separate I and Q throughout
    mixer_i = np.real(mixer_waveform)
    mixer_q = np.imag(mixer_waveform)

    # Create an array corresponding to the collection time
    t_all = np.linspace(tm_start, T_h + tm_start, len(mixer_waveform))

    # Print the transmit and heterodyne waveforms
    # TODO

    # Calculated the stretched processing
    dechirp = receive_waveform * mixer_waveform

    # DEBUG CODE - PLOT FFT (FIXME needs fixing)
    # --------------------------------------------------------
    # y = fft(dechirp)
    # N = len(mixer_waveform)

    # # sample spacing
    # T = 1/fs

    # x = np.linspace(0.0, N*T, N)
    
    # xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    
    # #import matplotlib.pyplot as plt
    # plt.semilogy(xf, 2.0/N * np.abs(y[0:N//2]))
    # #plt.semilogy(xf[1:N//2], 2.0/N * np.abs(ywf[1:N//2]), '-r')
    # plt.grid()
    # plt.show()
    
    # exit()
    # --------------------------------------------------------

    # Low pass filter the output
    from scipy import signal
    from scipy.signal import lfilter, firwin #, fftconvolve

    from helpers import mfreqz

    # Apply CIC decimation filters
    # TODO

    # Apply FIR filters (to correct CIC droop)
    # == Compensation FIR Filter
    #
    # Note: if CIC filters are applied, the required FIR design is changed
    # TODO: after applying CIC filters; this FIR is the CFIR / PFIR filter

    #  The following is used temporarily, only to Low pass filter the demodulated waveform


    # TODO - FIR filter to suit CIC filter above.
    numtaps = 2002
    bw = 0.001             
    f = bw / OSF

    n = numtaps
    b = signal.firwin(n, cutoff = f, window = "hamming")

    # Frequency and phase response
    #mfreqz(b)

    lpf_i = lfilter(b, [1.0], np.real(dechirp))
    lpf_q = lfilter(b, [1.0], np.imag(dechirp))

    lpf_complex = lfilter(b, [1.0], dechirp)

    complex2 = lpf_i + lpf_q * 1j

    # Plot freq response of fir filter
    # directly from: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.freqz.html
    #
    # w, h = signal.freqz(b)
    # fig, ax1 = plt.subplots()
    # ax1.set_title('Digital filter frequency response')

    # ax1.plot(w, 20 * np.log10(abs(h)), 'b')
    # ax1.set_ylabel('Amplitude [dB]', color='b')
    # ax1.set_xlabel('Frequency [rad/sample]')

    # ax2 = ax1.twinx()
    # angles = np.unwrap(np.angle(h))
    # ax2.plot(w, angles, 'g')
    # ax2.set_ylabel('Angle (radians)', color='g')
    # ax2.grid()
    # ax2.axis('tight')
    # plt.show()  

    # ==================================================
    # Window the time domain data
    M = int(len(complex2) * f/fs * 1000 / OSF)  # attempt to calculate desired decimation

    M = 1000   # set fixed decimation
    
    print ("Decimation %d" % M)
    decimate = complex2[1000::M]           #TODO-remove samples in transient, here starting 1000 samples in

    w = np.blackman(len(decimate))

    y = np.fft.fftshift(fft(decimate))
    ywf = np.fft.fftshift(fft(decimate*w))

    N = len(y)

    # sample spacing    TODO fix this: the frequency spacing is not correct for a full sweep.
    T = 1/(fs) * M

    x = np.linspace(0.0, N*T, N)

    #xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    xf = np.linspace(0.0, 1.0/(T), N)
    
    fig, ax1 = plt.subplots()
    
    #plt.semilogy(xf, 2.0/N * np.abs(y[0:N//2]))
    plt.semilogy(xf, 2.0/N * np.abs(y[0:N]))

    #plt.semilogy(xf, 2.0/N * np.abs(y[0:N//2]))
    plt.semilogy(xf[0:N], 2.0/N * np.abs(ywf[0:N]), '-r')

    plt.grid()
    plt.show()


    # =================================================
    # Plot the signal waveforms
    fig = plt.figure()
    ax0 = fig.add_subplot(311)
    ax0.plot(t_all, receive_waveform, label='received')
    ax0.set_xlabel("time in seconds")
    ax0.legend()

    ax1 = fig.add_subplot(313)
    #ax1.plot(t_all, np.abs(mixer_waveform), label='heterodyne')
    ax1.plot(x, np.abs(decimate), label='decimated')
    ax1.set_xlabel("time in seconds")
    ax1.legend()

    ax2 = fig.add_subplot(312)
    ax2.plot(t_all, np.abs(lpf_complex))
    ax2.plot(t_all, np.abs(complex2))           # this is the addition of I and Q, it is equivalent to lpf_complex

    ax2.set_xlabel("time in seconds")
    #ax1.set_ylim(0.0, a*duration + f0 + 1)  # +1 only to show the sweep
    ax2.legend()
    

    plt.show()

    # Spectrogram processing
    # TODO

    exit()

    ########################################################################################
    # Hilbert transform to produce analytic signal of chirp
    # From: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html
    analytic_signal = hilbert(transmit_chirp)
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) / (2.0*np.pi) * fs * OSF)

    # Cross-correlation method.
    # N/A

    # Matched filter method
    # NOT APPLIED; performing a matched filter on FPGA requires convolution of FFTs, 
    # which are hard to implement

    # Plot to test:
    
    

    fig = plt.figure()
    ax0 = fig.add_subplot(211)
    ax0.plot(t, transmit_chirp, label='signal')
    ax0.plot(t, amplitude_envelope, label='envelope')
    ax0.set_xlabel("time in seconds")
    ax0.legend()

    ax1 = fig.add_subplot(212)
    ax1.plot(t[1:], instantaneous_frequency)
    ax1.set_xlabel("time in seconds")
    ax1.set_ylim(0.0, a*duration + f0 + 1)  # +1 only to show the sweep

    plt.show()

    exit()






    # IGNORE BELOW, notes and code snippets only






    #--------------------------------
    # Original from https://scipy-cookbook.readthedocs.io/_downloads/chirp_plot.py
    f0 = 12.5
    t1 = 10.0
    f1 = 2.5

    make_linear(f0, t1, f1) #, 'chirp_linear.png')
    make_quadratic(f0, t1, f1, 'chirp_quadratic.png')
    make_quadratic_v0false(f0, t1, f1, 'chirp_quadratic_v0false.png')
    make_hyperbolic(f0, t1, f1, 'chirp_hyperbolic.png')
    make_logarithmic(f0, t1, f1, 'chirp_logarithmic.png')

    make_sweep_poly(filename='sweep_poly.png')

#https://viewer.mathworks.com/?viewer=plain_code&url=https%3A%2F%2Fau.mathworks.com%2Fmatlabcentral%2Fmlc-downloads%2Fdownloads%2Fsubmissions%2F28611%2Fversions%2F1%2Fcontents%2Flffm1.m&embed=web
# %function for Input LFM signal generation
# function [LFM,fre1,FLFM]=lffm1(BW,n,T)
# fc=10*10^6;
# alpha=(BW)/(T);%chirp rate
# disp(alpha);
# t=linspace(-T/2,T/2,n);%time interval
# ichannel=cos(2*pi*((fc)*t+alpha*t.^2));%real part
# %imaginary part
# qchannel=sin(2*pi*((fc)*t+alpha*t.^2));
# %computing linear frequency modulating waveform
# LFM=(ichannel+(1i*qchannel));
# LFM(2:1:10)=0;
# LFM(504:1:511)=0;
# disp(LFM);
# freqmin=fc-BW/2;%minimum frequency at t= -T/2;
# freqmax=fc+BW/2;%maximum frequnecy at t=  T/2;
# fre1=linspace(freqmin,freqmax,n);% frequency limitations
# FLFM=fftshift(fft(LFM));
# %plot(fre1,abs(FLFM));
# end
