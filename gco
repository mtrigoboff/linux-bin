#! /bin/bash

source gccflags

do_cmd "gcc -c $CFLAGS $1.c"
