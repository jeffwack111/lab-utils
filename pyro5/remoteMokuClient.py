import Pyro5.client
from moku.instruments import MultiInstrument, LaserLockBox, DigitalFilterBox, FrequencyResponseAnalyzer, SpectrumAnalyzer

MIM = Pyro5.client.Proxy("PYRONAME:remoteMIM")

connections = [dict(source="Input1", destination="Slot1InA"), # REFL PD to demodulation in laser lock box
               dict(source="Input2", destination="Slot1InB"), # TRANS PD to monitor in laser lock box
               dict(source="Slot1OutA", destination="Slot3InA"), # PID output -control signal- to summing junction in digital filter box
               dict(source="Slot1OutA", destination="Slot4InA"), #control signal to spectrum analyzer
               dict(source="Slot1OutA", destination="Slot2InB"), #control signal to slot B of frequency response analyzer
               dict(source="Slot1OutB",destination="Output3"), # modulation signal to EOM
               dict(source="Slot2OutA", destination="Slot3InB"), #Excitation signal from frequency response analyzer to summing junction in digital filter box
               dict(source="Slot3OutA", destination="Slot2InA"), #control signal plus excitation to slot A of frequency response analyzer
               dict(source="Slot3OutA", destination="Output1"), #control signal plus excitation goes to actuator
               dict(source="Slot3OutA",destination = "Slot4InB") #control signal plus excitation to spectrum analyzer
               ]

MIM.set_connections(connections=connections)

