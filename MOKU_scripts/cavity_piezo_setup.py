#Used to create the skeleton multi-instrument mode for locking an output filter cavity and taking transfer functions while locked. 
#Note that the code cannot currently configure output3 to the laser lock box C, that must be done manually. You'll have to manually change Out3 to +14 db.
from moku.instruments import MultiInstrument, LaserLockBox, DigitalFilterBox, FrequencyResponseAnalyzer, SpectrumAnalyzer
MIM = MultiInstrument('192.168.50.63', force_connect=True, platform_id=4)

print('setting instr.')
llb = MIM.set_instrument(1, LaserLockBox)
dfb = MIM.set_instrument(2, FrequencyResponseAnalyzer)
fra = MIM.set_instrument(3, DigitalFilterBox)
spa = MIM.set_instrument(4, SpectrumAnalyzer)
print("made devices")

connections = [dict(source="Input1", destination="Slot1InA"), # REFL PD to demodulator
               dict(source="Input2", destination="Slot1InB"), # TRANS PD to monitor
               #dict(source="Slot1OutC",destination="Output3"), # modulation to EOM, doesn't work
               dict(source="Slot1OutA", destination="Slot3InA"), # PID output to digital filter box
               dict(source="Slot1OutA", destination="Slot4InA"), 
               dict(source="Slot1OutA", destination="Slot4InB"),
               dict(source="Slot2OutA", destination="Slot3InB"),
               dict(source="Slot2OutB", destination="Output2"),
               dict(source="Slot3OutA", destination="Slot2InA"),
               dict(source="Slot3OutA", destination="Output1"),
               ]

print("made connections")


for x in connections:
    print(x)
    MIM.set_connections(connections=[x])
MIM.set_output(1, "0dB")
MIM.set_output(2, "0dB")
#MIM.set_output(3, "14dB") uncomment when output 3 can be set via the script
MIM.set_frontend(1,"50Ohm","AC","0dB")
MIM.set_frontend(2,"50Ohm","DC","0dB")
MIM.relinquish_ownership()
print("relinquish ownership")




