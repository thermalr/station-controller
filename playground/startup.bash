#!/bin/bash

until ping -c1 www.google.com >/dev/null 2>&1; 
do sleep 2
done
#python3 /home/pi/Docking_station/test_scripts/Docking_station_multiple_test.py
python3 /home/pi/Docking_station/test_scripts/mqtt_client_fifo_test.py 
