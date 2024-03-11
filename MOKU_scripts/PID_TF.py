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
