import numpy as np 
import pandas as pd 
import os
import cv2 as cv
import matplotlib.pyplot as plt
import pytesseract
import numpy as np
import copy
import math
import sys
from Levenshtein import distance
from fuzzywuzzy import fuzz

PATH_TO_MODEL= r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\copier-coller\east_ocr\frozen_east_text_detection.pb"


for dirname, _, filenames in os.walk(r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\copier-coller\image_test_ocr'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# decoding the geometry and scores
def decode(scores, geometry, scoreThresh):
    
    detections = []
    confidences = []

    ############ CHECK DIMENSIONS AND SHAPES OF geometry AND scores ############
    assert len(scores.shape) == 4, "Incorrect dimensions of scores"
    assert len(geometry.shape) == 4, "Incorrect dimensions of geometry"
    assert scores.shape[0] == 1, "Invalid dimensions of scores"
    assert geometry.shape[0] == 1, "Invalid dimensions of geometry"
    assert scores.shape[1] == 1, "Invalid dimensions of scores"
    assert geometry.shape[1] == 5, "Invalid dimensions of geometry"
    assert scores.shape[2] == geometry.shape[2], "Invalid dimensions of scores and geometry"
    assert scores.shape[3] == geometry.shape[3], "Invalid dimensions of scores and geometry"
    height = scores.shape[2]
    width = scores.shape[3]
    for y in range(0, height):

        # Extract data from scores
        scoresData = scores[0][0][y]
        x0_data = geometry[0][0][y]
        x1_data = geometry[0][1][y]
        x2_data = geometry[0][2][y]
        x3_data = geometry[0][3][y]
        anglesData = geometry[0][4][y]
        for x in range(0, width):
            score = scoresData[x]

            # If score is lower than threshold score, move to next x
            if (score < scoreThresh):
                continue

            # Calculate offset
            offsetX = x * 4.0
            offsetY = y * 4.0
            angle = anglesData[x]

            # Calculate cos and sin of angle
            cosA = math.cos(angle)
            sinA = math.sin(angle)
            h = x0_data[x] + x2_data[x]
            w = x1_data[x] + x3_data[x]

            # Calculate offset
            offset = (
                [offsetX + cosA * x1_data[x] + sinA * x2_data[x], offsetY - sinA * x1_data[x] + cosA * x2_data[x]])

            # Find points for rectangle/bounding box
            p1 = (-sinA * h + offset[0], -cosA * h + offset[1])
            p3 = (-cosA * w + offset[0], sinA * w + offset[1])
            center = (0.5 * (p1[0] + p3[0]), 0.5 * (p1[1] + p3[1]))
            detections.append((center, (w, h), -1 * angle * 180.0 / math.pi))
            confidences.append(float(score))

    # Return detections and confidences
    return [detections, confidences]


# get text bounding boxes
def get_EAST_regions(image):
    text_region_width = 1000
    confThreshold = 0.5
    nmsThreshold = 0.2
    inpWidth = 1600
    inpHeight = 1280
    model = PATH_TO_MODEL
    net = cv.dnn.readNet(model)
    outNames = []
    outNames.append("feature_fusion/Conv_7/Sigmoid")
    outNames.append("feature_fusion/concat_3")
    image = image.astype(np.uint8)
    height_ = image.shape[0]
    width_ = image.shape[1]
    rW = width_ / float(inpWidth)
    rH = height_ / float(inpHeight)

    
    blob = cv.dnn.blobFromImage(image, 1.0, (inpWidth, inpHeight))
    # Run the model
    net.setInput(blob)
    outs = net.forward(outNames)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())

    # Get scores and geometry
    scores = outs[0]
    geometry = outs[1]
    [boxes, confidences] = decode(scores, geometry, confThreshold)
    f_boxes = []
    # Apply NMS
    indices = cv.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        # get 4 corners of the rotated rect
        vertices = cv.boxPoints(boxes[i])
        # scale the bounding box coordinates based on the respective ratios
        for j in range(4):
            vertices[j][0] *= rW
            vertices[j][1] *= rH
        f_boxes.append(vertices)

    return f_boxes


# draw_detected_bounding_boxes
def draw_detected_bounding_boxes(image, east_boxes):
    #     fig, ax = plt.subplots(figsize=(25, 20))
    points_x = []
    points_y = []
    for box in east_boxes:
        x, y, w, h = cv.boundingRect(box)
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    plt.imshow(image)
    plt.title("regions detected by EAST method")
    plt.show()


# returns the bounding box containing all the previously detected bounding boxes 
def detect_text_region(image):
    east_boxes = get_EAST_regions(image)
    clone_img = copy.copy(image)
    draw_detected_bounding_boxes(clone_img, east_boxes)

    points_x = []
    points_y = []
    for box in east_boxes:
        x, y, w, h = cv.boundingRect(box)
        points_x.append(x)
        points_y.append(y)
        points_x.append(x + w)
        points_y.append(y + h)
    pad = 10
    x_min, y_min, x_max, y_max = min(points_x) - pad, min(points_y) - pad, max(points_x) + pad, max(points_y) + pad
    # show text region in a blue rectangle
    cv.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)
    plt.imshow(image)
    plt.title("a box containing all the detected boxes")
    plt.show()

    return x_min, y_min, x_max, y_max


# recognize text using pytesseract
def recognize_image(image):
     # Apply additional preprocessing to improve OCR accuracy
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    thresholded = cv.threshold(blurred, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    lines = pytesseract.image_to_string(image, lang='eng', config="--oem 1 --psm 6").split("\n")
    return lines

# main method
def run_ocr(image_path, ground_truth_lines, output_file):
    # Redirect standard output to a file
    original_stdout = sys.stdout
    with open(output_file, 'w') as file:
        sys.stdout = file

        image = cv.imread(image_path)
        if image is not None:
            image = image[:, :, ::-1]
            image = image.astype(np.uint8)
            h, w, d = image.shape

            # detect text region
            x_min, y_min, x_max, y_max = detect_text_region(image)

            # crop image to pass only text region to tesseract
            text_region = image[y_min:y_max, x_min:x_max]
            plt.imshow(text_region)
            plt.title("only text region")
            plt.show()

            # recognize image
            recognized_lines = recognize_image(text_region)

            # Print recognized text to console
            print("-----------recognized text------------")
            for line in recognized_lines:
                print(line)
            print("--------------------------------------")

    # Restore standard output
    sys.stdout = original_stdout

    # Continue with the rest of the processing
    # Compare recognized text with ground truth
    correct_chars = sum(len(set(rec_line) & set(gt_line)) for rec_line, gt_line in zip(recognized_lines, ground_truth_lines))
    total_chars = sum(len(gt_line) for gt_line in ground_truth_lines)
    accuracy = correct_chars / total_chars

    # Calculate WER, CER, and similarity ratio
    recognized_text = ' '.join(recognized_lines)
    ground_truth_text = ' '.join(ground_truth_lines)
    wer = distance(ground_truth_text.split(), recognized_text.split()) / max(len(ground_truth_text.split()), (len(recognized_text.split())))
    cer = distance(ground_truth_text, recognized_text) / max(len(ground_truth_text), len(recognized_text))
    similarity_ratio = fuzz.ratio(recognized_text, ground_truth_text)

    # Print or use the metrics as needed
    print(f"Word Error Rate (WER): {wer}")
    print(f"Character Error Rate (CER): {cer}")
    print(f"Similarity Ratio: {similarity_ratio}%")

if __name__ == "__main__":
    file = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\copier-coller\image_test_ocr\11blur.png"
    output_file = r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\copier-coller\image_test_ocr\output\output.txt"
    
    # Define ground truth lines
    ground_truth_lines = [
        "Jan 2022 - Aug 2022: Real Estate Specialist at Free G Company"
        "• Handled direct sales inbound/outbound calls for real estate staff."
        "• Organized meetings between customers and client’s representatives."
        "• Set plans for marketing issues."
        "Languages:"
        "• English (very good and conversational)"
        "• Arabic (native)"
        "Strengths:"
        "Course Completion"
        "• C++"
        "• Java"
        "• JavaScript"
        "• Oracle SQL Database"
        "• Computer Architecture"
        "• Data Analytics"
        "• Data Mining"
    ]

    run_ocr(file, ground_truth_lines, output_file)
