
# This file should not be included in the compiled wheel, but should be included in the tarball.

import os, logging
from .. import chelper as klippy_c_helper

HC_COMPILE_CMD = "gcc -Wall -g -O2 -o %s %s -lusb"
HC_SOURCE_FILES = ['hub-ctrl.c']
HC_SOURCE_DIR = '../../hub-ctrl'
HC_TARGET = "hub-ctrl"
DEST_LIB = klippy_c_helper.DEST_LIB

def build_hub_ctrl():
    srcdir = os.path.dirname(os.path.realpath(__file__))
    hubdir = os.path.join(srcdir, HC_SOURCE_DIR)
    srcfiles = get_abs_files(hubdir, HC_SOURCE_FILES)
    destlib = os.getenv("OVERRIDE_HUBCTRL_OUTPUT",get_abs_files(srcdir, [HC_TARGET])[0])
    logging.debug(f"Looking for {destlib}")
    if check_build_code(srcfiles, destlib):
        logging.info("Building C code module %s", HC_TARGET)
        do_build_code(HC_COMPILE_CMD % (destlib, ' '.join(srcfiles)))

def build_chelper():
    srcdir = os.path.dirname(os.path.realpath(__file__))
    srcfiles = get_abs_files(srcdir, SOURCE_FILES)
    ofiles = get_abs_files(srcdir, OTHER_FILES)
    destlib = os.getenv("OVERRIDE_CHELPER_OUTPUT",get_abs_files(srcdir, [DEST_LIB])[0])
    logging.debug(f"Looking for {destlib}")
    if check_build_code(srcfiles+ofiles+[__file__], destlib):
        if check_gcc_option(SSE_FLAGS):
            cmd = "%s %s %s" % (GCC_CMD, SSE_FLAGS, COMPILE_ARGS)
        else:
            cmd = "%s %s" % (GCC_CMD, COMPILE_ARGS)
        logging.info("Building C code module %s", DEST_LIB)
        do_build_code(cmd % (destlib, ' '.join(srcfiles)))

GCC_CMD = "gcc"
COMPILE_ARGS = ("-Wall -g -O2 -shared -fPIC"
                " -flto -fwhole-program -fno-use-linker-plugin"
                " -o %s %s")
SSE_FLAGS = "-mfpmath=sse -msse2"
SOURCE_FILES = [
    'pyhelper.c', 'serialqueue.c', 'stepcompress.c', 'itersolve.c', 'trapq.c',
    'pollreactor.c', 'msgblock.c', 'trdispatch.c',
    'kin_cartesian.c', 'kin_corexy.c', 'kin_corexz.c', 'kin_delta.c',
    'kin_deltesian.c', 'kin_polar.c', 'kin_rotary_delta.c', 'kin_winch.c',
    'kin_extruder.c', 'kin_shaper.c',
]
OTHER_FILES = [
    'list.h', 'serialqueue.h', 'stepcompress.h', 'itersolve.h', 'pyhelper.h',
    'trapq.h', 'pollreactor.h', 'msgblock.h'
]
# Update filenames to an absolute path
def get_abs_files(srcdir, filelist):
    return [os.path.join(srcdir, fname) for fname in filelist]

# Return the list of file modification times
def get_mtimes(filelist):
    out = []
    for filename in filelist:
        try:
            t = os.path.getmtime(filename)
        except os.error:
            continue
        out.append(t)
    return out

# Check if the code needs to be compiled
def check_build_code(sources, target):
    src_times = get_mtimes(sources)
    obj_times = get_mtimes([target])
    return not obj_times or max(src_times) > min(obj_times)

# Check if the current gcc version supports a particular command-line option
def check_gcc_option(option):
    cmd = "%s %s -S -o /dev/null -xc /dev/null > /dev/null 2>&1" % (
        GCC_CMD, option)
    res = os.system(cmd)
    return res == 0

# Check if the current gcc version supports a particular command-line option
def do_build_code(cmd):
    res = os.system(cmd)
    if res:
        msg = "Unable to build C code module (error=%s)" % (res,)
        logging.error(msg)
        raise Exception(msg)
