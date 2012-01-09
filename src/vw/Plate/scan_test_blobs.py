#!/usr/bin/env python
import sys, os
import glob
import  subprocess, multiprocessing

# assuming this file is in the vw bin bath, alongside the blob_file_test binary
BLOB_FILE_TEST_BINARY = os.path.abspath( os.path.join( os.path.dirname( __file__), 'blob_file_test'))

def scan_blob(blobfile):
    subp = subprocess.Popen( (BLOB_FILE_TEST_BINARY, blobfile), stdout=subprocess.PIPE)
    (output, err) = subp.communicate()
    return output

def record_output(output):
    print output
    sys.stdout.flush()


def scan_all_blobs(dirname):
    assert os.path.exists(dirname)
    pool = multiprocessing.Pool()
    i = 0
    for blobfile in glob.glob( os.path.join( dirname, '*.blob') ):
        r = pool.apply_async(scan_blob, [blobfile], callback=record_output)
        i += 1
    sys.stderr.write("Pooled %d blob scans" % i)
    sys.stderr.flush()
    pool.close()
    pool.join()
    

def main():
    if len(sys.argv) != 2:
        print "Usage: %s platefile_path" % os.path.basename(__file__)
    plate_dir = sys.argv[1]
    scan_all_blobs(plate_dir)

if __name__ == "__main__":
    main()
