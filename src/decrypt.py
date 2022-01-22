from config import Config
from utils import decrypt

# text = str(sys.argv[1])
text = "cEOFtTY+4kzbWcwQD4pzHsE2XduCeAen3vgZ+AeuJIW0VSmhjgvgULPcR4FFyVejq8/ykF6yt16iJzLwEIveIEr2fc9RMhnuvdGH9Kj6heVCGxY0dxDpGX5pV5YXSeWtSFrimUSVP5weD804qyLrDUFtRW1J7OzXsnbKwIuD1le2OJrAxTxTYqWiSG3z20mxiNa2JT4jYSZ2Yq+2ov9YWTfSB+TlVn6X/rdweVN6HuYpAF1XAdWwVZar79eQ/MnGZ+GVyWW1b8CCrbWAHOF437Irj/RjS5+fTNWPIl5Shss9VFP1pmLAMmfelDB3m29XHOmaFo+J2UNQxUFKbUEaJRPtwqRpFDjp2zxu379S8Vg14SsBUjqaDHzXKY54kjKkBiwncVimN+aJBMGmOeFRdVncGJryLENs9XovEKDG+lNId/7mInlsYJU+PVM="
print(f"Got {text}")
config = Config()
decrypted = decrypt(config.seed, text)
print(decrypted)
