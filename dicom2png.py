"""
Extracts the pixel arrays from dicom files
in a directory and save those as 16-bit png.

The pixel values are rescaled using the
`RescaleSlope` and `RescaleIntercept`
stored in the DICOM file.

By default, the PNG will be named using
DICOM `InstanceNumber`.
The original filename can be optionally
chosen to be appended to the PNG filename.


Sifan Ye
sye8 at cs dot stanford dot edu
2021

See repository at
https://github.com/sye8/dicom2png
"""

import argparse
import os

import cv2
import numpy as np
import pydicom as dicom

from tqdm import tqdm


parser = argparse.ArgumentParser(description=("Extracts the pixel arrays from dicom files in a directory and save those as 16-bit png."
                                              "The pixel values are rescaled using the `RescaleSlope` and `RescaleIntercept` stored in the DICOM file."
                                              "By default, the PNG will be named using DICOM `InstanceNumber`. "
                                              "The original filename can be optionally chosen to be appended to the PNG filename."))
parser.add_argument("input", type=str, help="input path to directory containing the DICOM files")
parser.add_argument("output", type=str, help="output path to directory where the PNG files will be saved")
parser.add_argument("--a_orig_filename", help="If present, the original filename will be appended to the PNG filename", action="store_true")
args = parser.parse_args()

dicom_path = args.input
png_path = args.output

if not os.path.exists(png_path):
    os.makedirs(png_path)

files = os.listdir(dicom_path)
for file in tqdm(files):
    file_splitted = file.split(".")
    file_name = ".".join(file_splitted[:-1])
    file_type = file_splitted[-1]
    if file_type == "dcm":
        ds = dicom.read_file(os.path.join(dicom_path, file))
        rawimg = ds.pixel_array
        m = ds.RescaleSlope
        c = ds.RescaleIntercept
        scaled_img = m * rawimg + c
        scaled_max = np.amax(scaled_img)
        scaled_min = np.amin(scaled_img)
        scaled_img = ((scaled_img - scaled_min) / (scaled_max - scaled_min)) * 65535
        scaled_img = scaled_img.astype("uint16")
        output_name = str(ds.InstanceNumber)
        if args.a_orig_filename:
            output_name += "_" + file_name
        output_name += ".png"
        cv2.imwrite(os.path.join(png_path, output_name), scaled_img)
