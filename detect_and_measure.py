import urllib

import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np


# noinspection PyUnresolvedReferences
def url_to_array(url):
    req = urllib.request.urlopen(url)
    arr = np.array(bytearray(req.read()), dtype=np.int8)
    arr = cv2.imdecode(arr, -1)
    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return arr


# noinspection PyUnresolvedReferences
def file_to_array(filepath):
    arr = cv2.imread(filepath)
    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return arr


# noinspection PyUnresolvedReferences,PyUnboundLocalVariable
def detect_and_measure(filepath, multiplier):
    # photo_as_array = url_to_array('https://b2cfurniture.com.au/pub/media/catalog/product/cache/3fb871f48f7af5e44260f2d9fd3932a9/e/l/elm-modern-hardwood-dining-chair-black-hardwood-frame-eco-friendly-beige-fabric_3_.jpg')
    photo_as_array = file_to_array(filepath)
    mp_objectron = mp.solutions.objectron
    mp_drawing = mp.solutions.drawing_utils
    # Instantiation
    objectron = mp_objectron.Objectron(
        static_image_mode=True,
        max_num_objects=5,
        min_detection_confidence=0.2,
        model_name='Chair')

    # Inference
    results = objectron.process(photo_as_array)

    if not results.detected_objects:
        print(f'No box landmarks detected.')

    # Copy image so as not to draw on the original one
    annotated_image = photo_as_array.copy()
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
    output_path = 'static/detected_cargo.jpg'
    cv2.imwrite(output_path, annotated_image)

    return get_sizes(detected_object.landmarks_3d, multiplier)


def get_sizes(landmarks_3d, multiplier):
    # Convert landmarks to numpy array
    landmarks_3d_np = np.array([[lm.x, lm.y, lm.z] for lm in landmarks_3d.landmark])

    # Calculate distances between opposite corners of the box
    width = np.linalg.norm(landmarks_3d_np[1] - landmarks_3d_np[5]) * multiplier
    length = np.linalg.norm(landmarks_3d_np[2] - landmarks_3d_np[6]) * multiplier
    height = np.linalg.norm(landmarks_3d_np[4] - landmarks_3d_np[8]) * multiplier
    volume = width * length * height

    return width, length, height, volume
