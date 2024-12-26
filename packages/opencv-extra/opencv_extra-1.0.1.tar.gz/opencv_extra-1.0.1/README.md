# OpenCV Extra Utilities

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

This package is built as a opencv utilities. Additional algorithms to write text on the image without thinking about the image size. My algorithm will do it own its own.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

pip install opencv-extra

## Usage <a name = "usage"></a>
```
image = cv.imread("car.jpg", cv.IMREAD_COLOR)
cv.namedWindow("Image", cv.WINDOW_NORMAL)
image = put_text(image, "car", (0, 255, 0), (0, 0), True)
cv.imshow("Image", image)
cv.waitKey(0)
```

#### Added draw_label in this version


### Additional algorithms will be updated regularly, keep in touch with this python package.
