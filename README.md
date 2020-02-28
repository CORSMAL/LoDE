# Multi-view shape estimation of transparent containers

*Authors*:
* Alessio Xompero
* Ricardo Sanchez-Matilla
* Apostolos Modas
* Pascal Frossard
* Andrea Cavallaro

Created date: 2020/02/28

Version: 0.1

Resource type: software

## Description
LoDE (Localisation and Object Dimensions Estimator) is a method for jointly 
localising container-like objects and estimating their dimensions using 
two wide-baseline, calibrated RGB cameras. Under the assumption of circular 
symmetry along the vertical axis, LoDE estimates the dimensions of an object 
with a generative 3D sampling model of sparse circumferences, iterative shape 
fitting and image re-projection to verify the sampling hypotheses in each camera 
using semantic segmentation masks (Mask R-CNN).

[LoDE webpage](http://corsmal.eecs.qmul.ac.uk/LoDE.html)
[CORSMAL Containers dataset](http://corsmal.eecs.qmul.ac.uk/containers.html)

## Tested on
* Python 3.6.8
* OpenCV 4.1.0
* PyTorch 1.4.0
* TorchVision 0.5.0
* NVIDIA CUDA 10.1
* CORSMAL Containers dataset

Tested on Linux machine with Ubuntu 16.04 LTS


## Installation
Download or clone the repository.
```
git clone https://github.com/CORSMAL/LoDE.git
```

We recomend creating an anaconda environment ([more info on how to install miniconda](https://docs.conda.io/en/latest/miniconda.html))

```
conda create -n LoDE python=3.6.8
source activate LoDE
```

Install dependencies in the environment

```
pip install -r requirements.txt
```

## Preparing the CORSMAL Containers dataset
Download the CORSMAL Containers dataset
```
cd <rootPath>
wget http://corsmal.eecs.qmul.ac.uk/data/ICASSP20/CORSMAL_containers_dataset.zip
unzip CORSMAL_containers_dataset.zip
mv CORSMAL_Containers dataset
rm CORSMAL_containers_dataset.zip
```

The dataset should be in the same working directory than LoDE. The dataset folder should be
named _dataset_ and should be structured as the CORSMAL Containers dataset (see current structure).

Run LoDE on the whole dataset
```
python main.py --object=0 --draw
```

## Demo with a pair of images
Run LoDE with a sample of the CORSMAL Containers dataset (e.g. object 15, lighting 0, and background 0; contained on ./dataset/images)
```
python main.py --object=15 --lighting=0 --background=0 --draw
```

## Output
LoDE outputs two results:
* Dimensions estimation of the height and width of the container in milimeters in results/estimation.txt
* Visual representation of the container shape in results/*.png. The visual representation can be removed by omitting the --draw commands


## Citation
If you use this data, please cite:
A. Xompero, R. Sanchez-Matilla, A. Modas, P. Frossard, and A. Cavallaro, 
_Multi-view shape estimation of transparent containers_, Published in the IEEE 
2020 International Conference on Acoustics, Speech, and Signal Processing,
Barcelona, Spain, 4-8 May 2020.

Bibtex:
@InProceedings{Xompero2020ICASSP,
  TITLE   = {Multi-view shape estimation of transparent containers},
  AUTHOR  = {A. Xompero, R. Sanchez-Matilla, A. Modas, P. Frossard, and A. Cavallaro},
  BOOKTITLE = {IEEE 2020 International Conference on Acoustics, Speech, and Signal Processing},
  ADDRESS	       = {Barcelona, Spain},
  MONTH		       = "4--8~" # MAY,
  YEAR		       = 2020
}


## Licence
This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 
International License. To view a copy of this license, visit 
http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to 
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
