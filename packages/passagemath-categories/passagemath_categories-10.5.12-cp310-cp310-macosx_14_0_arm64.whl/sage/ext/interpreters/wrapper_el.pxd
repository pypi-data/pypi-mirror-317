# sage_setup: distribution = sagemath-categories
# Automatically generated by /private/var/folders/95/0ydz4d79163427j3k5crp3fh0000gn/T/build-env-f5l9qc2_/lib/python3.10/site-packages/sage_setup/autogen/interpreters/internal/generator.py.  Do not edit!

from cpython.ref cimport PyObject

from sage.ext.fast_callable cimport Wrapper

cdef class Wrapper_el(Wrapper):
    cdef int _n_args
    cdef object _list_constants
    cdef int _n_constants
    cdef PyObject** _constants
    cdef object _list_stack
    cdef int _n_stack
    cdef PyObject** _stack
    cdef object _domain
    cdef int _n_code
    cdef int* _code
