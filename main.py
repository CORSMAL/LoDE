################################################################################## 
#        Author: Ricardo Sanchez Matilla
#         Email: ricardo.sanchezmatilla@qmul.ac.uk
#  Created Date: 2020/02/13
# Modified Date: 2020/02/28

# Centre for Intelligent Sensing, Queen Mary University of London, UK
# 
################################################################################## 
# License
# This work is licensed under the Creative Commons Attribution-NonCommercial 4.0
# International License. To view a copy of this license, visit 
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to 
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
##################################################################################


# System libs
import glob
import sys
import argparse

# Numeric libs
import cv2
import numpy as np
import torch
import torchvision

from numpy import linalg as LA

import shutil
import os

import pickle

from tqdm import tqdm


# Computer Vision libs
from libs._3d.projection import *
from libs.detection.detection import imageSegmentation


device = 'cuda' if torch.cuda.is_available() else 'cpu'

class LoDE:
	def __init__(self, args):

		self.args = args

		self.c1 = dict.fromkeys(['rgb', 'seg', 'intrinsic', 'extrinsic'])
		self.c2 = dict.fromkeys(['rgb', 'seg', 'intrinsic', 'extrinsic'])

		self.dataset_path = 'dataset'

		self.output_path = 'results'
		if not os.path.exists(self.output_path):
			os.makedirs(self.output_path)

		f = open('{}/estimation.txt'.format(self.output_path), 'w')
		f.write('fileName\theight[mm]\twidth[mm]\n')
		f.close()

		# Load object detection model
		self.detectionModel = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
		self.detectionModel.eval()
		self.detectionModel.cuda()

	def getObjectDimensions(self):
		
		f = open('{}/estimation.txt'.format(self.output_path), 'a+')
		try:
			centroid1, contour1 = getCentroid(self.c1['seg'])
			centroid2, contour2 = getCentroid(self.c2['seg'])

			centroid = cv2.triangulatePoints(self.c1['extrinsic']['projMatrix'], self.c2['extrinsic']['projMatrix'], centroid1, centroid2).transpose()
			centroid /= centroid[:,-1].reshape(-1,1)
			centroid = centroid[:,:-1].reshape(-1)
			
			height, width, visualization = getObjectDimensions(self.c1, self.c2, centroid, self.args.draw)
			cv2.imwrite('{}/id{}_l{}_b{}.png'.format(self.output_path, self.args.object, self.args.lighting, self.args.background), visualization )
			
			f.write('id{}_l{}_b{}.png\t{:.2f}\t{:.2f}\n'.format(self.args.object, self.args.lighting, self.args.background, height, width))
			print('Object {}, lighting {}, and background {} measured!'.format(self.args.object, self.args.lighting, self.args.background))
		
		except:
			f.write('id{}_l{}_b{}.png\terror\terror\n'.format(self.args.object, self.args.lighting, self.args.background))
			print('Error measuring object {}, lighting {}, and background {}'.format(self.args.object, self.args.lighting, self.args.background))
		f.close()

	def readData(self):			
		# Read images from Camera 1
		self.c1['rgb'] 	= cv2.imread('{}/images/id{}_l{}_b{}_c1_rgb.png'.format(self.dataset_path, self.args.object, self.args.lighting, self.args.background))
		self.c1['seg'] = imageSegmentation(self.detectionModel, self.c1['rgb'])

		# Read images from Camera 2
		self.c2['rgb'] 	= cv2.imread('{}/images/id{}_l{}_b{}_c2_rgb.png'.format(self.dataset_path, self.args.object, self.args.lighting, self.args.background))
		self.c2['seg'] = imageSegmentation(self.detectionModel, self.c2['rgb'])

  # Read calibration file for the chosen setup 
	def readCalibration(self):
		if self.args.lighting in [0,1]:	
			setup = 1
		else:
			setup = 2

		with open('./dataset/calibration/S{}/c1_calib.pickle'.format(setup), 'rb') as f:
			u = pickle._Unpickler(f)
			u.encoding = 'latin1'
			c1_intrinsic, c1_extrinsic = u.load()
		with open('./dataset/calibration/S{}/c2_calib.pickle'.format(setup), 'rb') as f:
			u = pickle._Unpickler(f)
			u.encoding = 'latin1'
			c2_intrinsic, c2_extrinsic = u.load()

		self.c1['intrinsic'] = c1_intrinsic['rgb']
		self.c1['extrinsic'] = c1_extrinsic['rgb']
		self.c2['intrinsic'] = c2_intrinsic['rgb']
		self.c2['extrinsic'] = c2_extrinsic['rgb']


	def run(self):
		
		# Read camera calibration files
		self.readCalibration()

		# Main loop
		self.readData()

		self.getObjectDimensions()


if __name__ == '__main__':

	# Parse arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('--object', type=int, default=0)
	parser.add_argument('--lighting', type=int, default=0)
	parser.add_argument('--background', type=int, default=0)
	parser.add_argument('--draw', default=False, action='store_true', help='Output visual results in ./results')
	args = parser.parse_args()

	print('Executing...')
	lode = LoDE(args)
	if args.object==0:	#All objects
		for args.object in tqdm(range(1,23)):
			for args.lighting in range(0,2):
				for args.background in range(0,2):
					lode.run()
	else:
		lode.run()

	print('Completed!')
