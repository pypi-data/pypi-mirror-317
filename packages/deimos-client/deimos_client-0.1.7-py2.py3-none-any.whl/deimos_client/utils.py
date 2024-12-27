import os
os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2

def encode_image(image, encode_type='.png'):
    if encode_type == '.jpg':
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
        is_success, im_buf_arr = cv2.imencode(encode_type, image, img_param)
    elif encode_type == '.webp':
        img_param = [int(cv2.IMWRITE_WEBP_QUALITY), 80]
        is_success, im_buf_arr = cv2.imencode(encode_type, image, img_param)
    else:
        is_success, im_buf_arr = cv2.imencode(encode_type, image)
    return im_buf_arr.tobytes()

def get_job_type(routing_key):
        return '.'.join(routing_key.split('.')[:2])