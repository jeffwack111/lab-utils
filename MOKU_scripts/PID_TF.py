from moku.instruments import MultiInstrument, PIDController, FrequencyResponseAnalyzer
import control as ct
import altair as alt
import pandas as pd

def PISDS_controller(prop_gain_dB,int_crossover,int_saturation_dB,diff_crossover,diff_saturation_dB):
    diff_saturation_mag = 10**(diff_saturation_dB/20)
    int_saturation_mag = 10**(int_saturation_dB/20)
    prop_gain_mag = 10**(prop_gain_dB/20)
    pid = ct.tf([1,diff_crossover,int_crossover*diff_crossover],[diff_crossover/prop_gain_mag,0])
    sat = ct.zpk([0],[-diff_crossover*diff_saturation_mag/prop_gain_mag,prop_gain_mag*int_crossover/int_saturation_mag],diff_crossover*diff_saturation_mag/prop_gain_mag)
    return ct.series(pid,sat)

#controller parameters:
prop_gain_dB=-30
int_crossover = 5e3
diff_crossover = 6e3
int_saturation_dB = 0
diff_saturation_dB = 20

#create model transfer function
model_TF = PISDS_controller(prop_gain_dB,int_crossover,int_saturation_dB,diff_crossover,diff_saturation_dB)

#Configure the MOKU to set and measure a PID controller with these parameters
MIM = MultiInstrument('192.168.50.97', force_connect=True, platform_id=4)

pid = MIM.set_instrument(1, PIDController)
fra = MIM.set_instrument(2, FrequencyResponseAnalyzer)

connections = [dict(source="Slot1OutA", destination="Slot2InA"),
               dict(source="Slot2OutA", destination="Slot1InA")]

MIM.set_connections(connections=connections)

#Set the PID controller
pid.set_by_frequency(channel=1, prop_gain=prop_gain_dB,int_crossover = int_crossover,diff_crossover = diff_crossover,int_saturation = int_saturation_dB,diff_saturation = diff_saturation_dB)
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



MIM.relinquish_ownership()
print("relinquished ownership")


