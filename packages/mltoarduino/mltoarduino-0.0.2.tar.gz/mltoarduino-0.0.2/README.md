<h1 style="text-align:center;">
Convert a Python Machine Learning Model to Arduino Code (C++)
</h1>

# Introduction

### Motivation

<div id = "contenner" style="display: flex;gap: 20px; width: 100%;">
<div id = "left_div" style="flex: 2;">
    <b>What ?</b> 
<br>
This project demonstrates the conversion of Python machine learning (ML) models to Arduino C++ code. 
<br>
We will use some ML models purely as examples; the goal is not to find the best model or achieve minimal error. 
<br> 
    <b>Why ?</b> 
<br>
In certain applications, such as embedded systems, small microcontrollers with limited memory and computing resources are used. The idea is to train a machine learning model in a Python environment and then convert the trained model to C++ for deployment on a microcontroller. 
<br>
In this project, we will use the Arduino Uno as an example, but the approach can be applied to other microcontrollers as well. 
<br>
<b>How ?</b> 
<br> 
Follow the step-by-step guide below, or go directly to the PyPi package <a href="https://pypi.org/search/?q=mltoarduino">mltoarduino</a>
</div>
<div id = "right_div" style="flex: 1 ;width:80%">
<img src = "https://bouz1.github.io/fils/MLModelToArduinoCpp/illustration.png">   
<div>
<div>

### Hardware

In this project, the Arduino Uno was used, but you can use other boards like Arduino Nano or Micro, Miga 2560, ESP32... <br> 
below a comparaison of some Arduino boards: 

| Feature                | Arduino Uno        | Arduino Nano       | Arduino Micro      | Arduino Mega 2560   | ESP32                |
|------------------------|--------------------|--------------------|--------------------|----------------------|----------------------|
| **Microcontroller**    | ATmega328P        | ATmega328P         | ATmega32U4         | ATmega2560           | Tensilica Xtensa LX6 |
| **Operating Voltage**  | 5V                | 5V                 | 5V                 | 5V                   | 3.3V                 |
| **Input Voltage**      | 7-12V             | 7-12V              | 7-12V              | 7-12V                | 5V via USB or 7-12V  |
| **Digital I/O Pins**   | 14 (6 PWM)        | 14 (6 PWM)         | 20 (7 PWM)         | 54 (15 PWM)          | 34                   |
| **Analog Input Pins**  | 6                 | 8                  | 12                 | 16                   | 18                   |
| **Flash Memory**       | 32 KB             | 32 KB              | 32 KB              | 256 KB               | Up to 16 MB          |
| **SRAM**               | 2 KB              | 2 KB               | 2.5 KB             | 8 KB                 | 520 KB               |
| **EEPROM**             | 1 KB              | 1 KB               | 1 KB               | 4 KB                 | None                 |
| **Clock Speed**        | 16 MHz            | 16 MHz             | 16 MHz             | 16 MHz               | 240 MHz (dual-core)  |
| **Connectivity**       | UART, I2C, SPI    | UART, I2C, SPI     | UART, I2C, SPI     | UART, I2C, SPI       | Wi-Fi, Bluetooth     |
| **USB Interface**      | USB-B             | Mini USB           | Micro USB          | USB-B                | Micro USB            |
| **Dimensions**         | 68.6 x 53.4 mm    | 45 x 18 mm         | 48 x 18 mm         | 101.52 x 53.3 mm     | 51 x 25.5 mm         |
| **Power Consumption**  | ~50 mA            | ~50 mA             | ~50 mA             | ~70 mA               | Varies (~80-240 mA)  |
| **Special Features**   | Simple and robust | Compact            | USB HID support    | High I/O count       | Wi-Fi and BLE        |
| **Price Range**        | Low               | Low                | Medium             | Medium               | Medium-High          |

# How to use the package


```python
!pip install mltoarduino
```


```python

```
