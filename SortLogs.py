import json
#import pandas as pd
import glob
#import matplotlib.pyplot as plt
import os

#os.system('pip install pandas')
#os.system('pip install matplotlib')

"""
#List all files in directory
for i in glob.glob("/Users/juanquintana/Desktop/JoeQC2.0/data/*.txt"):
    with open(f"/Users/juanquintana/Desktop/JoeQC2.0/data/{i}",'r') as file:
        #print(file.readlines())
        df = pd.read_csv(file)
        print(df)
"""
data={}
def EthernetCheckData():
    #Check Ethernet data and returns [okReads,failReads.totalReads]
    with open(f"/data/Ethernet_log.txt", 'r') as file:
        failReads=0
        totalReads=0
        for i in file.readlines():
            totalReads+=1
            if "Failed" in i:
                failReads+=1
        okReads = totalReads-failReads
    results=[okReads,failReads,totalReads]
    keys=["SuccessfullPing","FailedPing","TotalReads"]
    return dict(zip(keys,results))
result_ethernet=(EthernetCheckData())
def HardwareCheckData():
    with open("/data/Hardware_log.txt",'r') as file:
        okCamera=0
        okKeypad=0
        okPic18=0
        okScreen=0
        okCellModule=0
        okAudioCodec=0
        for i in file.readlines():
            if 'Microdia' in (i.strip().strip('\t').strip('\n')):
                okCamera+=1
            if 'Microchip' in (i.strip().strip('\t').strip('\n')):
                okPic18+=1
            if 'Chesen' in (i.strip().strip('\t').strip('\n')):
                okKeypad+=1
            if 'device_name' in (i.strip().strip('\t').strip('\n')):
                okScreen+=1
            if 'Cell_module_Enabled' in (i.strip().strip('\t').strip('\n')):
                okCellModule+=1
            if 'Audio_codec ON' in (i.strip().strip('\t').strip('\n')):
                okAudioCodec+=1
            result =[okCamera,okKeypad,okPic18,okScreen,okCellModule,okAudioCodec]
            keys = ["Camera_OK","Keypad_OK","Pic18_OK","Screen_OK","CellModule_OK","AudioCodec_OK"]
    return dict(zip(keys,result))
result_hardware=(HardwareCheckData())
def watchdogCheckData():
    with open("/data/PIC_watchdog.txt") as file:
        AACK = 0
        NACK = 0
        for i in file.readlines():
            if 'AACK_received' in (i.strip().strip('\t').strip('\n')):
                AACK+=1
            if 'Sent_NACK' in (i.strip().strip('\t').strip('\n')):
                NACK+=1
    result =[AACK,NACK]
    keys = ["Received_AACK","Sent_NACK"]
    return dict(zip(keys,result))
result_watchdog=(watchdogCheckData())
def resetCheckData():
    with open("/data/reset_log.txt") as file:
        failAACK = 0
        failPing= 0
        failPIC18 = 0
        failTouchScreen = 0
        failKeypad = 0
        failCamera = 0
        failAudio = 0
        for i in file.readlines():
            if 'Undetected_PIC18' in (i.strip().strip('\t').strip('\n')):
                failPIC18+=1
            if 'Undetected_Touchscreen' in (i.strip().strip('\t').strip('\n')):
                failTouchScreen+=1
            if 'Undetected_Keypad' in (i.strip().strip('\t').strip('\n')):
                failKeypad+=1
            if 'Undetected_Camera' in (i.strip().strip('\t').strip('\n')):
                failCamera+=1
            if 'Undetected_audio' in (i.strip().strip('\t').strip('\n')):
                failAudio+=1
            if 'Failed_ping' in (i.strip().strip('\t').strip('\n')):
                failPing+=1
            if 'Timeout No response AACK from PIC18' in (i.strip().strip('\t').strip('\n')):
                failAACK += 1
    result =[failAACK,failPing,failAudio,failCamera,failKeypad,failTouchScreen,failPIC18]
    keys = ["Failed_AACK","Failed_Ping","Failed_Audio","Failed_Camera","Undetected_Keypad","Undetected_touchscreen","Undetected_PIC18"]
    return dict(zip(keys,result))
result_reset = (resetCheckData())
"""
def watchdogStatus():
    with open("/Users/juanquintana/Desktop/TestDataOct22Oct25/dataJuan/Status_log.txt") as file:

watchdogStatus()

def graphResults(result):
    #Plot results in bar
    D = result
    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys()))
    # # for python 2.x:
    # plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
    # plt.xticks(range(len(D)), D.keys())  # in python 2.x
    return plt.show()
"""

#Join all results
data.update(result_ethernet)
data.update(result_hardware)
data.update(result_watchdog)
data.update(result_reset)
print(data)
uuid =os.getenv('RESIN_DEVICE_UUID')
json_object = json.dumps(data, indent = 4)
print(json_object)

with open(f'/data/Logs_{uuid}.json','a') as file:
    file.write(json_object)
"""
graphResults(result_ethernet)
graphResults(result_reset)
graphResults(result_watchdog)
graphResults(result_hardware)
"""
