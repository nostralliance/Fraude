import cv2
import pytesseract

img = cv2.imread(r'C:\Users\pierrontl\Documents\code_python\essaie_2.png')


h,w,c = img.shape
print(c)


boxes = pytesseract.image_to_boxes(img)
print(boxes)

#lien youtube pour tesseract https://www.youtube.com/watch?v=4uWp6dS6_G4, https://www.youtube.com/watch?v=89m89vVh4wg&list=PL2VXyKi-KpYuTAZz__9KVl1jQz74bDG7i&index=2