# tidbytplotlib

The [tidbyt](https://tidbyt.com/) is a wifi connected led matrix that's way more fun than it has any right to be. This is a simple python library that allows the display to plot simple lines and text, inspired by (but not nearly as functional as) matplotlib. 

## Basic Example

```python

    import tidbytplotlib as tbplt

    dev_name = "DEVICE_ID"
    api_token =  "API_TOKEN"
    tb = tbplt.tidbyt_plot(dev_name,api_token)
 
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
    tb.send_to_tidbyt(gif,"ok")
```
which should render

![example](https://user-images.githubusercontent.com/152047/176831799-f224a134-e1e1-4396-830f-af9c093357c2.gif)

## Requirements

- requests
- numpy
- PILLOW


