# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 20:24:02 2019

@author: Administrator
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import keysightSD1
import time
import warnings
from tqdm import tqdm
from instrumentserver.client import Client

cli = Client()
MXA = cli.get_instrument('MXA')
AWGSlot = 8
AWGChannel1 = 3
AWGChannel2 = 4
AWGAmp = 0.3 * 1.5
SSB_freq = 0e6 # Hz
markerSlot = 3
markerChannel = 2
center_freq  = 7.7654433e9

def configPXIe():
    AWG1 = keysightSD1.SD_AOU()
    AWG1_ID = AWG1.openWithSlot("", 1, AWGSlot)
    MARK1 = keysightSD1.SD_AOU()
    MARK1_ID = MARK1.openWithSlot("", 1, markerSlot)
    
    AWG1.channelWaveShape(AWGChannel1, keysightSD1.SD_Waveshapes.AOU_SINUSOIDAL)
    AWG1.channelWaveShape(AWGChannel2, keysightSD1.SD_Waveshapes.AOU_SINUSOIDAL)
    AWG1.channelAmplitude(AWGChannel1, AWGAmp)
    AWG1.channelAmplitude(AWGChannel2, AWGAmp)
    AWG1.channelFrequency(AWGChannel1, np.abs(SSB_freq))
    AWG1.channelFrequency(AWGChannel2, np.abs(SSB_freq))
    
    MARK1.AWGqueueConfig(markerChannel, 1)
    MARK1.channelWaveShape(markerChannel, keysightSD1.SD_Waveshapes.AOU_DC)
    MARK1.channelAmplitude(markerChannel, 1.5)
    return AWG1

def sweepBothDCOffset(AWG1, resOffset=np.zeros(2), precision=[0, 1, 2, 3], plot=0):
    MXAList = np.zeros(101)
    for j in tqdm(precision):
        offsetList = np.linspace(-0.5, 0.5, 101) / 10**j + resOffset[0]
        for i in range(101):
            AWG1.channelOffset(AWGChannel1, offsetList[i])
            time.sleep(0.02)
            specData = MXA.get_data(mute = True)
            MXAList[i] = specData[501, 1]
        
        resOffset[0] = offsetList[np.argmin(MXAList)]
        AWG1.channelOffset(AWGChannel1, resOffset[0])
        time.sleep(0.5)

        if plot:
            plt.figure('offset1')
            plt.plot(offsetList, MXAList)
        
        offsetList = np.linspace(-0.5, 0.5, 101) / 10**j + resOffset[1]
        for i in range(101):
            AWG1.channelOffset(AWGChannel2, offsetList[i])
            time.sleep(0.02)
            specData = MXA.get_data(mute = True)
            MXAList[i] = specData[501, 1]
        
        resOffset[1] = offsetList[np.argmin(MXAList)]
        AWG1.channelOffset(AWGChannel2, resOffset[1])
        time.sleep(0.5)
        if plot:
            plt.figure('offset2')
            plt.plot(offsetList, MXAList, label=str(resOffset[1]))
        plt.legend()
    return resOffset

def sweepIQ(AWG1, resIQ = np.zeros(2), precision=[0, 1, 2, 3], plot=0):
    MXAList = np.zeros(101)
    resIQ = np.zeros(2)
    resIQ[1] = AWGAmp
    for j in tqdm(precision):
        AWG1.channelPhaseResetMultiple(int("1111",2))
        phaseList = np.linspace(-180, 180, 101) / 5**j + resIQ[0]
        for i in range(101):
            AWG1.channelPhase(AWGChannel2, phaseList[i])
            time.sleep(0.02)
            specData = MXA.get_data(mute = True)
            MXAList[i] = specData[501, 1]
        
        resIQ[0] = phaseList[np.argmin(MXAList)]
        AWG1.channelPhase(AWGChannel2, resIQ[0])
        time.sleep(0.1)

        if plot:
            plt.figure('phase')
            plt.plot(phaseList, MXAList)
            
        iqScaleList = (np.linspace(-0.3, 0.3, 101) / 5**j + resIQ[1])
        if np.max(iqScaleList)>1:
            warnings.warn('AWG amplitude over flow. If keeping giving wrong result,\
            try to make sure AWGAmp < 1.5')
        
        for i in range(101):
            AWG1.channelAmplitude(AWGChannel2, iqScaleList[i])
            time.sleep(0.02)
            specData = MXA.get_data(mute = True)
            MXAList[i] = specData[501, 1]
        
        resIQ[1] = iqScaleList[np.argmin(MXAList)]
        AWG1.channelAmplitude(AWGChannel2, resIQ[1])
        time.sleep(0.1)

        if plot:
            plt.figure('iqScale')
            plt.plot(iqScaleList, MXAList)
    resIQ[1] /= AWGAmp
    return resIQ

def main(GenFreq,  precisionDC=[0, 1, 2, 3], precisionIQ=[0, 1, 2, 3], plot_=0):
    AWG1 = configPXIe()
    resIQ = [90, 1]

    if SSB_freq != 0:
        MXA.set_frequency_center(GenFreq + SSB_freq)
        MXA.set_frequency_span(1e6)
        resIQ = sweepIQ(AWG1, precision=precisionIQ, plot=plot_)

    MXA.set_frequency_center(GenFreq)
    MXA.set_frequency_span(1e6)
    resOffset = sweepBothDCOffset(AWG1, precision=precisionDC, plot=plot_)


    MXA.set_frequency_center(GenFreq)
    if SSB_freq != 0:
        MXA.set_frequency_span(np.abs(SSB_freq) * 3)
    else:
        MXA.set_frequency_span(1e6)
    if plot_:
        plt.figure()
        specData = MXA.get_data(mute = True)
        plt.plot(specData[:, 0], specData[:, 1])
    infoYamlFormatPrint(resOffset, resIQ)
    AWG1.close()
    return resOffset, resIQ

    
def quickCheck(resOffset, resIQ):
    AWG1 = configPXIe()
    AWG1.channelOffset(AWGChannel1, resOffset[0])
    AWG1.channelOffset(AWGChannel2, resOffset[1])
    AWG1.channelPhaseResetMultiple(int("1111",2))
    AWG1.channelPhase(AWGChannel2, resIQ[0])
    AWG1.channelAmplitude(AWGChannel2, resIQ[1] * AWGAmp)
    AWG1.channelAmplitude(AWGChannel1, AWGAmp)
    plt.figure()
    specData = MXA.get_data(mute = True)
    plt.plot(specData[:, 0], specData[:, 1])


def infoYamlFormatPrint(resOffset, resIQ):
    print (f"offset:  {np.round(resOffset[0], 5)}, {np.round(resOffset[1], 5)}")
    print (f"iqScale: {np.round(resIQ[1], 5)}, skewPhase: {np.round(resIQ[0], 5)}")


if __name__=='__main__':

    resOffset, resIQ = main(center_freq, precisionDC=[0, 1, 2, 3], precisionIQ=[0, 1, 2, 3, 4], plot_=1)

    # quickCheck(np.array([-0.074244, -0.011932]), np.array([0, 1]))
    
    plt.show()