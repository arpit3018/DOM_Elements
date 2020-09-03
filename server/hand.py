import sys
import numpy as np
import cv2
import tensorflow as tf

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

PATH_TO_FROZEN_GRAPH = 'model_exported/frozen_inference_graph.pb'
PATH_TO_LABELS = 'data/egohands_label_map.pbtxt'
OUTPUT_PATH = 'detection_output.jpg'

def detect_image(img):
# load label map
category_index = label_map_util.create_category_index_from_labelmap(
PATH_TO_LABELS)
# load detection graph
detection_graph = tf.Graph()
with detection_graph.as_default():
od_graph_def = tf.GraphDef()
with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
serialized_graph = fid.read()
od_graph_def.ParseFromString(serialized_graph)
tf.import_graph_def(od_graph_def, name='')
# define input/output tensors
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')
# load input image
if img is None:
sys.exit('failed to load image: %s' % image_path)
img = img[..., ::-1] # BGR to RGB
# run inference
with detection_graph.as_default():
with tf.Session() as sess:
boxes, scores, classes, _ = sess.run(
[detection_boxes, detection_scores, detection_classes, num_detections],
feed_dict={image_tensor: np.expand_dims(img, 0)})
# draw the results of the detection
vis_util.visualize_boxes_and_labels_on_image_array(
img,
np.squeeze(boxes),
np.squeeze(classes).astype(np.int32),
np.squeeze(scores),
category_index,
use_normalized_coordinates=True,
line_thickness=6,
min_score_thresh=0.3)
img = img[..., ::-1] # RGB to BGR
return img

def main():
cap = cv2.VideoCapture(0)
while True :
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
img = detect_image(frame)
cv2.namedWindow('hand_detection', cv2.WINDOW_NORMAL)
cv2.imshow('hand_detection', img)
if cv2.waitKey(1) & 0xFF == ord('q'):
break
cap.release()
cv2.destroyAllWindows()

if __name__ == '__main__':
main()
