import json

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mpcolor

from scipy.ndimage import gaussian_filter

## Color for text
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# 1. Read CSV Data, extract the left gaze and convert to float
df = pd.read_csv('Output/data-temp.csv')
# print(df.head(20))
df[['left_X', 'left_y']] = df['left_gaze_point_on_display_area'].str.strip('()').str.split(',', expand=True)
df = df[~df['left_X'].isna() & ~df['left_y'].isna()]
df['left_X'] = df['left_X'].astype(float)
df['left_y'] = df['left_y'].astype(float)

# 2. Open the image file and get shape
img = mpimg.imread('Output/screen-temp.png')
height, width, _ = img.shape
print(img.shape)


# 3. Create a histogram and add a gaussian filter
fig, ax = plt.subplots()
histogram = np.histogram2d(df['left_X'], df['left_y'], bins=[width, height],
                           range=[[0, 1], [0, 1]])[0]
print(histogram)

sigma = 30
histogram_gaussed = gaussian_filter(histogram, sigma=sigma)


# 4. Set color for the heatmap
c_white = mpcolor.colorConverter.to_rgba('white', alpha=0)
c_green1 = mpcolor.colorConverter.to_rgba('green', alpha=0.9)
c_green2 = mpcolor.colorConverter.to_rgba('green', alpha=0.9)
c_green3 = mpcolor.colorConverter.to_rgba('yellow', alpha=1)
c_yellow = mpcolor.colorConverter.to_rgba('red', alpha=1)

cmap_rb = mpcolor.LinearSegmentedColormap.from_list('rb_cmap',
                                                    [c_white, c_green1, c_green2, c_green3,
                                                     c_yellow], 512)

# 5. Show the image
plt.imshow(img[..., :, :, :], origin='upper')
plt.imshow(histogram_gaussed.T, cmap=cmap_rb, alpha=1, origin='upper')
plt.savefig(f'Output/heatmap{sigma}.png')
print(f'Screenshot saved in {bcolors.OKCYAN}Output/heatmap.png{bcolors.ENDC}')
plt.show()
