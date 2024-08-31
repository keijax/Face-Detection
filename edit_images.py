import cv2
import os

output_path = 'WillSmith/'
resized_path = 'will/'

target_size = (256, 256) 

def resize_image(image_path, output_path, size):
    img = cv2.imread(image_path)
    resized_img = cv2.resize(img, size)
    cv2.imwrite(output_path, resized_img)
    print(f"Saved resized image to {output_path}")

counter = 1
for file_name in os.listdir(output_path):
    str = ""
    if counter < 10:
        str = f"person4_00{counter}.jpg"
    elif 10<=counter<=99:
        str = f"person4_0{counter}.jpg"
    else:
        str = f"person4_{counter}.jpg"
    image_path = os.path.join(output_path, file_name)
    output_file = os.path.join(resized_path, str)
    resize_image(image_path, output_file, target_size)
    counter = counter+1