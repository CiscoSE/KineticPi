# KineticPi
Code for a Cisco Kinetic demonstration using a Raspberry Pi to create sensor data, transport it to the Kinetic cloud and pull it to display.

The KineticPi demonstration allows users to showcase the power and simplicity of the Kinetic framework's dashboard in onboarding sensors and sending data to the Kinetic cloud. Afterward, it can be extracted from the cloud again with another script to simulate an application that would store, process or display the data. In the case of this repository, the data is intended to be displayed using a dashboard software called freeboard.

The repository is composed of 3 components:

1. A Python script for making the Raspberry Pi sensor pollable by HTTP
2. A Java application that can be packaged onto a Cisco 8*9 gateway registered to the Kinetic framework which will poll the Pi for sensor data and, based on rules specified in the Kinetic dashboard, send the data at a specific frequency to the Kinetic Cloud
3. A Python script that then grabs this data out of the Kinetic cloud and stores it locally and a script that runs a CORS-enabled HTTP server to present the data in a dashboard using [freeboard](https://github.com/Freeboard/freeboard) 

For more detailed instructions on deploying this demonstration, see the deployment guide.
