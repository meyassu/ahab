"""
All the functions in this file assume the images and labels have not yet
been split into train/val/test subsets. The dataset can be unsplit with the
unsplit() function in this file.
"""

import os
import shutil
from sklearn.model_selection import train_test_split

IMAGE_DIR = "../data/images/"
LABEL_DIR = "../data/labels/"
NLABEL_DIR = "../data/labels/norm"
VACUUM_DIR = "../data/vacuums/"

def split():

	print("splitting data...")

	# read images and labels
	images = [os.path.join(IMAGE_DIR, x) for x in os.listdir(IMAGE_DIR) if x[-3:] == "jpg"]
	labels = [os.path.join(LABEL_DIR, x) for x in os.listdir(LABEL_DIR) if x[-3:] == "txt"]
	images.sort()
	labels.sort()

	# split
	train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size = 0.2, random_state = 1)
	val_images, test_images, val_labels, test_labels = train_test_split(val_images, val_labels, test_size = 0.5, random_state = 1)

	# move images
	move_files_to_folder(train_images, os.path.join(IMAGE_DIR, "train"))
	move_files_to_folder(val_images, os.path.join(IMAGE_DIR, "val"))
	move_files_to_folder(test_images, os.path.join(IMAGE_DIR, "test"))

	# move labels
	move_files_to_folder(train_labels, os.path.join(LABEL_DIR, "train"))
	move_files_to_folder(val_labels, os.path.join(LABEL_DIR, "val"))
	move_files_to_folder(test_labels, os.path.join(LABEL_DIR, "test"))

def unsplit():
	"""
	Move all files in train/val/test subsets into top-level folder.
	"""

  print("unsplitting data...")

  # get images
	train_images = [os.path.join(IMAGE_DIR, "train", x) for x in os.listdir(os.path.join(IMAGE_DIR, "train")) if x[-3:] == "jpg"]
	val_images = [os.path.join(IMAGE_DIR, "val", x) for x in os.listdir(os.path.join(IMAGE_DIR, "val")) if x[-3:] == "jpg"]
	test_images = [os.path.join(IMAGE_DIR, "test", x) for x in os.listdir(os.path.join(IMAGE_DIR, "test")) if x[-3:] == "jpg"]

	# get labels
	train_labels  = [os.path.join(LABEL_DIR, "train", x) for x in os.listdir(os.path.join(LABEL_DIR, "train")) if x[-3:] == "txt"]
	val_labels  = [os.path.join(LABEL_DIR, "val", x) for x in os.listdir(os.path.join(LABEL_DIR, "val")) if x[-3:] == "txt"]
	test_labels  = [os.path.join(LABEL_DIR, "test", x) for x in os.listdir(os.path.join(LABEL_DIR, "test")) if x[-3:] == "txt"]

	# move images
	move_files_to_folder(train_images, os.path.join(IMAGE_DIR))
	move_files_to_folder(val_images, os.path.join(IMAGE_DIR))
	move_files_to_folder(test_images, os.path.join(IMAGE_DIR))

	# move labels
	move_files_to_folder(train_labels, os.path.join(LABEL_DIR))
	move_files_to_folder(val_labels, os.path.join(LABEL_DIR))
	move_files_to_folder(test_labels, os.path.join(LABEL_DIR))

def move_files_to_folder(list_of_files, destination_folder):

  for f in list_of_files:
      try:
          shutil.move(f, destination_folder)
      except:
          print(f)
          assert False

def apply_cutoff(video_cutoff, frame_cutoff):
	"""
	Removes invalid images and labels from the dataset

	:video_cutoff: (int) -> the last valid video
	:frame_cutoff: (int) -> the last valid frame in the last valid video
	"""

	print("removing invalid dataset elements beyond cutoff...")

	img_dir = os.fsencode(IMAGE_DIR)
	label_dir = os.fsencode(LABEL_DIR)

	# delete invalid images
	print("removing invalid images...")
	for f in os.listdir(img_dir):
		fname = os.fsdecode(f)
		if fname[-4:] != ".jpg":
			continue
		fname_comp = fname[:-4].split("_")
		video_id = int(fname_comp[0]); frame_id = int(fname_comp[2])
		# beyond cutoff
		if video_id > video_cutoff or frame_id > frame_cutoff:
			os.remove(os.path.join(IMAGE_DIR, fname))

  # delete invalid labels
	print("removing invalid labels...")
	for f in os.listdir(label_dir):
		fname = os.fsdecode(f)
		if fname[-4:] != ".txt":
			continue
		fname_comp = fname[:-4].split("_")
		video_id = int(fname_comp[0]); frame_id = int(fname_comp[2])
		if video_id > video_cutoff or frame_id > frame_cutoff:
			os.remove(os.path.join(LABEL_DIR, fname))

def remove_misformatted_labels():
	"""
	A label is considered misformatted if there are too many
	or too few values in any given line. This function can be expanded
	to include a broader definition if needed.
	"""

	print("removing misformatted labels...")

	num_elements = 5

	labels = [x for x in os.listdir(LABEL_DIR) if x[-3:] == "txt"]

	for l in labels:
		# get video id, frame id
		l_split = l.split("_")
		l_split[2] = l_split[2][:-4]
		video_id = l_split[0]
		frame_id = l_split[2]

		# search for misformatted line
		with open(os.path.join(LABEL_DIR, l), "r") as l_inp:
			for line in l_inp:
				bbox = line.split()
				# remove label, corresponding image
				if len(bbox) != num_elements:
					print(f"misformatted label: {os.path.join(LABEL_DIR, l)}")
					os.remove(os.path.join(LABEL_DIR, l))
					img = video_id + "_frame_" + frame_id + ".jpg"
					os.remove(os.path.join(IMAGE_DIR, img))

def find_vacuums():
	"""
	Finds the (video, frame) tuple of vacuums, images without objects.
	This function assumes that only images without objects lack labels.
	"""

	print("searching for images without objects (vacuums)...")

	image_info = [(int(x[:-4].split("_")[0]), int(x[:-4].split("_")[2])) for x in os.listdir(IMAGE_DIR) if x[-3:] == "jpg"]
	label_info = [(int(x[:-4].split("_")[0]), int(x[:-4].split("_")[2])) for x in os.listdir(LABEL_DIR) if x[-3:] == "txt"]

	# search for images without labels
	vacuums = []
	for img_info in image_info:
		if img_info not in label_info:
			vacuums.append(img_info)

	return vacuums

def move_vacuums(vacuums):
	"""
	Places vacuums, objectless images, in a separate folder.
	"""

	print("moving vacuums into separate directory")

	for v in vacuums:
		v_fname = str(v[0]) + "_frame_" + str(v[1]) + ".jpg"
		shutil.copy(os.path.join(IMAGE_DIR, v_fname), os.path.join(VACUUM_DIR, v_fname))

def generate_vaccum_labels(vacuums):
	"""
	Generates empty txt files for vacuums with proper filenames.
	"""

	pass

def normalize_coordinates(img_width, img_height, safe_mode=True):
	"""
	Normalize pixel coordinates in image labels.

	:param img_width: (int) -> the width of the image (pixels)
	:param img_height: (int) -> the height of the image (pixels)
	:param safe_mode: (bool) -> if safe mode is on, the normalized labels
								will be saved to NLABEL_DIR, otherwise they
								will irreversibly replace the original labels
								and be saved in LABEL_DIR.
	"""

	labels = [x for x in os.listdir(LABEL_DIR) if x[-3:] == "txt"]

	# normalize labels
	for l in labels:
		print(f"normalizing {l}...")

		# set normalized file locations based on safe_mode
		if safe_mode == True:
			norm_fname = os.path.join(NLABEL_DIR, l[:-4] + "_norm.txt")
		else:
			norm_fname = os.path.join(LABEL_DIR, l[:-4] + "_norm.txt")

		# open normalized label file and original label file at once
		with open(norm_fname, "w") as l_norm:
			with open(os.path.join(LABEL_DIR, l), "r") as l_orig:
				for line in l_orig:
					# collect object data
					bbox = line.split()
					class_= int(bbox[0]); x_center = int(bbox[1]); y_center = int(bbox[2]); bbox_width = int(bbox[3]); bbox_height = int(bbox[4])

					x_center, y_center, bbox_width, bbox_height = normalize(x_center, y_center, bbox_width, bbox_height, img_width, img_height)

					# write normalized values to new file
					bbox_norm = str(class_) + " " + str(x_center) + " " + str(y_center) + " " + str(bbox_width) + " " + str(bbox_height) + "\n"
					l_norm.write(bbox_norm)

			# if safe_mode is off, replace the original label with the normalized label
			if safe_mode == False:
				shutil.move(norm_fname, os.path.join(LABEL_DIR, l))

def normalize(x_center, y_center, bbox_width, bbox_height, img_width, img_height):

	return round(x_center / img_width, 4), round(y_center / img_height, 4), round(bbox_width / img_width, 4), round(bbox_height / img_height, 4)

def denormalize(x_center, y_center, bbox_width, bbox_height, img_width, img_height):

	return int(x_center * img_width), int(y_center * img_height), int(bbox_width * img_width), int(bbox_height * img_height)

# apply_cutoff(video_cutoff=1, frame_cutoff=909)
# remove_misformatted_labels()
# normalize_coordinates(img_width=1280, img_height=720, safe_mode=False)
# split()