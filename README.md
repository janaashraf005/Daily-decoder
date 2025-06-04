# Daily Decoder

**Daily Decoder** is a computer vision–based application that helps travelers interact with unfamiliar public systems in foreign countries—such as bottle recycling machines in Germany, garbage sorting systems in Germany, train ticket machines in Tokyo, and public laundry machines in France. It provides real-time, step-by-step guidance by identifying the device from a captured image and delivering clear, context-aware instructions.
## Purpose

Many travelers struggle with using public devices abroad due to unfamiliar interfaces or language barriers. Daily Decoder addresses this by enabling users to take a photo of the device and receive instant, easy-to-follow instructions.

## How It Works

1. The user captures or streams an image of the device.
2. The application uses OpenCV and feature matching algorithms to identify the specific device.
3. Based on the match, tailored instructions are displayed to guide the user through the interaction process.

## Features

- Real-time image recognition using ORB and FLANN
- Similarity Calculation and Contextual Guidance
- Instructional pop-up interface with tkinter

## Technologies Used

- Python
- OpenCV
- Tkinter

## Impact

The application simplifies complex and unfamiliar systems, reduces user errors, and improves the travel experience by making essential public services more accessible and less intimidating.
