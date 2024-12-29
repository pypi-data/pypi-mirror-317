import hmac
import hashlib
import math
from typing import Optional

class Encryptor:
    """Encryption utility class"""
    _PADCHAR: str = "="
    _ALPHA: str = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA"

    @staticmethod
    def force(msg: str) -> bytes:
        return bytes(ord(w) for w in msg)

    @staticmethod
    def ordat(msg: str, idx: int) -> int:
        return ord(msg[idx]) if len(msg) > idx else 0

    @classmethod
    def sencode(cls, msg: str, key: bool) -> list:
        l = len(msg)
        pwd = []
        for i in range(0, l, 4):
            pwd.append(
                cls.ordat(msg, i) | cls.ordat(msg, i + 1) << 8 |
                cls.ordat(msg, i + 2) << 16 | cls.ordat(msg, i + 3) << 24
            )
        if key:
            pwd.append(l)
        return pwd

    @classmethod
    def lencode(cls, msg: list, key: bool) -> Optional[str]:
        l = len(msg)
        ll = (l - 1) << 2
        if key:
            m = msg[l - 1]
            if m < ll - 3 or m > ll:
                return None
            ll = m

        msg = [''.join(chr(msg[i] >> j & 0xff) for j in (0, 8, 16, 24)) for i in range(l)]
        return ''.join(msg)[:ll] if key else ''.join(msg)

    @classmethod
    def get_xencode(cls, msg: str, key: str) -> str:
        if not msg:
            return ""

        pwd = cls.sencode(msg, True)
        pwdk = cls.sencode(key, False)
        pwdk.extend([0] * (4 - len(pwdk))) if len(pwdk) < 4 else None

        n = len(pwd) - 1
        z = pwd[n]
        y = pwd[0]
        c = 0x86014019 | 0x183639A0
        d = 0
        q = math.floor(6 + 52 / (n + 1))

        while q > 0:
            d = d + c & (0x8CE0D9BF | 0x731F2640)
            e = d >> 2 & 3

            for p in range(n):
                y = pwd[p + 1]
                m = z >> 5 ^ y << 2
                m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
                m = m + (pwdk[(p & 3) ^ e] ^ z)
                pwd[p] = pwd[p] + m & (0xEFB8D130 | 0x10472ECF)
                z = pwd[p]

            y = pwd[0]
            m = z >> 5 ^ y << 2
            m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
            m = m + (pwdk[(n & 3) ^ e] ^ z)
            pwd[n] = pwd[n] + m & (0xBB390742 | 0x44C6F8BD)
            z = pwd[n]
            q -= 1

        return cls.lencode(pwd, False)

    @classmethod
    def get_base64(cls, s: str) -> str:
        def _getbyte(s: str, i: int) -> int:
            x = ord(s[i])
            if x > 255:
                raise ValueError("INVALID_CHARACTER_ERR: DOM Exception 5")
            return x

        if not s:
            return s

        x = []
        imax = len(s) - len(s) % 3

        for i in range(0, imax, 3):
            b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8) | _getbyte(s, i + 2)
            x.extend([
                cls._ALPHA[(b10 >> 18)],
                cls._ALPHA[((b10 >> 12) & 63)],
                cls._ALPHA[((b10 >> 6) & 63)],
                cls._ALPHA[(b10 & 63)]
            ])

        i = imax
        if len(s) - imax == 1:
            b10 = _getbyte(s, i) << 16
            x.append(cls._ALPHA[(b10 >> 18)] + cls._ALPHA[((b10 >> 12) & 63)] + cls._PADCHAR + cls._PADCHAR)
        elif len(s) - imax == 2:
            b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8)
            x.append(cls._ALPHA[(b10 >> 18)] + cls._ALPHA[((b10 >> 12) & 63)] + cls._ALPHA[((b10 >> 6) & 63)] + cls._PADCHAR)

        return "".join(x)