#Demonstration of using draw commands to draw simple shapes using wghs.

from pygame_functions import *

screenSize(400,400)
setBackgroundColour("white")

drawEllipse(200,200,350,350,"lightblue")

drawRect(100,100,200,200,"darkgreen", 3)

drawTriangle(150,150,180,150,165,180,"red") #  You can use an HTML color name

drawTriangle(220,150,250,150,235,180,[255,100,50]) # or use an RGB colour definition

drawPolygon([ (110,250) , (290,250) , (280,220), (120,220) ], "sienna" )  # note the pairs of coordinates within the point list.



endWait()