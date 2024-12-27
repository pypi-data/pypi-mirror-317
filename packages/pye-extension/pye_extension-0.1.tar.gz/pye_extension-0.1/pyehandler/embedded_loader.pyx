# pyehandler/embedded_loader.pyx
# cython: language_level=3
from cpython.bytes cimport PyBytes_FromStringAndSize
from libc.stdlib cimport malloc, free
import marshal
from cryptography.fernet import Fernet

cdef class PyeLoader:
    cdef object fernet
    
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)
    
    def get_code(self, path):
        return self.execute_pye(path)
                
    def execute_pye(self, str filename):
        with open(filename, 'rb') as f:
            encrypted = f.read()
        decrypted = self.fernet.decrypt(encrypted)
        return compile(decrypted, filename, 'exec')

    def get_data(self, path):
        with open(path, 'rb') as f:
            return f.read()

    def get_source(self, path):
        return None

    def get_filename(self, path):
        return path