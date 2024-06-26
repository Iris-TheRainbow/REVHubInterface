# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]
# Embedded file name: REVHubInterface.py
import REVcomm
from REV2mSensor import REV2mSensor
from REVColorSensorV3 import REVColorSensorV3
from REVcomm import *
from functools import partial
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox, os, subprocess, time, platform, logging    
try:
    import ft232
except Exception as e: 
    print(platform.system)
    tkMessageBox.showerror('Drivers Not Detected', '\n\tPlease verify the correct drivers are installed. Windows 10 will automatically\n\tinstall the correct drivers when the Expansion Hub is plugged in. Windows 7 \n\trequires a manual install. Please see this link for the correct driver (FTDI D2xx):\n\thttps://www.ftdichip.com/Drivers/CDM/CDM21228_Setup.zip\n\n\tNote that firmware update will be unavailable.\nAlso, if you are using linux, this is normal (for now)\n\n\tMessage: \n\t' + str(e))

class device_info():

    def __init__(self, root, setAddress):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid(sticky=(N, S, E, W))
        self.device_info_frame = ttk.Frame(root)
        self.device_label = ttk.Label(self.device_info_frame)
        self.Frame_1 = tk.Frame(self.device_info_frame)
        self.Button_1 = ttk.Button(self.Frame_1)
        self.device_info_frame.config(height=100)
        self.device_info_frame.config(width=100)
        self.device_info_frame.grid(column=0)
        self.device_info_frame.grid(row=0)
        self.device_info_frame.grid(sticky=(N, S, E, W))
        self.device_info_frame.grid_rowconfigure(0, weight=1)
        self.device_info_frame.grid_columnconfigure(0, weight=1)
        self.device_label.config(text='Module: ')
        self.device_label.config(width=10)
        self.device_label.grid(column=1)
        self.device_label.grid(padx=5)
        self.device_label.grid(pady=5)
        self.device_label.grid(row=0)
        self.device_label.grid(sticky=E)
        self.Frame_1.config(height=200)
        self.Frame_1.config(width=200)
        self.Frame_1.grid(column=0)
        self.Frame_1.grid(row=0)
        self.Frame_1.grid(sticky=E)
        self.Button_1.config(command=setAddress)
        self.Button_1.config(text='Set Address')
        self.Button_1.grid(column=2)
        self.Button_1.grid(row=0)
        self.Button_1.grid(sticky=E)
        self.Button_1.config(width=10)
        vcmd = (
         root.register(self.validate_float), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.addr_entry = ttk.Entry(self.device_info_frame, validate='key', validatecommand=vcmd)
        self.addr_entry.config(width=10)
        self.addr_entry.grid(column=3)
        self.addr_entry.grid(padx=5)
        self.addr_entry.grid(pady=5)
        self.addr_entry.grid(row=0)
        self.addr_entry.grid(sticky=E)

    def validate_float(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if action == '1':
            if text in '0123456789':
                try:
                    if int(value_if_allowed) < 255 and int(value_if_allowed) > 0:
                        return True
                    else:
                        return False
                except ValueError:
                    return False
            else:
                return False
        else:
            return True


class firmware_tab():

    def __init__(self, root, chooseBin, flashNow):
        self.INTERFACE_VERSION = '1.2.1'
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid(sticky=(N, S, E, W))
        self.firmware_frame = ttk.Frame(root)
        self.firmware_label = ttk.Label(self.firmware_frame)
        self.warning_block = tk.Text(self.firmware_frame)
        self.Frame_1 = tk.Frame(self.firmware_frame)
        self.Button_1 = ttk.Button(self.Frame_1)
        self.Button_2 = ttk.Button(self.Frame_1)
        self.Device_info_frame1 = ttk.Frame(self.firmware_frame)
        self.firmware_frame.config(height=200)
        self.firmware_frame.config(width=200)
        self.firmware_frame.grid(column=0)
        self.firmware_frame.grid(row=0)
        self.firmware_frame.grid(sticky=(N, S, E, W))
        self.firmware_frame.grid_rowconfigure(0, weight=1)
        self.firmware_frame.grid_columnconfigure(0, weight=1)
        self.Device_info_frame1.config(height=100)
        self.Device_info_frame1.config(width=100)
        self.Device_info_frame1.grid(column=0)
        self.Device_info_frame1.grid(row=4)
        self.Device_info_frame1.grid(sticky=(N, S, E, W))
        self.Device_info_frame1.grid_rowconfigure(0, weight=1)
        self.Device_info_frame1.grid_columnconfigure(0, weight=1)
        self.firmware_label.config(text='Interface Version: ' + self.INTERFACE_VERSION)
        self.firmware_label.config(width=10)
        self.firmware_label.grid(column=0)
        self.firmware_label.grid(columnspan=2)
        self.firmware_label.grid(padx=5)
        self.firmware_label.grid(pady=5)
        self.firmware_label.grid(row=1)
        self.firmware_label.grid(sticky=(E, W))
        self.warning_block.config(background='#bcbcbc')
        self.warning_block.config(height=11)
        self.warning_block.config(width=50)
        self.warning_block.config(wrap='word')
        self.warning_block.grid(column=0)
        self.warning_block.grid(columnspan=2)
        self.warning_block.grid(row=0)
        self.warning_block.grid(sticky=(N, S, E, W))
        self.Frame_1.config(height=200)
        self.Frame_1.config(width=200)
        self.Frame_1.grid(column=0)
        self.Frame_1.grid(row=2)
        self.Frame_1.grid(sticky=W)
        self.Button_1.config(command=chooseBin)
        self.Button_1.config(text='Choose .bin file')
        self.Button_1.grid(column=0)
        self.Button_1.grid(row=0)
        self.Button_1.grid(sticky=W)
        self.Button_2.config(command=flashNow)
        self.Button_2.config(text='Flash')
        self.Button_2.grid(column=1)
        self.Button_2.grid(row=0)
        self.Button_2.grid(sticky=W)


class digital_single():

    def __init__(self, root, setInputCallback, setOutputCallback, digital_set, digital_poll):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid(sticky=(N, S, E, W))
        true = True
        self.var2 = IntVar()
        self.digital_panel = ttk.Frame(root)
        self.digital_label_1 = ttk.Label(self.digital_panel)
        self.Frame_1 = ttk.Frame(self.digital_panel)
        self.poll_button = ttk.Button(self.digital_panel)
        self.Separator_1 = ttk.Separator(self.Frame_1)
        self.State_label = ttk.Label(self.Frame_1)
        self.input_button = tk.Button(self.Frame_1)
        self.output_button = tk.Button(self.Frame_1)
        self.Checkbutton_1 = ttk.Checkbutton(self.Frame_1)
        self.digital_panel.config(height=200)
        self.digital_panel.config(padding=(5, 5, 5, 5))
        self.digital_panel.config(relief='groove')
        self.digital_panel.config(width=200)
        self.digital_panel.grid(column=0)
        self.digital_panel.grid(row=0)
        self.digital_panel.grid(sticky=(N, S, E, W))
        self.digital_panel.grid_rowconfigure(0, weight=1)
        self.digital_panel.grid_columnconfigure(0, weight=1)
        self.digital_label_1.config(takefocus=true)
        self.digital_label_1.config(text='Digital 0:')
        self.digital_label_1.config(width=8)
        self.digital_label_1.grid(column=0)
        self.digital_label_1.grid(columnspan=1)
        self.digital_label_1.grid(padx=0)
        self.digital_label_1.grid(pady=0)
        self.digital_label_1.grid(row=0)
        self.digital_label_1.grid(sticky=W)
        self.Frame_1.config(height=200)
        self.Frame_1.config(width=200)
        self.Frame_1.grid(column=1)
        self.Frame_1.grid(columnspan=1)
        self.Frame_1.grid(row=0)
        self.Frame_1.grid(sticky=(N, S, E, W))
        self.Separator_1.config(orient='vertical')
        self.Separator_1.grid(column=3)
        self.Separator_1.grid(padx=5)
        self.Separator_1.grid(row=1)
        self.Separator_1.grid(sticky=(N, S))
        self.State_label.config(text='State read:')
        self.State_label.grid(column=4)
        self.State_label.grid(row=1)
        self.input_button.config(background='#aaccff')
        self.input_button.config(command=setInputCallback)
        self.input_button.config(text='IN')
        self.input_button.grid(column=0)
        self.input_button.grid(row=1)
        self.input_button.grid(sticky=(N, S, E, W))
        self.output_button.config(command=setOutputCallback)
        self.output_button.config(text='OUT')
        self.output_button.grid(column=1)
        self.output_button.grid(row=1)
        self.output_button.grid(sticky=(N, S, E, W))
        self.Checkbutton_1.config(command=digital_set)
        self.Checkbutton_1.config(offvalue=0)
        self.Checkbutton_1.config(onvalue=1)
        self.Checkbutton_1.config(state='disabled')
        self.Checkbutton_1.config(variable=self.var2)
        self.Checkbutton_1.config(width=0)
        self.Checkbutton_1.grid(column=5)
        self.Checkbutton_1.grid(row=1)
        self.poll_button.config(command=digital_poll)
        self.poll_button.config(text='POLL')
        self.poll_button.config(width=5)
        self.poll_button.grid(column=2)
        self.poll_button.grid(row=0)
        self.poll_button.grid(sticky=E)


class analog_single():

    def __init__(self, root):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid(sticky=(N, S, E, W))
        self.analog_panel = ttk.Frame(root)
        self.analog_label_1 = ttk.Label(self.analog_panel)
        self.Frame_1 = ttk.Frame(self.analog_panel)
        self.voltage_label_1 = ttk.Label(self.Frame_1)
        self.voltage_value_1 = ttk.Label(self.Frame_1)
        self.analog_scale_1 = ttk.Progressbar(self.Frame_1)
        self.java_label_1 = ttk.Label(self.Frame_1)
        self.java_value_1 = ttk.Label(self.Frame_1)
        self.analog_panel.config(height=200)
        self.analog_panel.config(padding=(5, 5, 5, 5))
        self.analog_panel.config(relief='ridge')
        self.analog_panel.config(width=200)
        self.analog_panel.grid(column=0)
        self.analog_panel.grid(row=0)
        self.analog_panel.grid(sticky=(N, S, E, W))
        self.analog_panel.grid_rowconfigure(0, weight=1)
        self.analog_panel.grid_rowconfigure(1, weight=1)
        self.analog_panel.grid_columnconfigure(0, weight=1)
        self.analog_label_1.config(text='Analog 0')
        self.analog_label_1.grid(column=0)
        self.analog_label_1.grid(padx=0)
        self.analog_label_1.grid(pady=0)
        self.analog_label_1.grid(row=0)
        self.analog_label_1.grid(sticky=W)
        self.Frame_1.config(height=200)
        self.Frame_1.config(width=200)
        self.Frame_1.grid(column=0)
        self.Frame_1.grid(pady=5)
        self.Frame_1.grid(row=1)
        self.Frame_1.grid(sticky=(N, S, E, W))
        self.Frame_1.grid_rowconfigure(0, weight=1)
        self.Frame_1.grid_rowconfigure(1, weight=1)
        self.Frame_1.grid_columnconfigure(0, weight=1)
        self.Frame_1.grid_columnconfigure(1, weight=1)
        self.Frame_1.grid_columnconfigure(2, weight=1)
        self.voltage_label_1.config(borderwidth=0)
        self.voltage_label_1.config(text='Voltage: ')
        self.voltage_label_1.grid(column=0)
        self.voltage_label_1.grid(row=1)
        self.voltage_label_1.grid(sticky=W)
        self.voltage_value_1.config(borderwidth=0)
        self.voltage_value_1.config(text='value')
        self.voltage_value_1.grid(column=1)
        self.voltage_value_1.grid(padx=5)
        self.voltage_value_1.grid(row=1)
        self.voltage_value_1.grid(sticky=W)
        self.analog_scale_1.config(length=100)
        self.analog_scale_1.config(maximum=3.3)
        self.analog_scale_1.config(orient='horizontal')
        self.analog_scale_1.config(value=0)
        self.analog_scale_1.grid(column=4)
        self.analog_scale_1.grid(row=1)
        self.analog_scale_1.grid(sticky=(E, W))
        self.java_label_1.config(borderwidth=0)
        self.java_label_1.config(text='Java: ')
        self.java_label_1.grid(column=2)
        self.java_label_1.grid(row=1)
        self.java_label_1.grid(sticky=W)
        self.java_value_1.config(borderwidth=0)
        self.java_value_1.config(text='value')
        self.java_value_1.grid(column=3)
        self.java_value_1.grid(padx=5)
        self.java_value_1.grid(row=1)
        self.java_value_1.grid(sticky=W)


class io_box():

    def __init__(self, root, analogAdd):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid(sticky=(N, S, E, W))
        self.io_pack = ttk.Frame(root)
        self.analog_pack = ttk.Labelframe(self.io_pack)
        self.digital_pack = ttk.Labelframe(self.io_pack)
        self.Button_1 = ttk.Button(self.analog_pack)
        self.innerFrame = ttk.Frame(self.analog_pack)
        self.innerFrame_1 = ttk.Frame(self.digital_pack)
        self.io_pack.config(height=200)
        self.io_pack.config(width=200)
        self.io_pack.grid(column=0)
        self.io_pack.grid(row=0)
        self.io_pack.grid(sticky=(N, S, E, W))
        self.io_pack.grid_rowconfigure(0, weight=1)
        self.io_pack.grid_rowconfigure(1, weight=1)
        self.io_pack.grid_columnconfigure(0, weight=1)
        self.analog_pack.config(height=200)
        self.analog_pack.config(text='Analog I/O')
        self.analog_pack.config(width=200)
        self.analog_pack.grid(column=0)
        self.analog_pack.grid(ipadx=5)
        self.analog_pack.grid(ipady=5)
        self.analog_pack.grid(row=0)
        self.analog_pack.grid(sticky=(N, S, E, W))
        self.analog_pack.grid_rowconfigure(0, weight=1)
        self.analog_pack.grid_rowconfigure(1, weight=0)
        self.analog_pack.grid_columnconfigure(0, weight=1)
        self.Button_1.config(command=analogAdd)
        self.Button_1.config(text='POLL')
        self.Button_1.grid(column=0)
        self.Button_1.grid(row=1)
        self.Button_1.grid(sticky=(E, W))
        self.innerFrame.config(height=200)
        self.innerFrame.config(width=200)
        self.innerFrame.grid(column=0)
        self.innerFrame.grid(row=0)
        self.innerFrame.grid(sticky=(N, S, E, W))
        self.digital_pack.config(height=200)
        self.digital_pack.config(text='Digital I/O')
        self.digital_pack.config(width=200)
        self.digital_pack.grid(column=0)
        self.digital_pack.grid(row=1)
        self.digital_pack.grid(sticky=(N, S, E, W))
        self.digital_pack.grid_rowconfigure(0, weight=1)
        self.digital_pack.grid_columnconfigure(0, weight=1)
        self.innerFrame_1.config(height=200)
        self.innerFrame_1.config(width=200)
        self.innerFrame_1.grid(column=0)
        self.innerFrame_1.grid(row=0)
        self.innerFrame_1.grid(sticky=(N, S, E, W))


class imu_box():

    def __init__(self, root, poll_imu_callback):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid(sticky=(N, S, E, W))
        self.i2c_pack = ttk.Labelframe(root)
        self.Label_2 = ttk.Label(self.i2c_pack)
        self.Euler_label = ttk.Label(self.i2c_pack)
        self.Accel_label = ttk.Label(self.i2c_pack)
        self.Euler_value = ttk.Label(self.i2c_pack)
        self.Accel_value = ttk.Label(self.i2c_pack)
        self.Poll_button = ttk.Button(self.i2c_pack)
        self.i2c_pack.config(height=200)
        self.i2c_pack.config(text='IMU')
        self.i2c_pack.config(width=200)
        self.i2c_pack.grid(column=0)
        self.i2c_pack.grid(padx=5)
        self.i2c_pack.grid(pady=5)
        self.i2c_pack.grid(row=0)
        self.i2c_pack.grid(sticky=(N, S, E, W))
        self.Label_2.config(text='IMU Sensor')
        self.Label_2.grid(column=0)
        self.Label_2.grid(padx=5)
        self.Label_2.grid(pady=5)
        self.Label_2.grid(row=0)
        self.Label_2.grid(sticky=(N, S, E, W))
        self.Euler_label.config(text='Heading, Roll, Pitch:')
        self.Euler_label.grid(column=0)
        self.Euler_label.grid(columnspan=2)
        self.Euler_label.grid(padx=5)
        self.Euler_label.grid(pady=5)
        self.Euler_label.grid(row=1)
        self.Euler_label.grid(sticky=W)
        self.Accel_label.config(text='Gravity (m/s^2):')
        self.Accel_label.grid(column=0)
        self.Accel_label.grid(columnspan=2)
        self.Accel_label.grid(padx=5)
        self.Accel_label.grid(pady=5)
        self.Accel_label.grid(row=2)
        self.Accel_label.grid(sticky=W)
        self.Euler_value.config(text='n/a')
        self.Euler_value.grid(column=2)
        self.Euler_value.grid(padx=5)
        self.Euler_value.grid(pady=5)
        self.Euler_value.grid(row=1)
        self.Euler_value.grid(sticky=W)
        self.Accel_value.config(text='n/a')
        self.Accel_value.grid(column=2)
        self.Accel_value.grid(padx=5)
        self.Accel_value.grid(pady=5)
        self.Accel_value.grid(row=2)
        self.Accel_value.grid(sticky=W)
        self.Poll_button.config(command=poll_imu_callback)
        self.Poll_button.config(text='POLL')
        self.Poll_button.config(width=5)
        self.Poll_button.grid(column=1)
        self.Poll_button.grid(padx=5)
        self.Poll_button.grid(pady=5)
        self.Poll_button.grid(row=0)


class i2c_chan():

    def __init__(self, root, add_col_callback, poll_col_callback):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.Frame_1 = ttk.Frame(root)
        self.i2c_pack = ttk.Labelframe(self.Frame_1)
        self.Frame_2 = ttk.Frame(self.i2c_pack)
        self.I2C_label = ttk.Label(self.Frame_2)
        self.Val_label = ttk.Label(self.Frame_2)
        self.I2C_value = ttk.Label(self.Frame_2)
        self.Config_button = ttk.Button(self.Frame_2)
        self.Poll_button = ttk.Button(self.Frame_2)
        self.Frame_1.config(height=200)
        self.Frame_1.config(width=200)
        self.Frame_1.grid(column=0)
        self.Frame_1.grid(row=0)
        self.Frame_1.grid(sticky=(N, S, E, W))
        self.Frame_1.grid_rowconfigure(0, weight=1)
        self.Frame_1.grid_columnconfigure(0, weight=1)
        self.i2c_pack.config(height=200)
        self.i2c_pack.config(padding=(1, 1, 1, 1))
        self.i2c_pack.config(text='test')
        self.i2c_pack.config(width=200)
        self.i2c_pack.grid(column=0)
        self.i2c_pack.grid(row=0)
        self.i2c_pack.grid(sticky=(N, S, E, W))
        self.i2c_pack.grid_rowconfigure(0, weight=1)
        self.i2c_pack.grid_columnconfigure(0, weight=1)
        self.Frame_2.config(borderwidth=2)
        self.Frame_2.config(height=200)
        self.Frame_2.config(relief='raised')
        self.Frame_2.config(width=100)
        self.Frame_2.grid(column=0)
        self.Frame_2.grid(row=0)
        self.Frame_2.grid(sticky=(N, S, E, W))
        self.Frame_2.grid_rowconfigure(0, weight=1)
        self.Frame_2.grid_rowconfigure(1, weight=1)
        self.Frame_2.grid_rowconfigure(2, weight=2)
        self.Frame_2.grid_rowconfigure(3, weight=1)
        self.Frame_2.grid_rowconfigure(4, weight=1)
        self.Frame_2.grid_rowconfigure(5, weight=1)
        self.Frame_2.grid_rowconfigure(6, weight=1)
        self.Frame_2.grid_columnconfigure(0, weight=1)
        self.Frame_2.grid_columnconfigure(1, weight=1)
        self.I2C_label.config(text='I2C Device (default: Color Sensor)')
        self.I2C_label.grid(column=0)
        self.I2C_label.grid(padx=5)
        self.I2C_label.grid(pady=5)
        self.I2C_label.grid(row=0)
        self.I2C_label.grid(sticky=(N, S, E, W))
        self.Val_label.config(text='Value (default: R,G,B,C,Prox)')
        self.Val_label.grid(column=0)
        self.Val_label.grid(padx=5)
        self.Val_label.grid(pady=5)
        self.Val_label.grid(row=3)
        self.Val_label.grid(sticky=W)
        self.I2C_value.config(text='n/a')
        self.I2C_value.config(width=12)
        self.I2C_value.grid(column=1)
        self.I2C_value.grid(columnspan=2)
        self.I2C_value.grid(padx=5)
        self.I2C_value.grid(pady=5)
        self.I2C_value.grid(row=3)
        self.I2C_value.grid(sticky=(E, W))
        self.Config_button.config(command=add_col_callback)
        self.Config_button.config(text='INIT')
        self.Config_button.config(width=6)
        self.Config_button.grid(column=1)
        self.Config_button.grid(padx=5)
        self.Config_button.grid(pady=5)
        self.Config_button.grid(row=0)
        self.Config_button.grid(sticky=(E, W))
        self.Poll_button.config(command=poll_col_callback)
        self.Poll_button.config(text='POLL')
        self.Poll_button.config(state=Tkinter.DISABLED)
        self.Poll_button.config(width=10)
        self.Poll_button.grid(column=2)
        self.Poll_button.grid(columnspan=1)
        self.Poll_button.grid(padx=5)
        self.Poll_button.grid(pady=5)
        self.Poll_button.grid(row=0)
        self.Poll_button.grid(sticky=(E, W))


class servo_motor():

    def __init__(self, root, slider_0_callback, java_0_callback, ms_0_callback, slider_1_callback, java_1_callback, ms_1_callback):
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.Frame_1 = ttk.Frame(root)
        self.servo_pack = ttk.Labelframe(self.Frame_1)
        self.servo_0 = ttk.Frame(self.servo_pack)
        self.servo_1 = ttk.Frame(self.servo_pack)
        self.Servo_num_0 = ttk.Label(self.servo_0)
        self.Java_label_0 = ttk.Label(self.servo_0)
        self.Speed_slider_0 = ttk.Scale(self.servo_0)
        self.Java_entry_0 = ttk.Entry(self.servo_0)
        self.Ms_entry_0 = ttk.Entry(self.servo_0)
        self.Ms_label_0 = ttk.Label(self.servo_0)
        self.Java_button_0 = ttk.Button(self.servo_0)
        self.Ms_button_0 = ttk.Button(self.servo_0)
        self.Servo_num_1 = ttk.Label(self.servo_1)
        self.Java_label_1 = ttk.Label(self.servo_1)
        self.Speed_slider_1 = ttk.Scale(self.servo_1)
        self.Java_entry_1 = ttk.Entry(self.servo_1)
        self.Ms_entry_1 = ttk.Entry(self.servo_1)
        self.Ms_label_1 = ttk.Label(self.servo_1)
        self.Java_button_1 = ttk.Button(self.servo_1)
        self.Ms_button_1 = ttk.Button(self.servo_1)
        self.Java_entry_0.bind('<Return>', self.update_java0)
        self.java_0_callback = java_0_callback
        self.Ms_entry_0.bind('<Return>', self.update_ms0)
        self.ms_0_callback = ms_0_callback
        self.Java_entry_1.bind('<Return>', self.update_java1)
        self.java_1_callback = java_1_callback
        self.Ms_entry_1.bind('<Return>', self.update_ms1)
        self.ms_1_callback = ms_1_callback
        self.Frame_1.config(borderwidth=5)
        self.Frame_1.config(height=200)
        self.Frame_1.config(width=200)
        self.Frame_1.grid(column=0)
        self.Frame_1.grid(row=0)
        self.Frame_1.grid(sticky=(N, S, E, W))
        self.Frame_1.grid_rowconfigure(0, weight=1)
        self.Frame_1.grid_columnconfigure(0, weight=1)
        self.servo_pack.config(height=200)
        self.servo_pack.config(padding=(1, 1, 1, 1))
        self.servo_pack.config(text='test')
        self.servo_pack.config(width=200)
        self.servo_pack.grid(column=0)
        self.servo_pack.grid(row=0)
        self.servo_pack.grid(sticky=(N, S, E, W))
        self.servo_pack.grid_rowconfigure(0, weight=1)
        self.servo_pack.grid_rowconfigure(1, weight=1)
        self.servo_pack.grid_columnconfigure(0, weight=1)
        self.servo_pack.grid_columnconfigure(1, weight=0)
        self.servo_0.config(borderwidth=2)
        self.servo_0.config(padding=(1, 1, 1, 1))
        self.servo_0.config(relief='raised')
        self.servo_0.grid(column=0)
        self.servo_0.grid(padx=1)
        self.servo_0.grid(pady=1)
        self.servo_0.grid(row=0)
        self.servo_0.grid(sticky=(N, S, E, W))
        self.servo_0.grid_rowconfigure(0, weight=1)
        self.servo_0.grid_rowconfigure(1, weight=1)
        self.servo_0.grid_columnconfigure(0, weight=1)
        self.servo_0.grid_columnconfigure(1, weight=1)
        self.servo_0.grid_columnconfigure(2, weight=1)
        self.servo_0.grid_columnconfigure(3, weight=1)
        self.Servo_num_0.config(justify='left')
        self.Servo_num_0.config(text='Servo 0')
        self.Servo_num_0.config(width=0)
        self.Servo_num_0.grid(column=0)
        self.Servo_num_0.grid(padx=5)
        self.Servo_num_0.grid(pady=5)
        self.Servo_num_0.grid(row=0)
        self.Servo_num_0.grid(sticky=(E, W))
        self.Java_label_0.config(text='Java (0,1)')
        self.Java_label_0.grid(column=2)
        self.Java_label_0.grid(padx=5)
        self.Java_label_0.grid(pady=5)
        self.Java_label_0.grid(row=1)
        self.Java_label_0.grid(sticky=(N, E, W))
        self.Speed_slider_0.config(command=slider_0_callback)
        self.Speed_slider_0.config(from_=500)
        self.Speed_slider_0.config(orient='horizontal')
        self.Speed_slider_0.config(to=2500)
        self.Speed_slider_0.config(value=1500)
        self.Speed_slider_0.grid(column=1)
        self.Speed_slider_0.grid(padx=5)
        self.Speed_slider_0.grid(pady=5)
        self.Speed_slider_0.grid(row=0)
        self.Speed_slider_0.grid(sticky=(E, W))
        self.Java_entry_0.config(width=10)
        self.Java_entry_0.grid(column=2)
        self.Java_entry_0.grid(padx=5)
        self.Java_entry_0.grid(pady=5)
        self.Java_entry_0.grid(row=0)
        self.Java_entry_0.grid(sticky=(N, S, E, W))
        self.Ms_entry_0.config(width=10)
        self.Ms_entry_0.grid(column=3)
        self.Ms_entry_0.grid(padx=5)
        self.Ms_entry_0.grid(pady=5)
        self.Ms_entry_0.grid(row=0)
        self.Ms_entry_0.grid(sticky=(N, S, E, W))
        self.Ms_label_0.config(text='MS (500,2500)')
        self.Ms_label_0.grid(column=3)
        self.Ms_label_0.grid(padx=5)
        self.Ms_label_0.grid(pady=5)
        self.Ms_label_0.grid(row=1)
        self.Ms_label_0.grid(sticky=(N, E, W))
        self.Java_button_0.config(command=java_0_callback)
        self.Java_button_0.config(text='set')
        self.Java_button_0.config(width=3)
        self.Java_button_0.grid(column=2)
        self.Java_button_0.grid(padx=5)
        self.Java_button_0.grid(pady=5)
        self.Java_button_0.grid(row=0)
        self.Java_button_0.grid(sticky=(N, S, E))
        self.Ms_button_0.config(command=ms_0_callback)
        self.Ms_button_0.config(text='set')
        self.Ms_button_0.config(width=3)
        self.Ms_button_0.grid(column=3)
        self.Ms_button_0.grid(padx=5)
        self.Ms_button_0.grid(pady=5)
        self.Ms_button_0.grid(row=0)
        self.Ms_button_0.grid(sticky=(N, S, E))
        self.servo_1.config(borderwidth=2)
        self.servo_1.config(padding=(1, 1, 1, 1))
        self.servo_1.config(relief='raised')
        self.servo_1.grid(column=0)
        self.servo_1.grid(padx=1)
        self.servo_1.grid(pady=1)
        self.servo_1.grid(row=1)
        self.servo_1.grid(sticky=(N, S, E, W))
        self.servo_1.grid_rowconfigure(0, weight=1)
        self.servo_1.grid_rowconfigure(1, weight=1)
        self.servo_1.grid_columnconfigure(0, weight=1)
        self.servo_1.grid_columnconfigure(1, weight=1)
        self.servo_1.grid_columnconfigure(2, weight=1)
        self.servo_1.grid_columnconfigure(3, weight=1)
        self.Servo_num_1.config(justify='left')
        self.Servo_num_1.config(text='Servo 1')
        self.Servo_num_1.config(width=0)
        self.Servo_num_1.grid(column=0)
        self.Servo_num_1.grid(padx=5)
        self.Servo_num_1.grid(pady=5)
        self.Servo_num_1.grid(row=0)
        self.Servo_num_1.grid(sticky=(E, W))
        self.Java_label_1.config(text='Java (0,1)')
        self.Java_label_1.grid(column=2)
        self.Java_label_1.grid(padx=5)
        self.Java_label_1.grid(pady=5)
        self.Java_label_1.grid(row=1)
        self.Java_label_1.grid(sticky=(N, E, W))
        self.Speed_slider_1.config(command=slider_1_callback)
        self.Speed_slider_1.config(from_=500)
        self.Speed_slider_1.config(orient='horizontal')
        self.Speed_slider_1.config(to=2500)
        self.Speed_slider_1.config(value=1500)
        self.Speed_slider_1.grid(column=1)
        self.Speed_slider_1.grid(padx=5)
        self.Speed_slider_1.grid(pady=5)
        self.Speed_slider_1.grid(row=0)
        self.Speed_slider_1.grid(sticky=(E, W))
        self.Java_entry_1.config(width=10)
        self.Java_entry_1.grid(column=2)
        self.Java_entry_1.grid(padx=5)
        self.Java_entry_1.grid(pady=5)
        self.Java_entry_1.grid(row=0)
        self.Java_entry_1.grid(sticky=(N, S, E, W))
        self.Ms_entry_1.config(width=10)
        self.Ms_entry_1.grid(column=3)
        self.Ms_entry_1.grid(padx=5)
        self.Ms_entry_1.grid(pady=5)
        self.Ms_entry_1.grid(row=0)
        self.Ms_entry_1.grid(sticky=(N, S, E, W))
        self.Ms_label_1.config(text='MS (500,2500)')
        self.Ms_label_1.grid(column=3)
        self.Ms_label_1.grid(padx=5)
        self.Ms_label_1.grid(pady=5)
        self.Ms_label_1.grid(row=1)
        self.Ms_label_1.grid(sticky=(N, E, W))
        self.Java_button_1.config(command=java_1_callback)
        self.Java_button_1.config(text='set')
        self.Java_button_1.config(width=3)
        self.Java_button_1.grid(column=2)
        self.Java_button_1.grid(padx=5)
        self.Java_button_1.grid(pady=5)
        self.Java_button_1.grid(row=0)
        self.Java_button_1.grid(sticky=(N, S, E))
        self.Ms_button_1.config(command=ms_1_callback)
        self.Ms_button_1.config(text='set')
        self.Ms_button_1.config(width=3)
        self.Ms_button_1.grid(column=3)
        self.Ms_button_1.grid(padx=5)
        self.Ms_button_1.grid(pady=5)
        self.Ms_button_1.grid(row=0)
        self.Ms_button_1.grid(sticky=(N, S, E))

    def update_java0(self, event):
        self.java_0_callback()

    def update_java1(self, event):
        self.java_1_callback()

    def update_ms0(self, event):
        self.ms_0_callback()

    def update_ms1(self, event):
        self.ms_1_callback()


class dc_motor():

    def __init__(self, root, speed_slider_callback, speed_button_callback, java_button_callback):
        self.root = root
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.Frame_5 = ttk.Frame(root)
        self.Motor_pack = ttk.Labelframe(self.Frame_5)
        self.ZeroButton = tk.Button(self.Motor_pack)
        self.Speed_slider = ttk.Scale(self.Motor_pack)
        self.Motor_values = ttk.Label(self.Motor_pack)
        self.Java_label = ttk.Label(self.Motor_pack)
        self.Speed_button = tk.Button(self.Motor_pack)
        self.Java_entry = tk.Entry(self.Motor_pack)
        self.Java_button = tk.Button(self.Motor_pack)
        self.Controls_label = ttk.Label(self.Motor_pack)
        self.Java_entry.bind('<Return>', self.update_java)
        self.java_button_callback = java_button_callback
        self.Frame_5.config(height=200)
        self.Frame_5.config(width=200)
        self.Frame_5.grid(column=0)
        self.Frame_5.grid(row=0)
        self.Frame_5.grid(sticky=(N, S, E, W))
        self.Frame_5.grid_rowconfigure(0, weight=1)
        self.Frame_5.grid_columnconfigure(0, weight=1)
        self.Motor_pack.config(height=200)
        self.Motor_pack.config(padding=(5, 5, 5, 5))
        self.Motor_pack.config(text='motornum')
        self.Motor_pack.config(width=200)
        self.Motor_pack.grid(column=0)
        self.Motor_pack.grid(padx=5)
        self.Motor_pack.grid(pady=5)
        self.Motor_pack.grid(row=0)
        self.Motor_pack.grid(sticky=(N, S, E, W))
        self.Motor_pack.grid_rowconfigure(0, weight=1)
        self.Motor_pack.grid_rowconfigure(1, weight=1)
        self.Motor_pack.grid_rowconfigure(2, weight=1)
        self.Motor_pack.grid_columnconfigure(0, weight=1)
        self.Motor_pack.grid_columnconfigure(1, weight=1)
        self.Motor_pack.grid_columnconfigure(2, weight=2)
        self.Motor_pack.grid_columnconfigure(3, weight=2)
        self.Speed_slider.config(command=speed_slider_callback)
        self.Speed_slider.config(from_=-32000)
        self.Speed_slider.config(orient='horizontal')
        self.Speed_slider.config(to=32000)
        self.Speed_slider.grid(column=1)
        self.Speed_slider.grid(padx=5)
        self.Speed_slider.grid(pady=5)
        self.Speed_slider.grid(row=0)
        self.Speed_slider.grid(sticky=(E, W))
        self.Motor_values.config(justify='left')
        self.Motor_values.config(text='Current (mA): %3d\n\nEncoder: %3d' % (0, 0))
        self.Motor_values.grid(column=0)
        self.Motor_values.grid(padx=5)
        self.Motor_values.grid(pady=5)
        self.Motor_values.grid(row=1)
        self.Motor_values.grid(sticky=(E, W))
        self.Java_label.config(text='Speed (-1,1)')
        self.Java_label.grid(column=3)
        self.Java_label.grid(padx=5)
        self.Java_label.grid(pady=5)
        self.Java_label.grid(row=1)
        self.Java_label.grid(sticky=(E, W))
        self.Speed_button.config(command=speed_button_callback)
        self.Speed_button.config(text='Zero')
        self.Speed_button.grid(column=2)
        self.Speed_button.grid(padx=5)
        self.Speed_button.grid(pady=5)
        self.Speed_button.grid(row=0)
        self.Speed_button.grid(sticky=E)
        self.Java_entry.config(width=10)
        self.Java_entry.grid(column=3)
        self.Java_entry.grid(padx=5)
        self.Java_entry.grid(pady=5)
        self.Java_entry.grid(row=0)
        self.Java_entry.grid(sticky=(N, S, E, W))
        self.Java_button.config(command=java_button_callback)
        self.Java_button.config(text='set')
        self.Java_button.grid(column=3)
        self.Java_button.grid(padx=5)
        self.Java_button.grid(pady=5)
        self.Java_button.grid(row=0)
        self.Java_button.grid(sticky=E)
        self.Controls_label.config(text='Controls:')
        self.Controls_label.grid(column=0)
        self.Controls_label.grid(padx=5)
        self.Controls_label.grid(pady=5)
        self.Controls_label.grid(row=0)
        self.Controls_label.grid(sticky=(E, W))

    def update_java(self, event):
        self.java_button_callback()


class Application():

    def __init__(self, root):
        self.root = root
        self.REVModules = []
        self.commMod = REVcomm()
        self.repetitiveFunctions = []
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        true = True
        self.Main_window = ttk.Frame(root)
        self.Tab_frame = ttk.Notebook(self.Main_window)
        self.Connected_Label = ttk.Label(self.Main_window)
        try:
            self.Top_Banner_Image = tk.PhotoImage(file='resource/banner.gif')
            self.Top_Banner = Label(self.Main_window, image=self.Top_Banner_Image)
        except:
            self.Top_Banner = Label(self.Main_window)

        self.Connect_button = ttk.Button(self.Main_window)
        self.Quit_button = ttk.Button(self.Main_window)
        self.DC_Motor = ttk.Frame(self.Tab_frame)
        self.Servo_Motor = ttk.Frame(self.Tab_frame)
        self.I2C_Device = ttk.Frame(self.Tab_frame)
        self.Firmware_Update = ttk.Frame(self.Tab_frame)
        self.IO = ttk.Frame(self.Tab_frame)
        self.DC_Motor_frame = ttk.Frame(self.DC_Motor)
        self.Servo_Motor_frame = ttk.Frame(self.Servo_Motor)
        self.I2C_Device_frame = ttk.Frame(self.I2C_Device)
        self.Firmware_tab = ttk.Frame(self.Firmware_Update)
        self.IO_tab = ttk.Frame(self.IO)
        self.Main_window.config(height=600)
        self.Main_window.config(width=900)
        self.Main_window.grid(column=0)
        self.Main_window.grid(row=0)
        self.Main_window.grid(sticky=(N, S, E, W))
        self.Main_window.grid_rowconfigure(0, minsize=0)
        self.Main_window.grid_rowconfigure(0, weight=1)
        self.Main_window.grid_rowconfigure(1, minsize=600)
        self.Main_window.grid_rowconfigure(1, weight=1)
        self.Main_window.grid_columnconfigure(0, minsize=350)
        self.Main_window.grid_columnconfigure(0, weight=1)
        self.Main_window.grid_columnconfigure(1, minsize=80)
        self.Main_window.grid_columnconfigure(1, weight=0)
        self.Main_window.grid_columnconfigure(2, minsize=20)
        self.Main_window.grid_columnconfigure(2, weight=0)
        self.Main_window.grid_columnconfigure(3, minsize=0)
        self.Main_window.grid_columnconfigure(3, weight=0)
        self.Tab_frame.config(height=240)
        self.Tab_frame.config(padding=(0, 2, 0, 0))
        self.Tab_frame.config(width=320)
        self.Tab_frame.grid(column=0)
        self.Tab_frame.grid(columnspan=3)
        self.Tab_frame.grid(padx=5)
        self.Tab_frame.grid(pady=5)
        self.Tab_frame.grid(row=1)
        self.Tab_frame.grid(sticky=(N, S, E, W))
        self.Connected_Label.grid(row=0)
        self.Connected_Label.grid(sticky=E)
        self.Connected_Label.config(text='Disconnected')
        self.Top_Banner.grid(row=0)
        self.Top_Banner.grid(sticky=W)
        self.DC_Motor_frame.config(height=250)
        self.DC_Motor_frame.config(width=200)
        self.DC_Motor_frame.grid(column=0)
        self.DC_Motor_frame.grid(row=0)
        self.DC_Motor_frame.grid(sticky=(N, S, E, W))
        self.DC_Motor_frame.grid_rowconfigure(0, weight=1)
        self.DC_Motor_frame.grid_columnconfigure(0, minsize=0)
        self.DC_Motor_frame.grid_columnconfigure(0, weight=1)
        self.DC_Motor_frame.grid(column=0)
        self.DC_Motor_frame.grid(row=0)
        self.DC_Motor_frame.grid(sticky=(N, S, E, W))
        self.Servo_Motor_frame.config(height=200)
        self.Servo_Motor_frame.config(width=200)
        self.Servo_Motor_frame.grid(column=0)
        self.Servo_Motor_frame.grid(row=0)
        self.Servo_Motor_frame.grid(sticky=(N, S, E, W))
        self.Servo_Motor_frame.grid_rowconfigure(0, weight=1)
        self.Servo_Motor_frame.grid_columnconfigure(0, weight=1)
        self.I2C_Device_frame.config(height=200)
        self.I2C_Device_frame.config(width=200)
        self.I2C_Device_frame.grid(column=0)
        self.I2C_Device_frame.grid(row=0)
        self.I2C_Device_frame.grid(sticky=(N, S, E, W))
        self.I2C_Device_frame.grid_rowconfigure(0, weight=1)
        self.I2C_Device_frame.grid_columnconfigure(0, weight=1)
        self.Firmware_tab.config(height=200)
        self.Firmware_tab.config(padding=(2, 6, 2, 6))
        self.Firmware_tab.config(width=200)
        self.Firmware_tab.grid(column=0)
        self.Firmware_tab.grid(row=0)
        self.Firmware_tab.grid(sticky=(N, S, E, W))
        self.Firmware_tab.grid_rowconfigure(0, weight=1)
        self.Firmware_tab.grid_columnconfigure(0, weight=1)
        self.IO_tab.config(height=200)
        self.IO_tab.config(padding=(2, 6, 2, 6))
        self.IO_tab.config(width=200)
        self.IO_tab.grid(column=0)
        self.IO_tab.grid(row=0)
        self.IO_tab.grid(sticky=(N, S, E, W))
        self.IO_tab.grid_rowconfigure(0, weight=1)
        self.IO_tab.grid_columnconfigure(0, weight=1)
        self.Connect_button.config(command=self.on_connect_button_callback)
        self.Connect_button.config(text='CONNECT')
        self.Connect_button.config(width=10)
        self.Connect_button.grid(column=1)
        self.Connect_button.grid(ipadx=0)
        self.Connect_button.grid(ipady=0)
        self.Connect_button.grid(padx=5)
        self.Connect_button.grid(pady=5)
        self.Connect_button.grid(row=0)
        self.Connect_button.grid(sticky=(N, S, E, W))
        self.Quit_button.config(command=self.on_quit_button_callback)
        self.Quit_button.config(text='E-STOP')
        self.Quit_button.config(width=7)
        self.Quit_button.grid(column=2)
        self.Quit_button.grid(padx=5)
        self.Quit_button.grid(pady=5)
        self.Quit_button.grid(row=0)
        self.Quit_button.grid(sticky=(N, S, E, W))
        self.Tab_frame.add(self.DC_Motor, padding=(2, 6, 2, 6), text='DC Motors')
        self.DC_Motor.grid_columnconfigure(0, weight=1)
        self.DC_Motor.grid_rowconfigure(0, weight=1)
        self.Tab_frame.add(self.Servo_Motor, padding=(2, 6, 2, 6), text='Servo Motors')
        self.Servo_Motor.grid_columnconfigure(0, weight=1)
        self.Servo_Motor.grid_rowconfigure(0, weight=1)
        self.Tab_frame.add(self.I2C_Device, padding=(2, 6, 2, 6), text='I2C Devices')
        self.I2C_Device.grid_columnconfigure(0, weight=1)
        self.I2C_Device.grid_rowconfigure(0, weight=1)
        self.Tab_frame.add(self.IO, text='GPIO Control')
        self.IO.grid_columnconfigure(0, weight=1)
        self.IO.grid_rowconfigure(0, weight=1)
        self.Tab_frame.add(self.Firmware_Update, text='Firmware')
        self.Firmware_Update.grid_columnconfigure(0, weight=1)
        self.Firmware_Update.grid_rowconfigure(0, weight=1)
        self.buildFirmwareFrame()

    def send_all_KA(self):
        for module in self.REVModules:
            isAlive = module.sendKA()
            if isAlive == False:
                self.on_quit_button_callback()
                self.Connected_Label.config(text='Disconnected')
            else:
                self.Connected_Label.config(text='Connected')
                module.getStatus()

    def speedMotorSlider(self, speed, moduleNumber, motorNumber, *args):
        self.Motor_packs[moduleNumber * 4 + motorNumber].Java_entry.delete(0, END)
        self.Motor_packs[moduleNumber * 4 + motorNumber].Java_entry.insert(0, '%.2f' % (float(speed) / 32000))
        self.REVModules[moduleNumber].motors[motorNumber].setPower(float(speed))
        self.REVModules[moduleNumber].motors[motorNumber].enable()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        self.repetitiveFunctions.append((lambda : self.updateMotorLabels(motorNumber, moduleNumber)))
        return True

    def speedMotorEntry(self, motorNumber, moduleNumber, *args):
        speed = 0
        self.Motor_packs[moduleNumber * 4 + motorNumber].Speed_slider.set(speed)
        self.Motor_packs[moduleNumber * 4 + motorNumber].Java_entry.delete(0, END)
        self.Motor_packs[moduleNumber * 4 + motorNumber].Java_entry.insert(0, '%.2f' % float(speed / 32000))
        self.REVModules[moduleNumber].motors[motorNumber].setPower(float(speed))
        self.REVModules[moduleNumber].motors[motorNumber].enable()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        self.repetitiveFunctions.append((lambda : self.updateMotorLabels(motorNumber, moduleNumber)))
        return True

    def javaMotorEntry(self, motorNumber, moduleNumber, *args):
        try:
            speed = float(self.Motor_packs[moduleNumber * 4 + motorNumber].Java_entry.get())
        except ValueError:
            print 'Invalid speed entered: ' + self.Motor_packs[moduleNumber * 4 + motorNumber].Java_entry.get()
            return False

        self.Motor_packs[moduleNumber * 4 + motorNumber].Speed_slider.set(speed * 32000)
        self.Motor_packs[moduleNumber * 4 + motorNumber].Speed_entry.delete(0, END)
        self.Motor_packs[moduleNumber * 4 + motorNumber].Speed_entry.insert(0, '%.2f' % float(speed * 32000))
        self.REVModules[moduleNumber].motors[motorNumber].setPower(float(speed * 32000))
        self.REVModules[moduleNumber].motors[motorNumber].enable()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        self.repetitiveFunctions.append((lambda : self.updateMotorLabels(motorNumber, moduleNumber)))
        return True

    def updateMotorLabels(self, motorNumber, moduleNumber):
        current = self.REVModules[int(moduleNumber)].motors[motorNumber].getCurrent()
        position = self.REVModules[int(moduleNumber)].motors[motorNumber].getPosition()
        self.Motor_packs[moduleNumber * 4 + motorNumber].Motor_values.config(text='Current (mA): %3d\n\nEncoder: %3d' % (current, position))

    def servoSlider(self, pulse, moduleNumber, servoNumber, *args):
        if servoNumber % 2 == 0:
            pulse = float(pulse)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_0.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_0.insert(0, '%.2f' % float((pulse - 500) / 2000))
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_0.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_0.insert(0, '%.2f' % float(pulse))
        else:
            pulse = float(pulse)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_1.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_1.insert(0, '%.2f' % float((pulse - 500) / 2000))
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_1.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_1.insert(0, '%.2f' % float(pulse))
        self.REVModules[int(moduleNumber)].servos[servoNumber].setPulseWidth(pulse)
        self.REVModules[int(moduleNumber)].servos[servoNumber].enable()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        return True

    def servoJava(self, servoNumber, moduleNumber, *args):
        pulse = 0
        if servoNumber % 2 == 0:
            try:
                pulse = float(self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_0.get())
            except ValueError:
                print 'Invalid value entered: ' + self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_0.get()
                return False

            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_0.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_0.insert(0, '%.2f' % float(pulse * 2000 + 500))
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Speed_slider_0.set(pulse * 2000 + 500)
        else:
            try:
                pulse = float(self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_1.get())
            except ValueError:
                print 'Invalid value entered: ' + self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_1.get()
                return False

            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_1.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_1.insert(0, '%.2f' % float(pulse * 2000 + 500))
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Speed_slider_1.set(pulse * 2000 + 500)
        self.REVModules[int(moduleNumber)].servos[servoNumber].setPulseWidth(pulse * 2000 + 500)
        self.REVModules[int(moduleNumber)].servos[servoNumber].enable()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        return True

    def servoMS(self, servoNumber, moduleNumber, *args):
        pulse = 0
        if servoNumber % 2 == 0:
            try:
                pulse = float(self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_0.get())
            except ValueError:
                print 'Invalid value entered: ' + self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_0.get()
                return False

            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_0.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_0.insert(0, '%.2f' % float((pulse - 500) / 2000))
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Speed_slider_0.set(pulse)
        else:
            try:
                pulse = float(self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_1.get())
            except ValueError:
                print 'Invalid value entered: ' + self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Ms_entry_1.get()
                return False

            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_1.delete(0, END)
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Java_entry_1.insert(0, '%.2f' % float((pulse - 500) / 2000))
            self.Servo_packs[moduleNumber * 3 + int(servoNumber / 2)].Speed_slider_1.set(pulse)
        self.REVModules[int(moduleNumber)].servos[servoNumber].setPulseWidth(float(pulse))
        self.REVModules[int(moduleNumber)].servos[servoNumber].enable()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        return True

    def colorSenseAdd(self, module_number, bus_number):
        self.I2C_packs[module_number * 4 + bus_number].Config_button.config(text='Wait')
        self.root.update_idletasks()
        is2mSensor = False
        try:
            sensor = REV2mSensor(self.commMod, bus_number, self.REVModules[module_number].getModuleAddress())
            is2mSensor = sensor.Is2mDistanceSensor()
        except:
            pass

        isInitialized = False
        if is2mSensor:
            self.I2C_packs[module_number * 4 + bus_number].I2C_label.config(text='2m Distance Sensor                     ')
            self.I2C_packs[module_number * 4 + bus_number].Val_label.config(text='Value (Distance mm)    ')
            self.REVModules[module_number].i2cChannels[bus_number].addI2CDevice(str(module_number) + 'COL' + str(bus_number), sensor)
            if self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].initialize():
                self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text='REV 2m Distance Sensor Found')
                isInitialized = True
        else:
            cs = REVColorSensorV3(self.commMod, bus_number, self.REVModules[module_number].getModuleAddress())
            if cs.initSensor():
                self.I2C_packs[module_number * 4 + bus_number].I2C_label.config(text='Color Sensor V3                        ')
                self.REVModules[module_number].i2cChannels[bus_number].addI2CDevice(str(module_number) + 'COL' + str(bus_number), cs)
                isInitialized = True
                self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text='Color Sensor V3 Found')
            else:
                self.REVModules[module_number].i2cChannels[bus_number].addColorSensor(str(module_number) + 'COL' + str(bus_number))
                if self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].initSensor():
                    self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text='Color Sensor V2 Found')
                    isInitialized = True
                self.I2C_packs[module_number * 4 + bus_number].I2C_label.config(text='I2C Device (default: Color Sensor)')
            self.I2C_packs[module_number * 4 + bus_number].Val_label.config(text='Value (default: R,G,B,C,Prox)')
        self.I2C_packs[module_number * 4 + bus_number].Config_button.config(text='INIT')
        if isInitialized:
            self.I2C_packs[module_number * 4 + bus_number].Poll_button.config(state=Tkinter.NORMAL)
        else:
            self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text='Device did not initialize')

    def colorSensePoll(self, module_number, bus_number):
        sensorType = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getType()
        self.repetitiveFunctions = [(lambda : self.send_all_KA())]
        if sensorType == 'REV2mSensor':
            self.repetitiveFunctions.append((lambda : self.update2mSensor(module_number, bus_number)))
        elif sensorType == 'REVColorSensorV3':
            self.repetitiveFunctions.append((lambda : self.updateColorDeviceV3(module_number, bus_number)))
        else:
            self.repetitiveFunctions.append((lambda : self.updateColorDevice(module_number, bus_number)))

    def update2mSensor(self, module_number, bus_number):
        distance_mm = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].readRangeContinuousMillimeters()
        colorString = str(distance_mm) + 'mm'
        self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text=colorString)
        self.I2C_packs[module_number * 4 + bus_number].Val_label.config(text='Value (Distance mm)')

    def updateColorDevice(self, module_number, bus_number):
        red = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getRedValue()
        green = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getGreenValue()
        blue = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getBlueValue()
        clear = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getClearValue()
        prox = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getProxValue()
        colorString = str(red) + ', ' + str(green) + ', ' + str(blue) + ', ' + str(clear) + ', ' + str(prox)
        self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text=colorString)
        if len(colorString) > 28:
            self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(font=('TkDefaultFont',
                                                                                  8))
        else:
            self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(font=('TkDefaultFont',
                                                                                  10))

    def updateColorDeviceV3(self, module_number, bus_number):
        red, green, blue, ir, prox = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'COL' + str(bus_number)].getAll()
        clear = red + green + blue - 2 * ir
        colorString = str(red) + ', ' + str(green) + ', ' + str(blue) + ', ' + str(clear) + ', ' + str(prox)
        self.I2C_packs[module_number * 4 + bus_number].I2C_value.config(text=colorString)

    def imuAdd(self, module_number):
        self.REVModules[module_number].i2cChannels[0].addIMU(str(module_number) + 'IMU')
        self.REVModules[module_number].i2cChannels[0].getDevices()[str(module_number) + 'IMU'].initSensor()
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        self.repetitiveFunctions.append((lambda : self.updateImuDevice(module_number, 0)))

    def updateImuDevice(self, module_number, bus_number):
        heading, roll, pitch = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'IMU'].getAllEuler()
        gx, gy, gz = self.REVModules[module_number].i2cChannels[bus_number].getDevices()[str(module_number) + 'IMU'].getGravity()
        eulerString = '%2.3f, %2.3f, %2.3f' % (heading, roll, -pitch)
        linaccString = 'X: %2.3f, Y: %2.3f, Z: %2.3f' % (gx, gy, gz)
        self.IMUs[module_number].Euler_value.config(text=eulerString)
        self.IMUs[module_number].Accel_value.config(text=linaccString)

    def analogAdd(self, module_number):
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        self.repetitiveFunctions.append((lambda : self.analogUpdate(module_number)))

    def analogUpdate(self, module_number):
        for i in range(0, 4):
            adc_data = self.REVModules[module_number].adcPins[i].getADC(0)
            self.Analog_panels[module_number * 4 + i].voltage_value_1.config(text=str(float(adc_data) / 1000.0) + ' volts')
            self.Analog_panels[module_number * 4 + i].java_value_1.config(text=str(float(adc_data) / 1000.0))
            self.Analog_panels[module_number * 4 + i].analog_scale_1.config(value=float(adc_data) / 1000.0)

    def digitalSetAsOutput(self, module_number, dio_number):
        self.repetitiveFunctions = [(lambda : self.send_all_KA())]
        self.REVModules[module_number].dioPins[module_number * 2 + dio_number].setAsOutput()
        self.Digital_panels[module_number * 8 + dio_number].output_button.config(background='#aaccff')
        self.Digital_panels[module_number * 8 + dio_number].input_button.config(background='#ffffff')
        self.Digital_panels[module_number * 8 + dio_number].poll_button.config(state='disabled')
        self.Digital_panels[module_number * 8 + dio_number].Checkbutton_1.config(state='normal')
        self.Digital_panels[module_number * 8 + dio_number].var2.set(1)

    def digitalSetAsInput(self, module_number, dio_number):
        self.REVModules[module_number].dioPins[module_number * 2 + dio_number].setAsInput()
        self.Digital_panels[module_number * 8 + dio_number].input_button.config(background='#aaccff')
        self.Digital_panels[module_number * 8 + dio_number].output_button.config(background='#ffffff')
        self.Digital_panels[module_number * 8 + dio_number].poll_button.config(state='normal')
        self.Digital_panels[module_number * 8 + dio_number].Checkbutton_1.config(state='disabled')

    def digitalSetCallback(self, module_number, dio_number):
        self.REVModules[module_number].dioPins[module_number * 2 + dio_number].setOutput(int(self.Digital_panels[module_number * 8 + dio_number].var2.get()))

    def digitalAdd(self, module_number, dio_number):
        self.repetitiveFunctions = [
         (lambda : self.send_all_KA())]
        self.repetitiveFunctions.append((lambda : self.digitalUpdate(module_number, dio_number)))

    def digitalUpdate(self, module_number, dio_number):
        value = self.REVModules[module_number].dioPins[dio_number].getInput()
        if not int(value):
            self.Digital_panels[module_number * 8 + dio_number].var2.set(0)
        else:
            self.Digital_panels[module_number * 8 + dio_number].var2.set(1)

    def checkForModules(self):
        self.REVModules = []
        self.REVModules = self.commMod.discovery()
        self.repetitiveFunctions.append((lambda : self.send_all_KA()))
        self.moduleNames = []
        for i in range(0, len(self.REVModules)):
            self.moduleNames.append('REV Expansion Hub ' + str(i))

        return self.moduleNames

    def set_address_callback(self, moduleNumber):
        addr = int(self.devce_info[moduleNumber].addr_entry.get())
        if addr < 1 or addr > 255:
            return
        self.REVModules[moduleNumber].setAddress(addr)
        for i in range(0, len(self.REVModules)):
            self.devce_info[i].addr_entry.delete(0, END)
            self.devce_info[i].addr_entry.insert(0, str(self.REVModules[i].getModuleAddress()))

    def on_connect_button_callback(self):
        self.commMod.openActivePort()
        moduleTot = len(self.checkForModules())
        self.Quit_button.config(state='enabled')
        for tab in self.Tab_frame.tabs():
            self.Tab_frame.tab(tab, state='normal')

        self.Motor_packs = []
        for moduleNumber in range(0, moduleTot):
            for motorNumber in range(0, 4):
                self.DC_Motor_frame.grid_rowconfigure(motorNumber, weight=1)
                self.DC_Motor_frame.grid_columnconfigure(moduleNumber, weight=1)
                frame = ttk.Frame(self.DC_Motor_frame, borderwidth=5, relief='sunken')
                frame.grid(row=motorNumber, column=moduleNumber, sticky=(N, S, E, W))
                self.Motor_packs.append(dc_motor(frame, partial(self.speedMotorSlider, motorNumber=motorNumber, moduleNumber=moduleNumber), partial(self.speedMotorEntry, motorNumber=motorNumber, moduleNumber=moduleNumber), partial(self.javaMotorEntry, motorNumber=motorNumber, moduleNumber=moduleNumber)))
                self.Motor_packs[-1].Motor_pack.config(text='Module: ' + str(moduleNumber) + ' Motors: ' + str(motorNumber))

        self.Servo_packs = []
        for moduleNumber in range(0, moduleTot):
            for motorNumber in range(0, 3):
                self.Servo_Motor_frame.grid_rowconfigure(motorNumber, weight=1)
                self.Servo_Motor_frame.grid_columnconfigure(moduleNumber, weight=1)
                frame = ttk.Frame(self.Servo_Motor_frame, borderwidth=5, relief='sunken')
                frame.grid(row=motorNumber, column=moduleNumber, sticky=(N, S, E, W))
                self.Servo_packs.append(servo_motor(frame, partial(self.servoSlider, servoNumber=2 * motorNumber, moduleNumber=moduleNumber), partial(self.servoJava, servoNumber=motorNumber * 2, moduleNumber=moduleNumber), partial(self.servoMS, servoNumber=motorNumber * 2, moduleNumber=moduleNumber), partial(self.servoSlider, servoNumber=motorNumber * 2 + 1, moduleNumber=moduleNumber), partial(self.servoJava, servoNumber=motorNumber * 2 + 1, moduleNumber=moduleNumber), partial(self.servoMS, servoNumber=motorNumber * 2 + 1, moduleNumber=moduleNumber)))
                self.Servo_packs[-1].servo_pack.config(text='Module: ' + str(moduleNumber) + ' Motors: ' + str(motorNumber * 2) + ' & ' + str(motorNumber * 2 + 1))

        self.I2C_packs = []
        self.IMUs = []
        for moduleNumber in range(0, moduleTot):
            self.I2C_Device_frame.grid_rowconfigure(0, weight=1)
            self.I2C_Device_frame.grid_columnconfigure(moduleNumber, weight=1)
            frame = ttk.Frame(self.I2C_Device_frame, borderwidth=5, relief='sunken')
            frame.grid(row=0, column=moduleNumber, sticky=W)
            self.IMUs.append(imu_box(frame, partial(self.imuAdd, moduleNumber)))
            for i2cNumber in range(0, 4):
                self.I2C_Device_frame.grid_rowconfigure(i2cNumber, weight=1)
                self.I2C_Device_frame.grid_columnconfigure(moduleNumber, weight=1)
                frame = ttk.Frame(self.I2C_Device_frame, borderwidth=5, relief='sunken')
                frame.grid(row=i2cNumber + 1, column=moduleNumber, sticky=(N, S, E, W))
                self.I2C_packs.append(i2c_chan(frame, partial(self.colorSenseAdd, bus_number=i2cNumber, module_number=moduleNumber), partial(self.colorSensePoll, bus_number=i2cNumber, module_number=moduleNumber)))
                self.I2C_packs[-1].i2c_pack.config(text='Module: ' + str(moduleNumber) + ' I2C Bus: ' + str(i2cNumber))

        self.IO_packs = []
        self.Digital_panels = []
        self.Analog_panels = []
        for moduleNumber in range(0, moduleTot):
            self.IO_tab.grid_columnconfigure(moduleNumber, weight=1)
            frame = ttk.Frame(self.IO_tab, borderwidth=5, relief='sunken')
            frame.grid(row=0, column=moduleNumber, sticky=(N, S, E, W))
            self.IO_packs.append(io_box(frame, partial(self.analogAdd, moduleNumber)))
            self.IO_packs[-1].analog_pack.config(text='Analog Inputs Module: ' + str(moduleNumber))
            self.IO_packs[-1].digital_pack.config(text='Digital Input/Outputs Module: ' + str(moduleNumber))
            self.IO_packs[-1].innerFrame.grid_columnconfigure(0, weight=1)
            for i in range(0, 4):
                frame = ttk.Frame(self.IO_packs[-1].innerFrame, borderwidth=5, relief='sunken')
                frame.grid(row=i, column=0, sticky=(N, S, E, W))
                self.IO_packs[-1].innerFrame.grid_rowconfigure(i, weight=1)
                self.Analog_panels.append(analog_single(frame))
                self.Analog_panels[-1].analog_label_1.config(text=str('Analog ' + str(i)))

            for i in range(0, 4):
                for j in range(0, 2):
                    frame = ttk.Frame(self.IO_packs[-1].innerFrame_1, borderwidth=5, relief='sunken')
                    frame.grid(row=i, column=j, sticky=(N, S, E, W))
                    self.IO_packs[-1].innerFrame_1.grid_rowconfigure(i, weight=1)
                    self.IO_packs[-1].innerFrame_1.grid_columnconfigure(j, weight=1)
                    self.Digital_panels.append(digital_single(frame, partial(self.digitalSetAsInput, moduleNumber, i * 2 + j), partial(self.digitalSetAsOutput, moduleNumber, i * 2 + j), partial(self.digitalSetCallback, moduleNumber, i * 2 + j), partial(self.digitalAdd, moduleNumber, i * 2 + j)))
                    self.Digital_panels[-1].digital_label_1.config(text=str(i * 2 + j))

        self.devce_info = []
        for moduleNumber in range(0, moduleTot):
            frame = ttk.Frame(self.firmware.Device_info_frame1, borderwidth=5, relief='sunken')
            frame.grid(row=1, column=moduleNumber, sticky=(N, S, E, W))
            self.devce_info.append(device_info(frame, partial(self.set_address_callback, moduleNumber=moduleNumber)))
            self.devce_info[-1].addr_entry.delete(0, END)
            self.devce_info[-1].addr_entry.insert(0, str(self.REVModules[moduleNumber].getModuleAddress()))
            self.devce_info[-1].device_label.config(text='Module: ' + str(moduleNumber))

        self.firmware.firmware_label.config(text='Interface Version: ' + self.firmware.INTERFACE_VERSION + '\nFirmware Version: ' + self.REVModules[0].getVersionString())
        self.root.after(500, self.every_second)

    def buildFirmwareFrame(self):
        frame = ttk.Frame(self.Firmware_tab, borderwidth=5, relief='sunken')
        frame.grid(row=0, column=0, sticky=(N, S, E, W))
        self.firmware = firmware_tab(frame, partial(self.firmware_bin_select), partial(self.firmware_flash))
        self.firmware.warning_block.insert(END, 'Firmware update to be performed to the Expansion Hub connected via USB only. \n\t\t\nFirmware update is to be performed with only REV qualified .bin files located in the default installation directory\n\t\t\n\nWARNING: incorrect firmware can brick the device.\n\nModified firmware files are not FTC legal.\n')
        self.firmware.warning_block.config(state='disabled')

    def on_quit_button_callback(self):
        for module in self.REVModules:
            module.killSwitch()

        self.repetitiveFunctions = []
        self.commMod.closeActivePort()
        self.Quit_button.config(state='disabled')
        self.Connected_Label.config(text='Disconnected')
        for i in range(0, len(self.Tab_frame.tabs())):
            if i < 4:
                self.Tab_frame.tab(i, state='disabled')

    def every_second(self):
        for func in self.repetitiveFunctions:
            func()

        self.root.after(500, self.every_second)

    def joinThreads(self):
        self.repetitiveFunctions = []
        self.commMod.closeActivePort()
        self.root.quit()

    def isValidFirmware(self, filename):
        name, ext = os.path.splitext(filename)
        if ext != '.bin':
            return (False, "Invalid file name, firmware file extension is '.bin'")
        fileSize = os.path.getsize(filename)
        if fileSize > 1048576 or fileSize < 1000:
            return (False, 'Invalid binary size, valid firmware is < 1MB')
        return (
         True, '')

    def firmware_bin_select(self):
        tmpFilename = tkFileDialog.askopenfilename(initialdir='./', title='Select file', filetypes=(('bin files', '*.bin'), ('all files', '*.*')))
        if tmpFilename == None or tmpFilename == '':
            return
        isValid, err = self.isValidFirmware(tmpFilename)
        if isValid == False:
            errMsg = 'Attempted to open invalid firmware file: ' + tmpFilename + '\r\n' + err
            tkMessageBox.showinfo('Invalid Firmware', errMsg)
            print errMsg
        self.filename = tmpFilename
        return

    def firmware_flash(self):
        try:
            if self.filename == None or self.filename == '':
                return
        except:
            return

        isValid, err = self.isValidFirmware(self.filename)
        if isValid == False:
            errMsg = 'Attempted to use an invalid firmware file: ' + self.filename + '\r\n' + err + '\r\n\r\nNo action will be done'
            tkMessageBox.showinfo('Invalid Firmware', errMsg)
            self.firmware.warning_block.config(state='disabled')
            return
        else:
            self.on_quit_button_callback()
            ftserial = ''
            device_list = ft232.list_devices()
            if device_list:
                for FTDI_device in device_list:
                    for element in FTDI_device:
                        self.firmware.warning_block.config(state='normal')
                        if 'FT230X' in element:
                            print 'element: ', element
                            ftserial = FTDI_device[0]
                            print 'serial: ', ftserial
                        else:
                            self.firmware.warning_block.insert(END, 'looking for FT230X\n')
            else:
                self.firmware.warning_block.insert(END, 'no FTDI devices found\n')
                exit()
            if ftserial is not '':
                ftdi_handle = ft232.Ft232(ftserial, baudrate=115200)
                ftdi_handle.cbus_setup(mask=3, init=3)
                ftdi_handle.cbus_write(0)
                time.sleep(0.1)
                ftdi_handle.cbus_write(1)
                time.sleep(0.1)
                ftdi_handle.cbus_write(3)
                self.firmware.warning_block.insert(END, 'board is in program mode, LED should not be flashing\n')
                ftdi_handle.close()
            else:
                self.firmware.warning_block.insert(END, 'did not find FT230X but found other FTDI parts\n')
                self.on_connect_button_callback()
                return
            port = ''
            if self.commMod.REVProcessor.port != None:
                port = self.commMod.REVProcessor.port[3:]
            else:
                allPorts = self.commMod.listPorts()
                if len(allPorts) == 0:
                    errMsg = 'No available com ports, verify connection and try again.\n'
                    tkMessageBox.showinfo('Invalid Firmware', errMsg)
                    self.firmware.warning_block.insert(END, errMsg)
                else:
                    port = allPorts[0].getNumber()
            if port != '':
                osExtension = ''
                if platform.system() == 'Linux':
                    print 'Linux detected, using no extension for sflash executable\n'
                    osExtension = ''
                else:
                    osExtension = '.exe'
                cmdLine = [
                 'sflash' + osExtension, self.filename, '-c', port, '-b', '230400', '-s', '252']
                statusMsg = '\n\nProgramming HUB: COM' + port + ' with file ' + self.filename + '\n\n'
                statusMsg = statusMsg + (' ').join(cmdLine) + '\n\nDO NOT REMOVE POWER WHILE PROGRAMMING...\n\n'
                self.firmware.warning_block.config(state='normal')
                self.firmware.warning_block.insert(END, statusMsg)
                self.root.update_idletasks()
                self.firmware.warning_block.config(state='disabled')
                subprocess.call(cmdLine)
            else:
                errMsg = 'Com port failure, detected Com as: ' + port + '\r\nCheck connection and try again\n'
                tkMessageBox.showinfo('Invalid Firmware', errMsg)
                self.firmware.warning_block.insert(END, errMsg)
                self.on_connect_button_callback()
                self.firmware.warning_block.config(state='disabled')
                return
            self.firmware.warning_block.insert(END, 'Programming Complete, status LED should be blinking,\nyou can now connect to the hub.')
            self.firmware.warning_block.config(state='disabled')

            self.root.update_idletasks()
            self.on_connect_button_callback()
            return


if __name__ == '__main__':
    mp.freeze_support()
    xroot = tk.Tk()
    xroot.title('Crossplatform Hub Interface')
    try:
        xroot.iconbitmap('resource\\\\favicon.ico')
    except:
        try:
            xroot.iconbitmap('favicon.ico')
        except:
            pass

    app = Application(xroot)
    xroot.protocol('WM_DELETE_WINDOW', app.joinThreads)
    print 'Loading application...'
    xroot.mainloop()

# okay decompiling REVHubInterface.pyc
