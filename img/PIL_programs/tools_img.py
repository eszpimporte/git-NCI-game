import PIL
import PIL.Image
import time
t1 = time.time()

#Create
feuille = PIL.Image.new("RGB",(256,256),(255,255,255))
size = 256
black_color = (0,0,0)

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

for x in range(size):
        for y in range(size):
            if x % 32 == 0 or y % 32 == 0:
                feuille.putpixel((x,y),black_color)


#Saving
feuille.save("./img/assets/tiles_set/base_tiles_set_8_by_8.png")
t2 = time.time()
print(f"Job done in {t2 - t1} seconds")