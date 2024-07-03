import Pyro5.client
from moku.instruments import MultiInstrument, LaserLockBox, DigitalFilterBox, FrequencyResponseAnalyzer, SpectrumAnalyzer

llb = Pyro5.client.Proxy("PYRONAME:llb3")

print(llb.summary()) 
