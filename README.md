# Pose Coding – an interactive system for live coding with body poses

This repository presents the software of Pose Coding. It is related to the respective master thesis.

# Before Starting
Before starting, the necessary libraries have to be installed on the computer. The current software version was only tested on a Apple machine. For other systems, the code might need some adaptations.

* [Conda](https://anaconda.org/anaconda/conda)
* [TensorFlow](https://www.tensorflow.org/)
* [jupyter](https://jupyter.org/)
* [SuperCollider](https://supercollider.github.io/)
* [OpenCV](https://opencv.org/)

# Running with trained model
## 1. Starting SuperCollider
First, the present SuperCollider File sc_setup_pose_coder_stereo.scd has to be opened. In the file: 
* adjust the interface settings
* boot the server
* execute the two closures

## 2. Start Python Module

When executing for the first time, the conda environment has to be created before activating it.

~~~bash
conda create --name tf-jupyter python=3.9
conda activate tf-jupyter
~~~

Then, start the application with: 

~~~bash
python3 pose_coder_main.py
~~~

Next, you are asked to enter SuperCollider's language port. In default cases, you dont have to type anything here, because it sets the SC default lang port 57120. In some cases, the port is altered and then you have to set the right port here.

Then a window opens in which you see the grafical interface of the system.  

# Train Custom Model
The delivered model, thirteen-signs-14kp-rf.pkl includes 13 different body poses that are described in detail in the thesis. 

If you wish to train your own model, follow the workflow described in Train_Custom_Poses.ipynb. 

The notebook can be opened by starting jupyter with the following command:

~~~bash
jupyter lab
~~~

There, open the file and follow the instructions.

# License
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.