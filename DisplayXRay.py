import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

import numpy as np


import matplotlib.colors as colors

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


class DisplayXRay:
    def __init__(self, root):

        self.root = Tk.Tk()
        self.root.wm_title("X-ray View")

        self.x_ray_image = 0;

        self.has_been_drawn = False;

    def draw(self, x_ray_image):
        self.x_ray_image = np.copy(x_ray_image);

        if not self.has_been_drawn:
            self.fig = Figure(figsize=(5, 8), dpi=100)

        #self.x_ray_image = np.multiply(np.divide(np.subtract(x_ray_image, self.x_ray_image.min()),
        #        self.x_ray_image.max() - self.x_ray_image.min()), 255);
        if self.has_been_drawn:
            print("redraw")
            self.fig.clear();

        norm = colors.Normalize(vmin=self.x_ray_image.min(),vmax=self.x_ray_image.max())

        ax = self.fig.add_subplot(211)
        self.im_plot1 = ax.imshow(self.x_ray_image, norm=norm, cmap="PuBu_r");
        self.fig.colorbar(self.im_plot1, ax=ax, extend='max');
        ax.set_title('X-ray image');

        ax = self.fig.add_subplot(212)
        n, bins, patches =  ax.hist(self.x_ray_image.ravel(), bins=256, density=True, facecolor='g', alpha=0.75)
        ax.set_yscale("log")
        ax.set_title("Intensity histogram")
        ax.set_xlabel("Intensity")
        ax.set_ylabel("Frequency")

        if not self.has_been_drawn:

            #ax.title("Intensity histogram of X-ray image");

            # a tk.DrawingArea
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)

            self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
            self.toolbar.update()

            self.canvas.mpl_connect('key_press_event', self.on_key_event)

            self.button = Tk.Button(master=self.root, text='Quit', command=self._quit)

            self.has_been_drawn = True;
        #else:

            #self.im_plot.set_data(self.x_ray_image)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.button.pack(side=Tk.BOTTOM)
        #self.fig.canvas.draw()
        #self.fig.canvas.flush_events()


    def on_key_event(self, event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas, self.toolbar)

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
