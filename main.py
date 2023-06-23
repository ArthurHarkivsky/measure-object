import mediapipe as mp

import cv2
import numpy as np
import matplotlib.pyplot as plt
import urllib


def url_to_array(url):
    req = urllib.request.urlopen(url)
    arr = np.array(bytearray(req.read()), dtype=np.int8)
    arr = cv2.imdecode(arr, -1)
    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return arr


mug = 'https://goodstock.photos/wp-content/uploads/2018/01/Laptop-Coffee-Mug-on-Table.jpg'
mug = url_to_array(mug)
mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils
# Instantiation
objectron = mp_objectron.Objectron(
    static_image_mode=True,
    max_num_objects=5,
    min_detection_confidence=0.2,
    model_name='Cup')

# Inference
results = objectron.process(mug)

if not results.detected_objects:
    print(f'No box landmarks detected.')

# Copy image so as not to draw on the original one
annotated_image = mug.copy()
for detected_object in results.detected_objects:
    # Draw landmarks
    mp_drawing.draw_landmarks(annotated_image,
                              detected_object.landmarks_2d,
                              mp_objectron.BOX_CONNECTIONS)

    # Draw axis based on rotation and translation
    mp_drawing.draw_axis(annotated_image,
                         detected_object.rotation,
                         detected_object.translation)

# Plot result
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(annotated_image)
ax.axis('off')
print(f'Output photo resolution: {annotated_image.shape[1]} x {annotated_image.shape[0]} pixels')


def get_volume(landmarks_3d):
    # Convert landmarks to numpy array
    landmarks_3d = np.array([[lm.x, lm.y, lm.z] for lm in landmarks_3d.landmark])

    # Calculate distances between opposite corners of the box
    d1 = np.linalg.norm(landmarks_3d[1] - landmarks_3d[5])
    d2 = np.linalg.norm(landmarks_3d[2] - landmarks_3d[6])
    d3 = np.linalg.norm(landmarks_3d[4] - landmarks_3d[8])
    # Calculate volume as product of distances
    volume = d1 * d2 * d3
    return volume


def get_size(landmarks_3d):
    # Convert landmarks to numpy array
    landmarks_3d = np.array([[lm.x, lm.y, lm.z] for lm in landmarks_3d.landmark])
    # Calculate distances between opposite corners of the box
    width = np.linalg.norm(landmarks_3d[1] - landmarks_3d[5])
    length = np.linalg.norm(landmarks_3d[2] - landmarks_3d[6])
    height = np.linalg.norm(landmarks_3d[4] - landmarks_3d[8])
    return width, length, height


print(
    f'Volume of detected object: {get_volume(detected_object.landmarks_3d):.4f} m^3 or {get_volume(detected_object.landmarks_3d) * 35.3147:.4f} ft^3')
print(
    f'Size of detected object: {get_size(detected_object.landmarks_3d)[0]:.4f} m x {get_size(detected_object.landmarks_3d)[1]:.4f} m x {get_size(detected_object.landmarks_3d)[2]:.4f} m or {get_size(detected_object.landmarks_3d)[0] * 100:.4f} cm x {get_size(detected_object.landmarks_3d)[1] * 100:.4f} cm x {get_size(detected_object.landmarks_3d)[2] * 100:.4f} cm')
# plt.show()
