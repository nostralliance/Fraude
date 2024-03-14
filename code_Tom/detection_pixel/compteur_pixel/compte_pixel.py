from PIL import Image

img = Image.open(r"C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\compteur_pixel\test_floue.png")
count_white = 0
count_autre = 0

list_pixel = []
list_pixel_autre = []
for y in range(img.height):
    for x in range (img.width):
        pixel = img.getpixel((x, y))
        list_pixel.append(pixel)
        # if pixel == (255, 255, 255) and (240, 240, 240):
        if (220 <= pixel[0] <= 255) and (220 <= pixel[1] <= 255) and (220 <= pixel[2] <= 255):
            count_white += 1
        elif pixel != (255, 255, 255):
            list_pixel_autre.append(pixel)
            count_autre += 1

with open(r'C:\Users\pierrontl\OneDrive - GIE SIMA\Documents\GitHub\Fraude\code_Tom\detection_pixel\compteur_pixel\data_floue.txt', 'w')as f:
    for item in list_pixel_autre:
        f.write(f'{item}\n')
print("done")


res_add = count_white + count_autre # Permet de connaitre le niveau de blanc
res_pourcentage = (count_white/res_add)*100

print("nombre pixel blanc :",count_white)
print("Nombre pixel différents de blanc :", count_autre)
print("pourcentage de pixel blanc :",res_pourcentage)
print("liste de pixel pour connaitre la valeur :", list_pixel_autre[0])
print("liste de pixel pour connaitre la longueur :", len(list_pixel_autre))