#!/usr/bin/env python
"""
This makes a multiband image from single band images.
"""

import os
import sys
import argparse


def mergeBands(projName, projDir, outDir): 
    bands = [r'blue', r'green', r'red', r'red edge', r'nir']
    projDir = os.path.join(projDir, r'Project\4_index\reflectance')
    images = []
    for b in bands:
        image = os.path.join(projDir, r'pix4d_transparent_reflectance_%s.tif'%b)
        if b == r'red edge':
            old = image
            image = image.replace(' ', '_')        
            if os.path.exists(old) is True:
                os.rename(old, image)
        images.append(image)
    dstFile = os.path.join(outDir, r'%s_multiband.tif'%project)
    cmd = r'gdal_merge.py -o %s -of GTiff -separate %s'%(dstFile, ' '.join(images))
    os.system(cmd)
    print("Processing completed")


def getCmdargs():
    """
    Get the command line arguments.
    """
    p = argparse.ArgumentParser(
            description=("Makes a multiband image from single band images."))
    p.add_argument("-p", "--projectName", dest="projectName", default=None,
                   help=("Project name for output file prefix"))
    p.add_argument("-i", "--inDir", dest="inDir", default=None,
                   help=("Directory containing input images"))
    p.add_argument("-o", "--outDir", dest="outDir", default=None,
                   help=("Directory for output images"))  
    cmdargs = p.parse_args()
    if (cmdargs.projectName is None or
        cmdargs.inDir is None or cmdargs.outDir is None):
        p.print_help()
        print("Must give project and directory names.")
        sys.exit()
    return cmdargs


if __name__ == "__main__":
    cmdargs = getCmdargs()
    mergeBands(cmdargs.projectName, cmdargs.inDir, cmdargs.outDir)