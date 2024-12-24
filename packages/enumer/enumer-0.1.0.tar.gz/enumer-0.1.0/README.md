# enumer
Residue class enumeration given partial information of either end.

Example:
```
# Python

from secret import secret_message_from_someone
from enumer import *

# E
secret_message = secret_message_from_someone.encode('utf-8')
assert secret_message.startswith(b'Merry Christmas~~~~~~~~~~~~~~~~~~~~')
assert secret_message.endswith(b'padoru padoru!!!!!!!!!!!!!!!!!!!!!!!')
assert len(secret_message) == 191
flag = b2l(secret_message)
mod = int('1337133713371337133713371337133713371337133713371337'
          '1337133713371337133713371337133713371337133713371337'
          '1337133713371337133713371337133713371337133713371337'
          '1337133713371337133713371337133713371337133713371337'
          '1337133713371337133713371337133713371337133713371337'
          '13371337133713371337133713371337133713371337000', 16)
ct = flag % mod
# ct =   0xfcad5e7f12e0fd8a5e8038e0fea85e80031e5e7f06e0fc9a5e7f29
#          e0fd865e7f01e0fca89be0fca25e7f08e0fcbd5e7f2ae0fd875e80
#          0d1e5e810ce0fe875e8126e0fe8f5e8104e0fea89b45dc70e366ed
#          629b70ea6fe476ea1de65ef562e96c9b76ea72e9669b71ee72e666
#          e866e35eed5f3fd20de055822dd862875ed34cce60f11a9d1a9d1a
#          9d1a9d1a9d1a9d1a9d1a9d1a9d1a3ebd0121

# D
head = b'Merry Christmas~~~~~~~~~~~~~~~~~~~~'
tail = b'padoru padoru!!!!!!!!!!!!!!!!!!!!!!!'
length = 191
for pt in head_tail_enumer(ct, mod, head, tail, length, size_limit = 15000):
    if pt == flag:
        print(l2b(pt).decode('utf-8'))

```


Features:
- `enumer`. Perform naive enumerations of representatives.
- `tail_enumer`. With the last few bits specified. This is done by simple modular arithmetic.
- `head_tail_enumer`. With both the last and first few bits specified. This is done by meet-in-the-middle tricks.

And...
### Merry Xmas 🎄🧑‍🎄
### ~~Merry Ymas 🎄🧑‍🎄~~
### ~~Merry Zmas 🎄🧑‍🎄~~