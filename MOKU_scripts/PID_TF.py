from moku.instruments import MultiInstrument, PIDController, FrequencyResponseAnalyzer
MIM = MultiInstrument('192.168.50.97', force_connect=True, platform_id=4)

pid = MIM.set_instrument(1, PIDController)
fra = MIM.set_instrument(2, FrequencyResponseAnalyzer)

connections = [dict(source="Slot1OutA", destination="Slot2InA"),
               dict(source="Slot2OutA", destination="Slot1InA")]

MIM.set_connections(connections=connections)

#Set the PID controller
pid.set_by_frequency(channel=1, prop_gain=-30,int_crossover = 5e3,diff_crossover = 6e3,int_saturation = 0,diff_saturation = 20)
pid.enable_input(1, True)
pid.enable_output(1,True,True)

#Take a transfer function with the frequency response analyzer
fra.set_sweep(start_frequency=20e6, stop_frequency=10, num_points=256,
                averaging_time=1e-3, averaging_cycles=1, settling_cycles=1,
                settling_time=1e-3)
fra.set_output(1, 0.01)

delay = fra.start_sweep() 
print(delay)
data = fra.get_data(wait_complete = True)

print(data)

MIM.relinquish_ownership()
print("relinquished ownership")


