# dicom2py

Extracts the pixel arrays from dicom files
in a directory and save those as 16-bit png.

The pixel values are rescaled using the
`RescaleSlope` and `RescaleIntercept`
stored in the DICOM file.

By default, the PNG will be named using
DICOM `InstanceNumber`.
The original filename can be optionally
chosen to be appended to PNG filename.

## Dependencies

```
pydicom opencv-python numpy tqdm 
```

## How to Run

```
python3 dicom2png.py [-h] [--a_orig_filename] input output
```

### Positional Arguments

- `input`: input path to directory containing the DICOM files

- `output`: output path to directory where the PNG files will be save

### Optional Arguments

- `-h, --help`: See help

- `a_orig_filename`: If present, the original filename will be appended to the PNG filename

