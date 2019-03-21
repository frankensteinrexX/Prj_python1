# -*- coding: utf-8 -*-
"""
Objective: Estimation of Height of a Building using a Barometer

Description : Analysing and familiarizing Numpy and Panda
Micro project : Estimating the Height of a building
This project depends upon a Pressure sensor which provides the change in
atmospheric pressure(hPa) when in a lift.
Sensor reading are taken from an iphone 6s and Sensortoolbox Application
1. Barometeric sensor
 1.1 Averaging height difference calculated using Barometric Formula
 1.2 Finding the vertical velocity of the Elevator using Accelerometer
 1.3 3D mapping the position of elevator
 1.4 Inferences about the elevator(Too Fast/Slow)
 1.5 applicable from small buildings to skyscrappers //reference file

Sensors data used:  Barometer/Pressure Sensor
                    Accelerometer
                    Location

@author: Prithviraj Chouhan

Version : 3.7

Date: 19/03/2019

Initial Static Code Analysis Score - > 5.71/10
Final Static Code Analysis Score - >9.39/10"""
# Import the excel file and call it xls_file
import pandas as pd
import matplotlib.pyplot as plt
import gmplot

def press_height(df):
    '''function to convert pressure to height'''
    init = df[0]
    df = ((init - df)*(100))/(9.8*1.225)
    return df

EXCEL_FILE = pd.ExcelFile('barometer_final.xls')
# View the excel_file's sheet names
print(EXCEL_FILE.sheet_names, "\n")

# Load the excel_file's Sheet1 as a dataframe
DF_ACC = EXCEL_FILE.parse('Accelerometer')
print(DF_ACC)
# Load the excel_file's Sheet2 as a dataframe
DF_BAR = EXCEL_FILE.parse('Barometer')
print(DF_BAR)
# Load the excel_file's Sheet3 as a dataframe
DF_LOC = EXCEL_FILE.parse('Location')
print(DF_LOC)

#%%re-defining Coloumns
#Accelerometer
DF_ACC.columns = ['Time',
                  'Accx',
                  'Accy',
                  'Accz']
#Pressure sensor
DF_BAR.columns = ['Time',
                  'Pressure']
#Location Sensor
DF_LOC.columns = ['Time',
                  'Lat',
                  'Longitude',
                  'Height',
                  'Velocity',
                  'Direction',
                  'Horizontal_Accuracy',
                  'Vertical_Accuracy']

#initial Plots
DF_BAR.plot(x='Time', y='Pressure', style='o')
DF_LOC.plot(x='Time', y='Longitude', style='o')
DF_ACC.plot(x='Time', y='Accz', style='*')

#%%
#Plotting the inferences
HEIGHT_BUILDING = pd.Series.to_frame(press_height(DF_BAR.Pressure))
plt.figure()
plt.title("Pressure vs Height")
plt.plot(DF_BAR.Pressure, HEIGHT_BUILDING,
         color="blue", label="press vs height")
plt.legend()
plt.axis([950, 1000, 0, 20])
plt.xlabel("Pressure (hPa)")
plt.ylabel("Height (m)")
plt.show()

plt.figure()
plt.title("Accelerometer vs Time")
plt.plot(DF_ACC.Time, DF_ACC.Accz, color="red")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Vertical Velocity (m/s))")
plt.show()
AVERAGE_VELOCITY = (DF_ACC.Accz.mean() - 9.81)

if AVERAGE_VELOCITY > 1.5:
    print("Elevator too fast Danger!!")
elif AVERAGE_VELOCITY < 1.5 and AVERAGE_VELOCITY > 0.5:
    print("Elevator is at optimum speed level")
elif AVERAGE_VELOCITY < 0.5 and AVERAGE_VELOCITY > 0:
    print("Elevator is too slow")
else:
    print("Elevator stopped or Malfunctioned")

#Plotting the location of the Noise on the maps using the Gmplot.
LONGITUDE = DF_LOC.Longitude
LATITUDE = DF_LOC.Lat
GMAP4 = gmplot.GoogleMapPlotter(LATITUDE[0], LONGITUDE[0], 10)
GMAP4.heatmap(LATITUDE, LONGITUDE, 30)
GMAP4.draw("map.html")
