#!/usr/bin/env python

import vigra
import numpy as np
import sys


def visualize(img, intensityScaling, seedDistance, minSize=0, iterations=10):
    res = vigra.analysis.slicSuperpixels(img,
                                         intensityScaling,
                                         seedDistance,
                                         minSize,
                                         iterations)
    clusters = np.array(np.unique(res[0]))
    out = np.zeros(img.shape[:2] + (3,))
    for c in clusters:
        ind = (res[0] == c)[...,0]
        for i in xrange(out.shape[-1]):
            out[...,i][ind] = np.random.randint(0,255)
    return res, out

        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("visualize slic")
    parser.add_argument('--filename', '-f', required=True)
    parser.add_argument('--scale', '-s', required=True, type=float)
    parser.add_argument('--seedDist', '-d', required=True, type=int)
    parser.add_argument('--minSize', '-S', default=0, type=int)
    args = vars(parser.parse_args())
    fn = args['filename']
    out_fn = ''.join(fn.split('.')[:-1] + ['_slic.'] + [fn.split('.')[-1]])
    img = vigra.impex.readImage(fn)
    res, out = visualize(img,
                         args['scale'],
                         args['seedDist'],
                         args['minSize'],
                         10)
    vigra.impex.writeImage(out, out_fn)
    
    
