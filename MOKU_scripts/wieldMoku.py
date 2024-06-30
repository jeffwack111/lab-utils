import numpy as np
from wield.control import SISO
from moku.instruments import MultiInstrument, LaserLockBox, DigitalFilterBox, FrequencyResponseAnalyzer, SpectrumAnalyzer

def standard_MultiInstrument(IP):
    MIM = MultiInstrument(IP, force_connect=True, platform_id=4)

    print("creating instruments")
    llb = MIM.set_instrument(1, LaserLockBox)
    fra = MIM.set_instrument(2, FrequencyResponseAnalyzer)
    dfb = MIM.set_instrument(3, DigitalFilterBox)
    spa = MIM.set_instrument(4, SpectrumAnalyzer)

    print("connecting instruments")
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

    print("setting defaults")
    #set inputs
    MIM.set_frontend(1,"50Ohm","AC","0dB")
    MIM.set_frontend(2,"1MOhm","DC","0dB")

    #set outputs
    MIM.set_output(1, "0dB") #to laser
    #MIM.set_output(2, "0dB") #to piezo
    MIM.set_output(3, "14dB") #to EOM

    dfb.set_control_matrix(1, input_gain1=1, input_gain2=1)
    dfb.set_control_matrix(2, input_gain1=0, input_gain2=0)

    filter_coefficients = [
        [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
        [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
        [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
        [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000]]

    dfb.set_custom_filter(1, "39.06MHz", coefficients=filter_coefficients) 

    dfb.set_input_gain(1,gain = 0)
    dfb.set_output_gain(1,gain = 0)

    dfb.enable_output(1,True,True)

    llb.set_demodulation(mode="Modulation",frequency=50.6e6,phase=54)
    llb.set_aux_oscillator(enable = True,frequency=50.6e6,amplitude=2,output = "OutputB")
    llb.set_output(2, signal=False, output=True)

    llb.set_output_offset(1, offset=0.0)

    llb.set_monitor(1, 'ErrorSignal')
    llb.set_monitor(2, 'Input2')
    llb.set_acquisition_mode(mode="Precision")
    llb.set_trigger(type="Edge", source="Scan", level=0,edge="Rising")

    return MIM, llb, fra, dfb, spa


def set_controller(MokuLaserLockBox,prop_gain_dB,int_crossover_Hz,int_saturation_dB):
    MokuLaserLockBox.set_pid_by_frequency(channel=1,  int_crossover = int_crossover_Hz, int_saturation = int_saturation_dB,prop_gain = prop_gain_dB, diff_crossover = None,diff_saturation =None, double_int_crossover = None,invert=True)
    return PIS_controller(prop_gain_dB,int_crossover_Hz,int_saturation_dB)

def PIS_controller(prop_gain_dB,int_crossover_Hz,int_saturation_dB):
    int_crossover = int_crossover_Hz*2*np.pi #convert from hz to rad/s
    int_saturation_mag = 10**(int_saturation_dB/20)
    prop_gain_mag = 10**(prop_gain_dB/20)
    return SISO.zpk([-int_crossover],[-int_crossover*prop_gain_mag/int_saturation_mag],prop_gain_mag)

def aquire_lock(MokuLaserLockBox):
    scan_freq = 10
    scan_amp = 1
    MokuLaserLockBox.set_scan_oscillator(enable=True,amplitude = scan_amp, frequency = scan_freq, output ="OutputA",shape =  "Triangle")
    MokuLaserLockBox.set_output(1, signal=False, output=True)
    MokuLaserLockBox.set_timebase(0.0,1/(4*scan_freq))
    data = MokuLaserLockBox.get_data(wait_complete=True)
    t = np.array(data['time'])
    err = np.array(data['ch1'])
    trans = np.array(data['ch2'])
    med_err = np.median(err)
    t_res = t[np.argmax(trans)]
    V_res = scan_amp*t_res*4*scan_freq
    MokuLaserLockBox.set_setpoint(-med_err)
    MokuLaserLockBox.set_output_offset(1,offset=V_res)
    MokuLaserLockBox.set_scan_oscillator(enable=False,amplitude = scan_amp, frequency = scan_freq, output ="OutputA",shape =  "Triangle")
    MokuLaserLockBox.set_output(1, signal=True, output=True)