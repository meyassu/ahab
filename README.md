# uav


## Table of Contents
- [Overview](#overview)
- [Repository Contents](#repository-contents)
- [Background](#background)
- [Instructions](#instructions)

## Overview
The software in this repository was developed for an aquatic UAV in preparation for an obstacle course competition on the Potomac River (2022) which consisted of various buoys and other static objects floating in the water. This repository contains a YOLOv5 neural network trained on images of a static obstacle course in an aquatic environment; credit to @john-kliem and @wellssam100 for helping with collecting + labeling dataset and to @glenn-jocher / @ultralytics for NN definition + training + inference programs.

## Repository Contents

- data/ contains the test images the user can run the model on for demo purposes

- model/ contains the model weights
	- model/performance/ contains representative metrics of performance (e.g. F1 curve, PR curve, confusion matrix etc...) from a thorough evaluation process involving hundreds of images

- output/ will contain the model outputs; note that outputs will be saved under a subdirectory whose name corresponds to the job name the user provides when issuing the command to run the model (see #instructions for more information)
	- output/samples/ contains some samples for the user to see.

- src/ contains the source code 
	- detect.py actually performs the YOLOv5 inference (written by @ultralytics)
	- export.py exports the model (written by @ultralytics)
	- postprocess.py corrects a slight miscalculation in the dataset labeling
	- preprocess.py was initially applied to the training dataset, which is not included here due to storage restrictions
	- requirements.txt specifies the necessary environment to run the source files
	- train.py was used to train the YOLOv5 on the custom dataset (written by @ultralytics)
	- val.py was used for validation / to prevent overfitting during training (written by @ultralytics)


## Background
 Modern Unmanned Autonomous Vehicles (UAVs) rely heavily on advanced machine-learning models to perform real-time object detection, localization, and recognition. This information enables them to build high-resolution / information-dense maps of the environment which, in turn, better positions them to independently make good navigational decisions.

 The YOLO object detection algorithm was originally created by Joseph Redmon in 2015 and subsequently improved on by others, including Glenn Jocher (@glenn-jocher) and his company, Ultralytics (@ultralytics), who are now spearheading efforts to improve AI vision algorithms. The fundamental contribution of the YOLO network lies in its ability to look at a given image in its totality and to simultaneously predict bounding box coordinates and object class. It resembles the human visual system more than any other algorithm proposed thus far and is capable of generalizing across image styles (e.g. natural, artistic, etc. . . ). The general idea behind the algorithm is simple to understand. It first breaks up the image into an SxS grid and commands each cell of the grid to generate a set of bounding boxes based on local features. The grid cell also computes a set of class probabilities based on local features and uses these probabilities to classify each bounding box. YOLO has various limitations. For instance, it struggles to accurately identify clusters of small objects. The dataset it was trained on here, though, plays well to its strengths.

 Traditional object detection algorithms function by compartmentalizing their operations into several disjoint components. They tend to repurpose existing methods designed for other problems instead of developing specialized techniques from scratch. For this reason, they are commonly unwieldy and slow. Since each component is oriented around a relatively isolated subproblem, the loss functions governing the models in the system are unrelated to the cumulative aim of the algorithm, object detection. This explains, at least in part, the subpar accuracy of these early techniques such as Deformable Parts Model (DPM) and FR-CNN. 

## Instructions
To install dependencies, navigate to src/ and enter
~~~
python -m pip install requirements.txt
~~~

To run the model, navigate to src/ and enter

~~~
python detect.py --save-txt --source ../data/images/test --weights ../model/best.pt --conf 0.5 --name [JOB_NAME]
~~~

The job name must be unique to all previous runs.

Go to output/JOB_NAME/ to view the output images. Due to a slight miscalculation, the bounding boxes will be offset by a constant value. To correct this, please run the postprocessing script by navigating to src/ and running:

~~~
python postprocess.py --name [JOB_NAME]
~~~

The JOB_NAME given here must be identical to the JOB_NAME given previously when running detect.py. Now, the bounding boxes should be positioned over the center (approximately) of each object in the image.








