#!/usr/bin/env python3
import sys
import numpy as np

np.random.seed(2017)

def inside_circle(total_count):

    x = np.random.uniform(size=total_count)
    y = np.random.uniform(size=total_count)

    radii_square = x**2 + y**2

    count = (radii_square<=1.0).sum()

    return count

def estimate_pi(n_samples, executor):

    n_workers = executor._max_workers
    n_samples_inside = np.sum(list(executor.map(inside_circle, [n_samples//n_workers] * n_workers)))

    return (4.0 * n_samples_inside / n_samples)

if __name__=='__main__':

    n_samples = 10000
    if len(sys.argv) > 1:
        n_samples = int(sys.argv[1])
        n_workers = int(sys.argv[2])

    import concurrent.futures

    executor = concurrent.futures.ProcessPoolExecutor(max_workers = n_workers)

    my_pi = estimate_pi(n_samples, executor)
    sizeof = np.dtype(np.float64).itemsize

    print("[multicore version] required memory {:.3f} MB".format(n_samples*sizeof*3/(1024*1024)))
    print("[multicore version] pi is {} from {} samples".format(my_pi,n_samples))
    print("[multicore version] got {} digits right".format(int(np.ceil(-np.log10(abs(my_pi - np.pi))))))
