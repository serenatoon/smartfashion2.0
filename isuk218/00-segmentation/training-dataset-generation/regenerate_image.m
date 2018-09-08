% This script is intended to regenerate the nth image from the 'data' matrix
% where n = the index of the image of interest in the dataset
% The purpose is to ease checking of the correct image conversion and
% storing
% Author: Ira Sukimin (isuk218@aucklanduni.ac.nz)

% Clear Command Window ONLY (Workspace should be retained)
clc

% Change value based on the index. Should not exceed the 'total_images'
% initialisation in dataset_generator.m
image_index = 56;

% Size of photo should correspond to the initialisation made in
% dataset_generator.m
size_of_photo = 200;

% Select row of interest based on the index
X = data(image_index,:);
% Reshape into a size_of_photo by size_of_photo matrix
Y = reshape(X,[200,200]);
% Display the reshaped matrix
imshow(Y);