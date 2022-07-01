##Author: Dan Steingart
##Date Started: 2022-06-29
##Notes: Tidbyt Plot Library

#To DO
# [x] scatter plot
# [x] scaling 
# [x] animations
# [x] text

from PIL import Image, ImageDraw
import requests
import base64
from io import BytesIO
from time import time
import json
from numpy import *

class tidbyt_plot:
    def __init__(self,dev_name,dev_toke):
        self.buffered = BytesIO()
        self.dev_name = dev_name
        self.dev_toke = dev_toke
        self.images = []
        self.im = Image.new('RGB', (64, 32), (0,0,0))
        self.pixels = self.im.load()
        self.renders = []
        self.colors = []
        self.xpix = 64-1
        self.ypix = 32-1
        self.ims = []

    def map_range(self,x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def plot(self,a,b,color):
        out = {}
        out['type'] = 'plot'
        out['x'] = a
        out['y'] = b
        out['color'] = color
        self.renders.append(out)

    def text(self,txt,x,y,color='white'):
        out = {}
        out['type'] = 'text'
        out['position'] = (x,y)
        out['text'] = txt
        out['color'] = color
        self.renders.append(out)


    def render_frame(self,show=False,debug=False):
        self.im = Image.new('RGB', (64, 32), (0,0,0))
        self.pixels = self.im.load()
        self.xs = []
        self.ys = []
        mnx = mny = mxx = mxy = 0
        for out in self.renders:
            if out['type'] == 'plot':
                self.xs.append(out['x'])
                self.ys.append(out['y'])
            flatx = [x for sub in self.xs for x in sub]
            flaty = [y for sub in self.ys for y in sub]
        try:
            mnx =  min(flatx)
            mxx =  max(flatx)
            mny =  min(flaty)
            mxy =  max(flaty)
        except: None

        for out in self.renders:
            if out['type'] == 'plot':
                x = self.map_range(out['x'],mnx,mxx,0,self.xpix)
                y = self.map_range(out['y'],mny,mxy,self.ypix+1,0)
                x = clip(x,0,self.xpix)
                y = clip(y,0,self.ypix)
                for j in range(len(x)): self.pixels[x[j],y[j]] = out['color']
            elif out['type'] == 'text':
                draw = ImageDraw.Draw(self.im)
                draw.multiline_text(out['position'],out['text'],spacing=0,fill=out['color'])
        self.ims.append(self.im.copy())
        self.renders = []

        
    def make_gif(self,show=False,duration=100,loop=0,rev=False):
        these = self.ims
        if rev: these = these+these[-2:1:-1]
        these[0].save(self.buffered, format="GIF",save_all = True, append_images=these[1:], duration=duration,loop=loop)
        img_str = base64.b64encode(self.buffered.getvalue())
        ss = f'data:image/gif;base64,{img_str.decode()}'
        if show: print(f"<img src='{ss}'>")
        return img_str.decode()

    def send_to_tidbyt(self,media,inst,background=False):
        headers = {
            'Content-Type': "application/json",
            'Authorization': f"Bearer {self.dev_toke}"
            }

        url = f"https://api.tidbyt.com/v0/devices/{self.dev_name}/push"

        dd = {}
        dd['image'] = media
        dd['installationID'] = inst
        dd['background'] = background

        payload = json.dumps(dd)
        response = requests.request("POST", url, data=payload, headers=headers)
        return response

if __name__ == "__main__":

    dev_name = "DEVICE_ID"
    dev_toke =  "API_TOKEN"
    tb = tidbyt_plot(dev_name,dev_toke)
    a = linspace(0,1,100)

    mxx = 25
    mmm = 200

    for i in range(0,100,2):
        for j in range(1,mxx):
            b = j*sin(j*.5*a)
            tb.plot(a,b,(255-i-j*mmm//mxx,10,i+j*mmm//mxx))

        tb.text("hello\nworld",16,5,color='white')
        tb.render_frame()
    gif = tb.make_gif(show=True,rev=True,duration=100)
    #tb.send_to_tidbyt(gif,"ok")
