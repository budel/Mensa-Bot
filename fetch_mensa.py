import ctypes
import functools

lib = ctypes.CDLL('fetch_mensa/target/debug/libmensa_fetcher.so')
lib.compute.restype = ctypes.c_char_p

@functools.cache
def fetch_mensa():
    ptr = lib.compute()
    result = ctypes.c_char_p(ptr).value.decode("utf-8")
    if result:
        return result
    else:
        raise RuntimeError("fetch_menu returned an empty string")

# Free the memory in Rust after usage.
# lib.free_string.argtypes = [ctypes.c_char_p]
# lib.free_string(ptr)
