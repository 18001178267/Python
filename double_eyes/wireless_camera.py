# -*- coding: utf-8 -*-
"""
@author: Terry n
"""
# Imports
import numpy as np
import os
import sys
import tensorflow as tf
import cv2



# if tf.__version__ < '1.4.0':
#     raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')

os.chdir('C:\\Users\\YFZX\\Desktop\\tensorflow_jupyter\models-master\\research\\object_detection')


# Env setup
# This is needed to display the images.
# %matplotlib inline

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Object detection imports
from utils import label_map_util

from utils import visualization_utils as vis_util

# Model preparation
# What model to download.
#MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'  # [30,21]  best
# MODEL_NAME = 'ssd_inception_v2_coco_2017_11_17'            #[42,24]
# MODEL_NAME = 'faster_rcnn_inception_v2_coco_2017_11_08'         #[58,28]
# MODEL_NAME = 'faster_rcnn_resnet50_coco_2017_11_08'     #[89,30]
# MODEL_NAME = 'faster_rcnn_resnet50_lowproposals_coco_2017_11_08'   #[64, ]
# MODEL_NAME = 'rfcn_resnet101_coco_2017_11_08'    #[106,32]
# MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28'
# MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'
# MODEL_NAME = 'fod_detection'
MODEL_NAME = 'nanjing_detection'


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/1_frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
#PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
PATH_TO_LABELS = os.path.join('data', '1_label_map.pbtxt')


NUM_CLASSES = 1
# NUM_CLASSES = 1
# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    # Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Helper code
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)



# Size, in inches, of the output images.
# IMAGE_SIZE = (12, 8)


with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # the video to be detected, eg, "test.mp4" here
        url = "rtsp://admin:yzwlgzw123@192.168.0.117/h264/ch1/main/av_stream"


        # vidcap = cv2.VideoCapture(0)
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.





        while (True):
            print('1')
            vidcap = cv2.VideoCapture(url)
            ret, image = vidcap.read()
            #frame_width = int(vidcap.get(3))
            #frame_height = int(vidcap.get(4))

            if ret == True:

                # image_np = load_image_into_numpy_array(image)
                image_np = image

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8)
                print(scores)

                cv2.imshow("capture",image_np)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    ret = False
            # Break the loop
            else:
                break
vidcap.release()
cv2.destroyAllWindows()