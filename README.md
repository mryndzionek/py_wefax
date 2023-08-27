# Decoding Weatherfax in Python

A Python script decoding USB radio signals recorded as WAV files
to images. The recordings need to start with at least
10s of synchronization pulses.
 
![websdr_settings](images/websdr.png)

All contents of this repo are for educational purposes.
Copyright of the faxed material belongs to the transmitting agencies.

#### Example outputs:

![img_1](images/07:17:08-3853.1-Pinneberg-1693120628.png)

![img_2](images/07:30:08-3853.1-Pinneberg-1693121408.png)

![img_3](images/08:17:08-5278f06158064f19-3853.1-Pinneberg-1693124228.png)

![img_4](images/08:20:08-06cce9bc651878b0-7793.1-JMH-1693124408.png)

![img_5](images/1693134008-11:00:08-7793.1-JMH-06cce9bc651878b0.png)

![img_6](images/1693135148-11:19:08-7793.1-JMH-06cce9bc651878b0.png)

![img_7](images/1693136408-11:40:08-7793.1-JMH-de3cef578287c347.png)

![img_8](images/1693138808-12:20:08-7793.1-JMH-3d95ec5e52cf2381.png)

![img_9](images/1693140008-12:40:08-7793.1-JMH-06cce9bc651878b0.png)

![img_10](images/1693140668-12:51:08-7793.1-JMH-3d95ec5e52cf2381.png)

![img_11](images/1693141388-13:03:08-7793.1-JMH-9b7b5c5451ad62e6.png)

![img_12](images/1693141808-13:10:08-7793.1-JMH-3d95ec5e52cf2381.png)

![img_13](images/20230826T170105Z_7793100_usb.png)

![img_14](images/20230826T171911Z_7793100_usb.png)

![img_15](images/20230826T173906Z_7793100_usb.png)

![img_16](images/20230826T181006Z_7793100_usb.png)

![img_17](images/20230826T182104Z_7793100_usb.png)

![img_18](images/20230826T183210Z_7793100_usb.png)

![img_19](images/20230826T185031Z_7793100_usb.png)

![img_20](images/20230826T191015Z_7793100_usb.png)

![img_21](images/20230826T195006Z_7793100_usb.png)

![img_22](images/20230826T201003Z_7793100_usb.png)

![img_23](images/20230826T210005Z_4608100_usb.png)

![img_24](images/20230826T214011Z_7793100_usb.png)

![img_25](images/20230826T222013Z_7793100_usb.png)

![img_26](images/20230827T054812Z_7793100_usb.png)

![img_28](images/websdr_recording_start_2023-08-23T07_43_20Z_7878.9kHz.png)

![img_29](images/websdr_recording_start_2023-08-24T14_00_40Z_7878.7kHz.png)

![img_30](images/websdr_recording_start_2023-08-24T14_12_39Z_7878.7kHz.png)

![img_31](images/websdr_recording_start_2023-08-24T14_24_41Z_7878.7kHz.png)

![img_32](images/websdr_recording_start_2023-08-24T14_44_46Z_7878.0kHz.png)

![img_33](images/websdr_recording_start_2023-08-24T15_08_30Z_7878.1kHz.png)

![img_34](images/websdr_recording_start_2023-08-24T16_32_41Z_7878.1kHz.png)

![img_35](images/websdr_recording_start_2023-08-24T18_00_03Z_7878.1kHz.png)

![img_36](images/websdr_recording_start_2023-08-24T18_20_33Z_7878.1kHz.png)

![img_37](images/websdr_recording_start_2023-08-24T18_36_12Z_7878.1kHz.png)

![img_38](images/websdr_recording_start_2023-08-24T18_51_12Z_7878.1kHz.png)

![img_39](images/websdr_recording_start_2023-08-24T19_04_07Z_7878.1kHz.png)

![img_40](images/websdr_recording_start_2023-08-24T19_15_53Z_7878.1kHz.png)

![img_41](images/websdr_recording_start_2023-08-24T19_27_37Z_7878.1kHz.png)

![img_42](images/websdr_recording_start_2023-08-24T19_39_46Z_7878.1kHz.png)

![img_43](images/websdr_recording_start_2023-08-25T05_25_08Z_3853.1kHz.png)

![img_44](images/websdr_recording_start_2023-08-25T08_30_07Z_3853.1kHz.png)

![img_45](images/websdr_recording_start_2023-08-25T08_43_08Z_3853.1kHz.png)

![img_46](images/websdr_recording_start_2023-08-25T08_55_19Z_3853.1kHz.png)

![img_47](images/websdr_recording_start_2023-08-25T09_43_08Z_3853.1kHz.png)

![img_48](images/websdr_recording_start_2023-08-25T09_55_10Z_3853.1kHz.png)

![img_49](images/websdr_recording_start_2023-08-25T10_16_08Z_3853.1kHz.png)

![img_50](images/websdr_recording_start_2023-08-25T10_28_08Z_3853.1kHz.png)

![img_51](images/websdr_recording_start_2023-08-25T10_40_09Z_3853.1kHz.png)

![img_52](images/websdr_recording_start_2023-08-25T11_32_08Z_3853.0kHz.png)

![img_53](images/websdr_recording_start_2023-08-25T11_44_09Z_3853.0kHz.png)

![img_54](images/websdr_recording_start_2023-08-25T11_56_47Z_3853.0kHz_1.png)

![img_55](images/websdr_recording_start_2023-08-25T11_56_47Z_3853.0kHz_2.png)

![img_56](images/websdr_recording_start_2023-08-25T11_56_47Z_3853.0kHz_3.png)

![img_57](images/websdr_recording_start_2023-08-25T11_56_47Z_3853.0kHz_4.png)

![img_58](images/websdr_recording_start_2023-08-25T11_56_47Z_3853.0kHz_5.png)

![img_59](images/websdr_recording_start_2023-08-25T11_56_47Z_3853.0kHz_6.png)

![img_60](images/websdr_recording_start_2023-08-25T18_00_38Z_4608.1kHz.png)

![img_61](images/websdr_recording_start_2023-08-26T08_55_19Z_3853.1kHz_1.png)

![img_62](images/websdr_recording_start_2023-08-26T08_55_19Z_3853.1kHz_2.png)

![img_63](images/websdr_recording_start_2023-08-26T09_31_08Z_3853.1kHz.png)

