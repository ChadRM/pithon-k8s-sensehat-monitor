#!/usr/bin/env python

import colorsys
import math
import time
from sys import exit
import socket

try:
     from PIL import Image, ImageDraw, ImageFont
except ImportError:
     exit("This script requires pillow module!")

import unicornhathd

width, height = unicornhathd.get_shape()

img = Image.open('k8s-logo.png')

print("""Unicorn HAT HD: demo.py

This pixel shading demo transitions between 4 classic graphics demo effects.

Press Ctrl+C to exit!

""")

unicornhathd.rotation(270)
unicornhathd.brightness(0.6)
u_width, u_height = unicornhathd.get_shape()
showing_ip = False
ip_start_at = 0

# Generate a lookup table for 8bit hue to RGB conversion
hue_to_rgb = []

for i in range(0, 255):
    hue_to_rgb.append(colorsys.hsv_to_rgb(i / 255.0, 1, 1))

# Get IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
my_ip = s.getsockname()[0]
s.close()

#create image of ip address

colors = (255,255,250)
font_file = '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf'
font_size = 12
font = ImageFont.truetype(font_file, font_size)
w, h = font.getsize(my_ip)
text_x, text_y = width, 0
text_width, text_height = width, 0
text_width += w + width                # add some padding so the ip scrolls$
text_height = max(text_height, h, 16)  # no more than the size of the unico$
image = Image.new('RGB', (text_width, text_height), (0, 0, 0))
draw = ImageDraw.Draw(image)
draw.text((text_x, text_y), my_ip, colors, font=font)
# Also, remember that this only creates the base image
# The function finds the appropriate pixel to map to the display
# this is great, but to map to the screen... ugh...
# image is:
#
#  123
#  456
#  789
#
# I need:
#
#  147
#  258
#  369

def gradient(x, y, step):
    g = x * 16
    b = y * 16
    r = 255 - (x * 16)
    return (r, g, b)


# twisty swirly goodness
def swirl(x, y, step):
    x -= (u_width / 2)
    y -= (u_height / 2)
    dist = math.sqrt(pow(x, 2) + pow(y, 2)) / 2.0
    angle = (step / 10.0) + (dist * 1.5)
    s = math.sin(angle)
    c = math.cos(angle)
    xs = x * c - y * s
    ys = x * s + y * c
    r = abs(xs + ys)
    r = r * 12.0
    r -= 20
    return (r, r + (s * 130), r + (c * 130))


# roto-zooming checker board
def checker(x, y, step):
    x -= (u_width / 2)
    y -= (u_height / 2)
    angle = (step / 10.0)
    s = math.sin(angle)
    c = math.cos(angle)
    xs = x * c - y * s
    ys = x * s + y * c
    xs -= math.sin(step / 200.0) * 40.0
    ys -= math.cos(step / 200.0) * 40.0
    scale = step % 20
    scale /= 20
    scale = (math.sin(step / 50.0) / 8.0) + 0.25
    xs *= scale
    ys *= scale
    xo = abs(xs) - int(abs(xs))
    yo = abs(ys) - int(abs(ys))
    v = 0 if (math.floor(xs) + math.floor(ys)) % 2 else 1 if xo > .1 and yo > .1 else .5
    r, g, b = hue_to_rgb[step % 255]
    return (r * (v * 255), g * (v * 255), b * (v * 255))


# weeee waaaah
def blues_and_twos(x, y, step):
    x -= (u_width / 2)
    y -= (u_height / 2)
    scale = math.sin(step / 6.0) / 1.5
    r = math.sin((x * scale) / 1.0) + math.cos((y * scale) / 1.0)
    b = math.sin(x * scale / 2.0) + math.cos(y * scale / 2.0)
    g = r - .8
    g = 0 if g < 0 else g
    b -= r
    b /= 1.4
    return (r * 255, (b + g) * 255, g * 255)


# rainbow search spotlights
def rainbow_search(x, y, step):
    xs = math.sin((step) / 100.0) * 20.0
    ys = math.cos((step) / 100.0) * 20.0
    scale = ((math.sin(step / 60.0) + 1.0) / 5.0) + 0.2
    r = math.sin((x + xs) * scale) + math.cos((y + xs) * scale)
    g = math.sin((x + xs) * scale) + math.cos((y + ys) * scale)
    b = math.sin((x + ys) * scale) + math.cos((y + ys) * scale)
    return (r * 255, g * 255, b * 255)


# zoom tunnel
def tunnel(x, y, step):
    speed = step / 100.0
    x -= (u_width / 2)
    y -= (u_height / 2)
    xo = math.sin(step / 27.0) * 2
    yo = math.cos(step / 18.0) * 2
    x += xo
    y += yo
    if y == 0:
        if x < 0:
            angle = -(math.pi / 2)
        else:
            angle = (math.pi / 2)
    else:
        angle = math.atan(x / y)
    if y > 0:
        angle += math.pi
    angle /= 2 * math.pi  # convert angle to 0...1 range
    hyp = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
    shade = hyp / 2.1
    shade = 1 if shade > 1 else shade
    angle += speed
    depth = speed + (hyp / 10)
    col1 = hue_to_rgb[step % 255]
    col1 = (col1[0] * 0.8, col1[1] * 0.8, col1[2] * 0.8)
    col2 = hue_to_rgb[step % 255]
    col2 = (col2[0] * 0.3, col2[1] * 0.3, col2[2] * 0.3)
    col = col1 if int(abs(angle * 6.0)) % 2 == 0 else col2
    td = .3 if int(abs(depth * 3.0)) % 2 == 0 else 0
    col = (col[0] + td, col[1] + td, col[2] + td)
    col = (col[0] * shade, col[1] * shade, col[2] * shade)
    return (col[0] * 255, col[1] * 255, col[2] * 255)

def d2iq_logo(x, y, step):
    logo = [
      (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      (0,0,1,1,1,1,0,0,0,0,1,1,1,0,0,0),
      (0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0),
      (0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0),
      (0,0,1,0,0,0,1,0,0,0,1,1,0,0,0,0),
      (0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0),
      (0,0,1,1,1,1,0,0,0,1,1,1,1,1,0,0),
      (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      (0,0,1,1,1,1,1,0,0,0,1,1,1,0,0,0),
      (0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0),
      (0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0),
      (0,0,0,0,1,0,0,0,0,1,0,1,0,1,0,0),
      (0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0),
      (0,0,1,1,1,1,1,0,0,0,1,1,1,1,0,0),
      (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0) 
    ]
    if logo[x][y] == 1:
      return (255,255,255)
    else:
     return (51,0,114)

def k8s_logo(x, y, step):
     pixel = img.getpixel((x, y))

     r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
     if r or g or b:
          return(r,g,b)
     else:
          return(0,0,0)

def current_milli_time():
    return int(round(time.time() * 1000))

def show_IP(x, y, step):
     global showing_ip
     global ip_start_at
     global image
     if showing_ip == False:
          showing_ip = True
          ip_start_at = step
     if (int((step - ip_start_at)/2) + x) >= text_width:
         ip_start_at = step
         scroll_loc = x
     else:
         scroll_loc = (int((step - ip_start_at)/2) + x)
     pixel = image.getpixel((scroll_loc, y))
     r, g, b = [int(n) for n in pixel]
     return (r, g, b)


effects = [gradient, tunnel, show_IP, rainbow_search, checker, k8s_logo, swirl, d2iq_logo]


step = 0

try:
    while True:
        for i in range(125):
            start = current_milli_time()
            for y in range(u_height):
                for x in range(u_width):
                    r, g, b = effects[0](x, y, step)
                    if i > 100:
                        r2, g2, b2 = effects[-1](x, y, step)
                        ratio = (125.00 - i) / 25.0
                        r = r * ratio + r2 * (1.0 - ratio)
                        g = g * ratio + g2 * (1.0 - ratio)
                        b = b * ratio + b2 * (1.0 - ratio)
                    r = int(max(0, min(255, r)))
                    g = int(max(0, min(255, g)))
                    b = int(max(0, min(255, b)))
                    unicornhathd.set_pixel(x, y, r, g, b)

            step += 2
            unicornhathd.show()

        effect = effects.pop()
        effects.insert(0, effect)

except KeyboardInterrupt:
    unicornhathd.off()
