# -*- coding: utf-8 -*-
# Need to constrain U32 to only 32 bits using the & 0xFFFFFFFF
# since Python has no native notion of integers limited to 32 bit
# http://docs.python.org/library/stdtypes.html#numeric-types-int-float-long-complex
"""Original copyright notice:
    By Bob Jenkins, 1996.  bob_jenkins@burtleburtle.net.  You may use this
    code any way you wish, private, educational, or commercial. Its free.
来自七仔个人补充说明：
    这个是纯Python实现的，运行的速度还是蛮快的，温馨提示，您将可以通过修改某些位操作，可以作为自己的私有的加密方式，
    然后可以作为一个校验码来使用！欢迎大家一起交流学习，感谢！
"""

import sys


def rot(x, k):
    return (((x)<<(k)) | ((x)>>(32-(k))))


def mix(a, b, c):
    a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF
    a -= c; a &= 0xFFFFFFFF; a ^= rot(c,4);  a &= 0xFFFFFFFF; c += b; c &= 0xFFFFFFFF
    b -= a; b &= 0xFFFFFFFF; b ^= rot(a,6);  b &= 0xFFFFFFFF; a += c; a &= 0xFFFFFFFF
    c -= b; c &= 0xFFFFFFFF; c ^= rot(b,8);  c &= 0xFFFFFFFF; b += a; b &= 0xFFFFFFFF
    a -= c; a &= 0xFFFFFFFF; a ^= rot(c,16); a &= 0xFFFFFFFF; c += b; c &= 0xFFFFFFFF
    b -= a; b &= 0xFFFFFFFF; b ^= rot(a,19); b &= 0xFFFFFFFF; a += c; a &= 0xFFFFFFFF
    c -= b; c &= 0xFFFFFFFF; c ^= rot(b,4);  c &= 0xFFFFFFFF; b += a; b &= 0xFFFFFFFF
    return a, b, c


def final(a, b, c):
    a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF
    c ^= b; c &= 0xFFFFFFFF; c -= rot(b,14); c &= 0xFFFFFFFF
    a ^= c; a &= 0xFFFFFFFF; a -= rot(c,11); a &= 0xFFFFFFFF
    b ^= a; b &= 0xFFFFFFFF; b -= rot(a,25); b &= 0xFFFFFFFF
    c ^= b; c &= 0xFFFFFFFF; c -= rot(b,16); c &= 0xFFFFFFFF
    a ^= c; a &= 0xFFFFFFFF; a -= rot(c,4);  a &= 0xFFFFFFFF
    b ^= a; b &= 0xFFFFFFFF; b -= rot(a,14); b &= 0xFFFFFFFF
    c ^= b; c &= 0xFFFFFFFF; c -= rot(b,24); c &= 0xFFFFFFFF
    return a, b, c


def hashlittle2(data, initval=0, initval2=0):
    length = lenpos = len(data)

    a = b = c = (0xdeadbeef + (length) + initval)

    c += initval2; c &= 0xFFFFFFFF

    p = 0  # 字符串偏移，进行位操作运算
    while lenpos > 12:
        a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24)); a &= 0xFFFFFFFF
        b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); b &= 0xFFFFFFFF
        c += (ord(data[p+8]) + (ord(data[p+9])<<8) + (ord(data[p+10])<<16) + (ord(data[p+11])<<24)); c &= 0xFFFFFFFF
        a, b, c = mix(a, b, c)
        p += 12
        lenpos -= 12

    if lenpos == 12:
        c += (ord(data[p+8]) + (ord(data[p+9])<<8) + (ord(data[p+10])<<16) + (ord(data[p+11])<<24)); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 11:
        c += (ord(data[p+8]) + (ord(data[p+9])<<8) + (ord(data[p+10])<<16)); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 10:
        c += (ord(data[p+8]) + (ord(data[p+9])<<8)); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 9:
        c += (ord(data[p+8])); b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 8:
        b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16) + (ord(data[p+7])<<24)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 7:
        b += (ord(data[p+4]) + (ord(data[p+5])<<8) + (ord(data[p+6])<<16)); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 6:
        b += ((ord(data[p+5])<<8) + ord(data[p+4])); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24))
    if lenpos == 5:
        b += (ord(data[p+4])); a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24));
    if lenpos == 4:
        a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16) + (ord(data[p+3])<<24))
    if lenpos == 3:
        a += (ord(data[p+0]) + (ord(data[p+1])<<8) + (ord(data[p+2])<<16))
    if lenpos == 2:
        a += (ord(data[p+0]) + (ord(data[p+1])<<8))
    if lenpos == 1:
        a += ord(data[p+0])
    a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF
    if lenpos == 0:
        return c, b

    a, b, c = final(a, b, c)

    return c, b  # 这里是原版，您可以修改这里，返回不同的结果，
    # 例如py3写法(py2可能要注意int和long的转换)：
    # return ((int(a)) << 24) | (int(b) & 0xFFFFFF)  # 这里返回的值是一个，后面的记得也相应修改   


def hashlittle(data, initval=0):
    c, b = hashlittle2(data, initval, 0)
    return c


if __name__ == "__main__":
    hashstr = "hello every one!"
    # hashstr = "123456"
    # hashstr = '反对黄赌毒'

    hash, hash2 = hashlittle2(hashstr, 0xdeadbeef, 0xdeadbeef)  # 也可以修改这些偏移量(或者称为自己某一指定的校验)
    print('"%s": %x %x' % (hashstr, hash, hash2))

    hash = hashlittle(hashstr, 0)
    print('"%s": %s' % (hashstr, hash))



