import sys
import Pyro5.server
from moku.instruments import *

exposed_MultiInstrument = Pyro5.server.expose(MultiInstrument)

def serve_MultiInstrument(IP,MIM_name,instrument_classes,instrument_names):
    MIM = exposed_MultiInstrument(IP, force_connect=True, platform_id=4)

    instruments=[]

    for idx,inst in enumerate(instrument_classes):
        print(idx)
        instruments.append(MIM.set_instrument(idx+1,Pyro5.server.expose(inst)))

    dictionary = dict(zip(instruments,instrument_names))
    dictionary.update({MIM:MIM_name})

    Pyro5.server.serve(
        dictionary,
    use_ns=True, verbose=True, host="gouyvm")  

def standard_MultiInstrument(moku_number):

    IPdict = dict([('1' , "192.168.50.97"),('3' , "192.168.50.57"), ('4', "192.168.50.57")])

    print("creating instruments")
    serve_MultiInstrument(IPdict[moku_number],f"MIM{moku_number}",[LaserLockBox,FrequencyResponseAnalyzer,DigitalFilterBox,SpectrumAnalyzer],[f"llb{moku_number}",f"fra{moku_number}",f"dfb{moku_number}",f"spa{moku_number}"])

if __name__ == "__main__":
    standard_MultiInstrument(sys.argv[1])