s1 = "Carrefour Cairo, Maddi branch Product name Price Qty Total El-Doha Rice 4-Kilo 160LE 1 160 Crystal corn-oil 1-Liter 80LE 3 240 Juhayna yogurt 200-gram 495LE 8 396 El-Malekah macaroni 300-gram 695LE 7 48.65 Sun-light shower gel 3-Liter 95LE 1 95 Fern butter 650-Gram 56 LE 1 56 Heinz Ketchup 400-Gram 34LE 1 34 Black pepper 100-Gram 38LE 1 38 Himalaya salt 350-Gram SOLE 1 50 Barka water 1.5-Liter 65LE 20 130 Basma Bamya 400-Gram 48 LE 2 96 chicken breast 1-Kilo 155LE 3 465 Turkey cheese 250-Gram 44LE 4 176 1628.25 Date: May 25, 2023"

l=["El-Doha Rice 4-Kilo",
"Crystal corn-oil 1-Liter",
"Juhayna yogurt 200-gram",
"El-Malekah macaroni 300-gram",
"Sun-light shower gel 3-Liter",
"Fern butter 650-Gram",
"Heinz Ketchup 400-Gram",
"Black pepper 100-Gram",
"Himalaya salt 350-Gram",
"Barka water 1.5-Liter",
"Basma Bamya 400-Gram",
"chicken breast 1-Kilo",
"Turkey cheese 250-Gram",
"betengan"

]


for i in l:
    s = s1.find(i)
    if s!= -1:
        for x in range(0,999):
            if s1[s+x]=="L" and s1[s+x+1]=="E":
                # print(s1[s+x])
                # print(s+x)
                lens = len(i)
                # print(lens+s)
                print(i)
                print(s1[lens+s:s+x])
                break;



