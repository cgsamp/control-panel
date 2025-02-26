#!/bin/bash
# Use -c to create a new password_file. Then use -b to add subsequent Batch
sudo mosquitto_passwd -c /etc/mosquitto/password_file your_device DevicePassword
sudo mosquitto_passwd -b /etc/mosquitto/password_file your_controller ControllerPassword
