import cv2
import numpy as np
import os
import argparse

def draw_bbox(infer_dir, img_sdir, img_ddir, img_width, img_height):
	"""
	Gets bounding box data, applies a shift, and draws the bounding box.

	:param infer_dir: (str) -> the directory containing the inferences e.g. yolo_cone_det/labels/
	:param img_sdir: (str) -> the directory containing the original images e.g. jetson_nano/ or train/
	:param img_ddir: (str) -> the destination directory for the annotated images e.g. yolo_cone_det/
	:param img_width: (int) -> the image width
	:param img_height: (int) -> the image height
	"""

	print("drawing bounding boxes...")

	infers = [x for x in os.listdir(infer_dir) if x[-3:] == "txt"]
	images = [x for x in os.listdir(img_sdir) if x[-3:] == "jpg"]

	# align inferences, images
	infers.sort()
	images.sort()

	# White: blue, Black: green, Green: red
	classID_to_class = {0:"BG", 1:"White", 2:"Black", 3:"Green"}
	classID_to_color = {0:None, 1:(255,0,0), 2:(0,255,0), 3:(0,0,255)}
	rect_thickness = 3
	text_color = (255, 255, 255)

	for inf, image in zip(infers, images):
		print(f"processing {(inf, image)}...")
		# get corresponding image
		img = cv2.imread(os.path.join(img_sdir, image), cv2.IMREAD_COLOR)
		with open(os.path.join(infer_dir, inf)) as f_inf:
			for line in f_inf:
				# get bbox data, denormalize
				bbox = line.split()
				classID = int(bbox[0]); x_center = float(bbox[1]); y_center = float(bbox[2]); bbox_width = float(bbox[3]); bbox_height = float(bbox[4])
				x_center, y_center, bbox_width, bbox_height = denormalize(x_center, y_center, bbox_width, bbox_height, img_width, img_height)

				# shift bbox, draw on image
				top_left = (x_center, y_center)
				bottom_right = (x_center + bbox_width, y_center + bbox_height)
				cv2.rectangle(img, top_left, bottom_right, classID_to_color[classID], rect_thickness)

				# label rectangle
				cv2.putText(img, classID_to_class[classID], (top_left[0]-50, top_left[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

		# save img
		cv2.imwrite(os.path.join(img_ddir, image), img)

def denormalize(x_center, y_center, bbox_width, bbox_height, img_width, img_height):

	return int(x_center * img_width), int(y_center * img_height), int(bbox_width * img_width), int(bbox_height * img_height)



parser = argparse.ArgumentParser(description="Postprocessing script")
parser.add_argument("--name", type=str, help="Job name (NOTE: ensure this job name matches job name given to detect.py)", required=True)

args = parser.parse_args()
name = args.name

INFER_DIR = "../output/" + name + "/labels/"
SDIR = "../data/images/test/"
DDIR = "../output/" + name

draw_bbox(infer_dir= INFER_DIR, img_sdir=SDIR, img_ddir=DDIR, img_width=1280, img_height=720)





