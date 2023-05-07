![Musical Notes](https://user-images.githubusercontent.com/61359702/236662285-7245844d-e9e3-46a6-87a4-a0b45de7bf15.PNG)

# About Project
Musical Note Reader is a Python project that uses optical music recognition (OMR) technology to extract musical notes from digital images of sheet music. The project uses libraries such as numpy, skimage, matplotlib and scipy. The project includes a classifier that is trained on a set of musical notes to accurately identify and classify the notes found in the uploaded images.

## What I learned

 - Image processing techniques
 - Working with python
 - Numpy and Scipy
 - Scikit-mage package
 - Working with images in python
 - Edge detection
 - Convolution
 - Image histograms
 - Image segmentation
 - Hough transform
 - Feature extraction


# Notes recognition pipeline
The image goes through a pipeline of processing in order to extract and identify musical notes. Here is a brief rundown of the pipeline.

Original input image:
![Original input image](https://user-images.githubusercontent.com/61359702/236663042-61bfb030-cafb-40c7-bd0e-02756a704496.jpg)


1. Preprocessing  
    a. Converting image to binary
    ![Binarized image](https://user-images.githubusercontent.com/61359702/236663714-ddbabd9d-5346-48af-8f1e-984ce238c1a4.png)
    b. Inverting image
    ![Inverted image](https://user-images.githubusercontent.com/61359702/236663894-a2249ee8-8aea-4d55-8eb3-502be94752e3.png)
    c. Deskew image
    ![Deskewed image](https://user-images.githubusercontent.com/61359702/236663947-81e8286a-3e89-4cba-a80e-82dcb73746f5.png)
    d. Identify staff lines
    ![Staff lines](https://user-images.githubusercontent.com/61359702/236664792-02e4fdb9-5e0e-4dd3-ae3f-98f232a95d96.png)
    e. Remove staff lines
    ![Staff lines removed](https://user-images.githubusercontent.com/61359702/236665346-1ad56a7d-480d-456a-a23a-363789c80f1f.png)
2. Partition image into staffs
![One staff](https://user-images.githubusercontent.com/61359702/236665522-b9b30cd8-c59b-4aca-af98-e2e244ccc06d.png)
3. Segment staffs into notes
![Segmented musical notes](https://user-images.githubusercontent.com/61359702/236665875-b732e6e1-da53-4836-80e1-3dd4aa2da9c4.png)
4. Normalize notes into 100x100 blocks
![Normalized musical notes](https://user-images.githubusercontent.com/61359702/236666105-0ae83f6c-10c1-4bd3-8eab-603b41c623c4.png)
5. Classify notes  
    a. Calculate histogram of note  
    b. Compare with histograms of all other notes in pretrained model  
    c. Identify closest match
6. Output staffs and notes to file
![Output text file](https://user-images.githubusercontent.com/61359702/236666922-e95a0e06-b45c-4d75-81e8-42bdd4c624cb.png)

# Limitations
 - Connected notes are misclassified as the model was not trained on them.  
 ![Connected notes](https://user-images.githubusercontent.com/61359702/236667243-9f09d835-6cc4-419e-b6b0-7f69a855b632.png)
 - Notes that are close to each other and overlap in the x-axis are misclassified because they are segmented as one note.  
 ![Overlapping notes](https://user-images.githubusercontent.com/61359702/236667430-18563f9a-7607-40df-931e-c0bab60e613a.png)
 - Errors in preprocessing can cause notes like this:  
 ![Example error note](https://user-images.githubusercontent.com/61359702/236667752-28f6084d-d9ba-4c3a-849c-66c82d051186.png)  
 to have disconnects in x-axis, causing it to be regarded as 2 separate notes.  
 ![Two separate notes](https://user-images.githubusercontent.com/61359702/236667905-c4e6d95e-0ebf-4b6c-acb3-8c32f80f0dee.png)

# Installation instructions
1. Clone the repository by running the following command in your terminal or command prompt:
   ```shell
   git clone https://github.com/ziadabdo98/Musical-Notes-Reader.git MusicalNotesReader
   ```
2. Run the script main.py using python3 with the first argument as the folder containing the images, and the second argument as the folder to output the text files 
   ```shell
   python main.py test-cases output
   ```