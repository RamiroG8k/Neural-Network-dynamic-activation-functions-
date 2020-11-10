import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

class ClickableInputs:
    def get_data(self):
        res = {
            "inputs": np.array(self.__inputs),
            "desired": np.array(self.__d) 
        }
        return res

    def onclick(self, event):
        if event.dblclick:
            x, y = event.xdata, event.ydata
            if event.button == 1:
                plt.plot(x, y, 'go')
                self.__d.append(0)
            elif event.button == 3:
                plt.plot(x, y, 'ro')
                self.__d.append(1)
            # Round precition of axis 
            self.__inputs.append([round(x,5), round(y,5)])

    def open_clickable_inputs(self):
        self.__inputs = []
        self.__d = []
        fig, ax = plt.subplots()
        plt.ylim(top=10, bottom=-10)
        plt.xlim(left=-10, right=10)
        plt.axhline(0, color="red")
        plt.axvline(0, color="red")
        # cursor = Cursor(ax, horizOn=True, vertOn=True, color='white', linewidth=2.0)
        cursor = Cursor(ax, horizOn=False, vertOn=False)
        fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.grid()
        plt.show()