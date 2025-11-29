import PIL
import PIL.Image
import time
t1 = time.time()
print("lunched")

#Create
# feuille = PIL.Image.new("RGB",(256,256),(255,255,255))
# size = 256
# black_color = (0,0,0)

feuille = PIL.Image.open("./img/assets/background/mainfondlight.jpg")

def plateau():
    #Nb cases
    nb_case = int(input("Nombre de case ? : "))


    #Size // by nb_case
    size = feuille.size[0]//nb_case * nb_case
    feuille.resize((size,size))

    #Caractères pour les cases
    size_case = int(size/nb_case)
    color1 = (200,200,255)
    color2 = (100,100,255)

    #Painting
    for x in range(size):
        for y in range(size):
            if (x//size_case + y//size_case) % 2 == 0:
                feuille.putpixel((x,y),color1)
            else:
                feuille.putpixel((x,y),color2)

def green_blue_teinte():
    for x in range(feuille.size[0]):
            for y in range(feuille.size[1]):
                pix = feuille.getpixel((x,y))
                feuille.putpixel((x,y),(min(255,pix[0]),min(255, pix[1]*5),min(255, pix[2]*3)))

for x in range(feuille.size[0]):
    for y in range(feuille.size[1]):
        pix = feuille.getpixel((x,y))
        if y < 500:
            feuille.putpixel((x,y),(max(255-round(y/2),0),round(pix[1]/max((2-y/200),1)),round(pix[2]/max(2-y/200,1))))
        else:
            feuille.putpixel((x,y),(pix[0],pix[1],pix[2]))

#Saving
file_name = str(input("Quel nom pr le ficher : _"))
feuille.save(file_name, "png")
t2 = time.time()
print(f"Job done in {t2 - t1} seconds")