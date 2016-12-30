#!/usr/bin/env python3

import struct

class opcodes(object):
    short_jump = b'\xeb'
    short_call = b'\xe8'
    mov_in_rax = b'\xb8'
    mov_in_rbx = b'\xbb'
    mov_in_rdx = b'\xba'
    pop_in_rcx = b'\x59'
    ret        = b'\xc3'
    syscall    = b'\xcd\x80'

    @staticmethod
    def to_binary(data, c_type='i'):
        endianess = '<' # Little endian
        return struct.pack(endianess + c_type, data)


def syscall_write(fd, buf, count=None):

    if not isinstance(buf, bytes):
        buf = bytes(buf, 'utf-8')

    if count is None:
        count = len(buf)

    return (
        opcodes.short_jump + opcodes.to_binary(19, 'b') # Jump to 2:
      + opcodes.mov_in_rax + opcodes.to_binary(4, 'i') # 1:
      + opcodes.mov_in_rbx + opcodes.to_binary(fd, 'i')
      + opcodes.mov_in_rdx + opcodes.to_binary(count, 'i')
      + opcodes.pop_in_rcx # Move return address from stack to rcx, contains payload
      + opcodes.syscall
      + opcodes.ret # Return to original caller (since return adress from our call was popped)
      + opcodes.short_call + opcodes.to_binary(-24, 'i') # 2: Call 1
      + buf
    )

