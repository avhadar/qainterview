## Code (main.py)

### General remarks
* The code doesn't include comments, general descriptions or details about functions and classes.
* Type hints are also not included, but might be useful
* Some dependencies are not included in the requirements file, even though they are used:  
opencv-python (used as cv2) for image processing, possibly pytest for testing
* Magic numbers are used in some methods without further explanation:  
250/270, 650 

### Remarks for specific sections
#### PixelFilter.convert_hue_to_wavelength: 
* int(250/270.0) will always return 0 -> use instead int(hue*250/270.0) ?
#### PixelFilter.convert_wavelength_to_hue:
* int(270/250) will always return 1 -> use another formula instead?
#### iterate:
* the variable "pixel" seems superfluous -> use new_pixel instead of pixel?  
```
    new_pixel = filter.apply(hsv_pixel)
    pixel = new_pixel
    filtered_image[i, j] = pixel
```

#### main section:
* code can be re-used easily if it is part of a function instead of a code section
* what happens if no filters are found or available?

###  Suggestions:
* add unit tests
* add docstrings and comments for class, functions and the main section
* use tools for linting, formatters and type hints
* wrap the code of the main section in a function for further (re-)use
* use constants instead of magic numbers if possible


## Backlog 

### General remarks
* Each story has all the preceding ones as pre-requisite, even though some of them seem independent:  
e.g. conversion functions and csv definition
* Some stories are more specific than others

### Remarks for specific stories:
#### ASTRO-0002:
* formula references for conversion would be useful for the implementation
#### ASTRO-0003 and ASTRO-0004:
* some overlap between these stories; also the definition of the CSV content changes
* could be merged or rather separated into filter definition vs filter application on image
#### ASTRO-0005:
* how is the "proper order" defined and how can it be enforced?
#### ASTRO-0006:
* "as fast as possible", "within the shortest timespan" are not measurable, not specific enough for performance definitions

