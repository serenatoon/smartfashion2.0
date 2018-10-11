% This script is intended to run through the leather and 
% wool images (in jpg and png formats respectively) files in the 
% current directory, convert them into grayscale and store the RGB
% value for each pixel in an array.
% The array for each image is stored in a 2d matrix called 'data'
% (i.e each column corresponds to one image)
% Labels corresponding to the each of the index of the images are assigned 
% to an array called 'label'
% To create the .mat dataset for LR script, select "label" and "data" in
% the workspace and click "Save As", rename appropriately.
% Author: Ira Sukimin (isuk218@aucklanduni.ac.nz)

% Clear Command Window and Workspace
clc
clear

% Intialisation
num_of_images_per_material = 50;
total_images = 2*num_of_images_per_material;
size_of_photo = 400; % in pixels
data = zeros(size_of_photo*size_of_photo,total_images); 
mldata_descr_ordering = {'label', 'data'}; % create key for dataset

for k = 1:total_images
    
    % Loop through total_images files, reads them to image_data and assigns
    % an indexed label based on the type of material
    if k <= num_of_images_per_material
        file_name = strcat('init/leather (', num2str(k), ').png');
        if exist(file_name, 'file')
            image_data = imread(file_name);
            label(1,k) = 1; %1 represents leather
            fprintf('processing %s file\n', file_name);
        else
            fprintf('File %s does not exist.\n', file_name);
        end
    else
        m = k - num_of_images_per_material;
        file_name = strcat('init/wool (', num2str(m), ').png');
        if exist(file_name, 'file')
            image_data = imread(file_name);
            label(1,k) = 0; %0 represents wool
            fprintf('processing %s file\n', file_name);
        else
            fprintf('File %s does not exist.\n', file_name);
        end
    end
    
    C = rgb2gray(image_data);
    
    for col = 1:size_of_photo
        for row = 1:size_of_photo
            index = (col-1)*size_of_photo + row;
            data(index,k) = C(row,col); 
        end
    end	
end

data = uint8(data);
data = transpose(data);

% fprintf('pixel col: %d pixel row: %d processed \n', row,col);
% https://au.mathworks.com/help/images/ref/im2bw.html?requestedDomain=true#bt56tsr
% https://blogs.mathworks.com/steve/2016/05/16/image-binarization-new-r2016a-functions/