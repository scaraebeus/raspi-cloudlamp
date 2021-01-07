raspi-cloudlamp
===============

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

What is raspi-cloudlamp?
------------------------

raspi-cloudlamp is an interactive led cloud lamp built around the Raspberry Pi platform.

This was originally inspired by the `interactive cloud lamp <https://www.rclarkson.com/collections/clouds/products/speaker-cloud>`_ 
from Richard Clarkson Studio. There are `plenty <https://www.instructables.com/LED-Cloud-Light/>`_ of `examples <https://diyprojectsforteens.com/how-to-make-a-diy-cloud-light/>`_ 
of `DIY cloud <https://www.youtube.com/watch?v=vwb2obZW47s>`_ led lamps out there, built around different platforms such as `Arduino <https://learn.sparkfun.com/tutorials/led-cloud-connected-cloud/all>`_, 
`color-changing lightbulbs <https://diy.dunnlumber.com/projects/how-to-make-an-interactive-cloud-lamp>`_ (like Philips Hue), remote controlled battery powered color changing strips, etc.

The aim of this project is to build a fully interactive led cloud lamp with the features listed below.

Features
~~~~~~~~

* Unique visuals/animations representing various weather conditions with the ability to display the current condition based on the set location
* Realistic lightning animations
* Select from a range of different visual modes - including changing colors and color intensities
* Sound reactivity across the various modes
* Ability to play sounds through built-in speakers - such as playing rain or thunderstorm sounds in sync with visual animations
* Controled through IR remote, web interface, and/or bluetooth

What's needed to make this?
---------------------------

There are both hardware and software requirements in order to create a cloud lamp from this project.  The project was built using a Raspberry Pi ZeroW, NeoPixels, an Adafruit mini remote, 
and the Raspberry PI OS (Dec 2, 2020 release).

Hardware
~~~~~~~~

* Raspberry PI (tested on a ZeroW, though should work with any PIs as long as there is WiFi/BT)
* MicroSD card (any size should do - tested with 16GB which was way more than plenty)
* 48 NeoPixels - using 30 led/meter strip
* 1x TSOP38238 IR Sensor - for use with IR remote
* 1x Adafruit mini remote - NEC based remote
* 1x 74AHCT125 Level shift - for converting 3V to 5V
* 1x 1000uF 16V Capacitor
* 3x JST SM 3-pin Male/Female plug pairs
* 1x Male/Female 5.5 X 2.1mm DC power plug pair
* 1x 2.1mm female/male barrel jack extension cable - 1.5m / 5 ft
* 1x MicroUSB plug to 5.5/2.1mm DC barrel jack adapter
* 1x small perf board - for level shifter and breakout connectors to IR and NeoPixels
* 1x set of female/male 20x2 headers for Raspberry PI to ease perfboard connection
* 24awg hookup wire
* Container of some type as the base for the cloud - ractangular clear plastic food storage container for example
* Enough polyfill to cover base container
* Clear nylon wire - for hanging the cloud

Software
~~~~~~~~

* Raspberry PI OS (Debian Buster - Dec 2, 2020 release was used)
* Python 3.7+
* Adafruit Blinka Library (CircuitPython implementation for Raspberry PI)
* Adafruit LED Animations Library
* Python-evdev Library


Guide
-----

This is still to come . . .
