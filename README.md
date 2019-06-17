# To start the project, you must first install:
* [Python 3.6+](https://www.python.org/downloads/)
* [Matterport Mask R-CNN](https://github.com/matterport/Mask_RCNN)
* OpenCV

# After installing all necessary dependencies:
* Copy the file pet_recognition.py to the directory with the Mask R-CNN
* Create a test_images directory
* Add to the directory test_images video file on which you want to recognize the cat
* Change the video source file path in the VIDEO_SOURCE in the pet_recognition.py
* run the script through a terminal or console command

Linux
```
python3 pet_recognition.py
``` 

Windows
```
python pet_recognition.py
``` 

# What result is expected:
* the video stream starts and breaks into frames
* the neural network searches for a pet at each frame (the first appearance of the pet on the video and its subsequent movements are taken into account)
* Count the number of frames on which there is no pet.
* notification of the appearance in the frame of a pet
* notification of pet leaving the frame