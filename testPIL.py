# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 11:07:51 2020

@author: andmra2
"""


from PIL import Image as PILImage
from io import BytesIO

fp = r'\\corp.hidria.com\aet\SI-TO-Izmenjava\Andrej_Mrak\__Nove_Meritve\TC\F-784_11V_181217\TCRTG\1F.jpg'
im = PILImage.open(fp)
im1 = im.crop((0, 0, 1000, 750))
im1.load()
im1.show()
#im = im.resize((173, 130), PILImage.ANTIALIAS)
memfile = BytesIO()