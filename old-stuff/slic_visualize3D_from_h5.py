#!/usr/bin/env python

import vigra
import numpy as np
import sys
import h5py


def visualize(img, intensityScaling, seedDistance, minSize=0, iterations=10):
    res = vigra.analysis.slicSuperpixels(img,
                                         intensityScaling,
                                         seedDistance,
                                         minSize,
                                         iterations)
    clusters = np.array(np.unique(res[0]))
    ndim = len(img.shape)
    out = np.zeros(img.shape[:ndim] + (3,))
    for c in clusters:
        ind = (res[0] == c)[...]
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
    with h5py.File(fn, 'r') as f:
        ds = f['volume/data']
        img = ds[0,...,0].astype(np.float32)
        axtags = ds.attrs['axistags']
    res, out = visualize(img,
                         args['scale'],
                         args['seedDist'],
                         args['minSize'],
                         10)
    with h5py.File(out_fn, 'w') as f:
        ds = f.create_dataset('volume/data', data=out[np.newaxis,...].astype(np.uint8))
        ds.attrs['axistags'] = axtags
    
    
