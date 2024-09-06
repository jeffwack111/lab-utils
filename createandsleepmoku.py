import Pyro5.client
import subprocess
from time import sleep

moku_number = 2

#start nameserver
devnull = subprocess.DEVNULL
subprocess.Popen(['nohup', 'pyro5-ns', '-n', '192.168.50.179'],stdout=devnull, stderr=devnull)
print("nameserver started")

#create instruments
subprocess.Popen(['nohup', 'python', '/home/lab/code/labutils/pyro5/serve.py', '3'], stdout=devnull, stderr=devnull)
sleep(60)

MIM = Pyro5.client.Proxy(f"PYRONAME:MIM{moku_number}")
llb = Pyro5.client.Proxy(f"PYRONAME:llb{moku_number}")
fra = Pyro5.client.Proxy(f"PYRONAME:fra{moku_number}")
dfb = Pyro5.client.Proxy(f"PYRONAME:dfb{moku_number}")
spa = Pyro5.client.Proxy(f"PYRONAME:spa{moku_number}")

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

llb.set_demodulation(mode="Modulation",frequency=51e6,phase=54)
llb.set_aux_oscillator(enable = True,frequency=51e6,amplitude=2,output = "OutputB")
llb.set_output(2, signal=False, output=True)

llb.set_output_offset(1, offset=0.0)

llb.set_monitor(1, 'ErrorSignal')
llb.set_monitor(2, 'Input2')
llb.set_acquisition_mode(mode="Precision")
llb.set_trigger(type="Edge", source="Scan", level=0,edge="Rising")
