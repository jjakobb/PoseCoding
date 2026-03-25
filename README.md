# Pose Coding – an interactive system for live coding with body poses

This repository presents the software of Pose Coding, related to the respective master thesis. The system uses a webcam to detect body poses in real time and maps them to live coding commands sent to SuperCollider via OSC.

---

## Requirements

- **macOS** (tested on Apple Silicon and Intel Mac)
- **[Miniforge](https://github.com/conda-forge/miniforge)** (conda package manager)
- **[SuperCollider](https://supercollider.github.io/)**

> The software was developed and tested on macOS. Other platforms may require adaptations.

---

## Installation (macOS)

### 1. Install Miniforge

If you don't have Miniforge installed yet:

```bash
brew install --cask miniforge
```

Then close and reopen your terminal so that `conda` is available.

### 2. Create the conda environment

From the root of this repository, run:

```bash
conda env create -f environment.yml
```

This installs all required packages including OpenCV, MediaPipe, scikit-learn, and python-osc.

> **Note on package versions:** MediaPipe (`0.10.13`) and protobuf (`4.25.3`) are pinned to specific versions. Newer versions of these packages are known to cause compatibility issues. Do not upgrade them without testing.

### 3. Activate the environment

```bash
conda activate posecoding
```

---

## Running the system

### 1. Start SuperCollider

Open `sc_setup_pose_coder_stereo.scd` in SuperCollider and:

1. Adjust the audio interface settings at the top of the file
2. Boot the server
3. Execute both closures (Cmd+Return on each)

### 2. Start the Python application

Make sure the conda environment is active, then run:

```bash
python3 pose_coder_main.py
```

You will be prompted to enter SuperCollider's language port. In most cases, just press Enter to use the default port `57120`. If you changed the SC port, enter the correct value here.

A window opens showing the graphical interface of the system.

---

## Training a custom model

The included model (`thirteen-signs-14kp-rf.pkl`) contains 13 body poses described in detail in the thesis. To train your own model, use the provided Jupyter notebook:

```bash
jupyter lab
```

Then open `Train_Custom_Poses.ipynb` and follow the instructions inside.

---

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](./LICENSE) file for details.
