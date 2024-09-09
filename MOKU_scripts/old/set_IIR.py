from moku.instruments import DigitalFilterBox

filter_coefficients = [
    [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
    [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
    [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
    [1.0000000000, 1.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000]]

DFB = DigitalFilterBox('192.168.50.57', force_connect=True, platform_id=4) #192.168.50.97 is the IP for Moku Pro 3

DFB.set_custom_filter(1, "39.06MHz", coefficients=filter_coefficients) 

DFB.set_frontend(1, "DC", "50Ohm", "0dB")

DFB.set_input_gain(1,gain = 0)
DFB.set_output_gain(1,gain = 0)

DFB.enable_output(1,True,True)

DFB.relinquish_ownership()