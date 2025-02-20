"""
Mock filesystem contents for duprem units; originally copied from dgutil.test
"""

files = {
    "topdir": {
        "filetree": {
            "empty1.txt": b"",
            "empty2.txt": b"",
            "basic.txt": b"some text here",
            "notapic.jpg": b"Should be recognized as a general file, not an image, despite the extension",
            "badpic2.jpg": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x01\x2c\x01\x2c\x00\x00\xff\xe1\x00\xf2\x45\x78\x69\x66\x00\x00\x49\x49\x2a\x00\x08\x00\x00\x00\x08\x00\x0e\x01\x02\x00\x12\x00\x00\x00\x6e\x00\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x80\x00\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x88\x00\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x90\x00\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x9e\x00\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\xb2\x00\x00\x00\x00\x00\x00\x00\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x31\x39\x3a\x32\x33\x00\x02\x00\x86\x92\x07\x00\x19\x00\x00\x00\xd0\x00\x00\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\xff\xdb\x00\x43\x00\x03\x02\x02\x03\x02\x02\x03\x03\x03\x03\x04\x03\x03\x04\x05\x08\x05\x05\x04\x04\x05\x0a\x07\x07\x06\x08\x0c\x0a\x0c\x0c\x0b\x0a\x0b\x0b\x0d\x0e\x12\x10\x0d\x0e\x11\x0e\x0b\x0b\x10\x16\x10\x11\x13\x14\x15\x15\x15\x0c\x0f\x17\x18\x16\x14\x18\x12\x14\x15\x14\xff\xdb\x00\x43\x01\x03\x04\x04\x05\x04\x05\x09\x05\x05\x09\x14\x0d\x0b\x0d\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xfe\x00\x14\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\xff\xc2\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03\x10\x00\x00\x01\x54\x9f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x05\x02\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x42\x41\x44\x20\x44\x41\x54\x41\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x06\x3f\x02\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x21\x7f\xff\xda\x00\x0c\x03\x01\x00\x02\x00\x03\x00\x00\x00\x10\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x10\x7f\xff\xd9\x0a",
            "pic1.bmp": b"\x42\x4d\x8e\x00\x00\x00\x00\x00\x00\x00\x8a\x00\x00\x00\x7c\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x04\x00\x00\x00\x23\x2e\x00\x00\x23\x2e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x42\x47\x52\x73\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00",
            "pic1.jpg": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x01\x2c\x01\x2c\x00\x00\xff\xe1\x00\xf2\x45\x78\x69\x66\x00\x00\x49\x49\x2a\x00\x08\x00\x00\x00\x08\x00\x0e\x01\x02\x00\x12\x00\x00\x00\x6e\x00\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x80\x00\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x88\x00\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x90\x00\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x9e\x00\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\xb2\x00\x00\x00\x00\x00\x00\x00\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x31\x37\x3a\x33\x38\x00\x02\x00\x86\x92\x07\x00\x19\x00\x00\x00\xd0\x00\x00\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\xff\xdb\x00\x43\x00\x03\x02\x02\x03\x02\x02\x03\x03\x03\x03\x04\x03\x03\x04\x05\x08\x05\x05\x04\x04\x05\x0a\x07\x07\x06\x08\x0c\x0a\x0c\x0c\x0b\x0a\x0b\x0b\x0d\x0e\x12\x10\x0d\x0e\x11\x0e\x0b\x0b\x10\x16\x10\x11\x13\x14\x15\x15\x15\x0c\x0f\x17\x18\x16\x14\x18\x12\x14\x15\x14\xff\xdb\x00\x43\x01\x03\x04\x04\x05\x04\x05\x09\x05\x05\x09\x14\x0d\x0b\x0d\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xfe\x00\x14\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\xff\xc2\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03\x10\x00\x00\x01\x54\x9f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x05\x02\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x06\x3f\x02\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x21\x7f\xff\xda\x00\x0c\x03\x01\x00\x02\x00\x03\x00\x00\x00\x10\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x10\x7f\xff\xd9",
            "pic1.tiff": b"\x49\x49\x2a\x00\x08\x00\x00\x00\x14\x00\x00\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x02\x01\x03\x00\x03\x00\x00\x00\xfe\x00\x00\x00\x03\x01\x03\x00\x01\x00\x00\x00\x08\x00\x00\x00\x06\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x11\x01\x04\x00\x01\x00\x00\x00\x5e\x01\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x15\x01\x03\x00\x01\x00\x00\x00\x03\x00\x00\x00\x16\x01\x03\x00\x01\x00\x00\x00\x80\x00\x00\x00\x17\x01\x04\x00\x01\x00\x00\x00\x0b\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x04\x01\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x0c\x01\x00\x00\x1c\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1d\x01\x02\x00\x0f\x00\x00\x00\x14\x01\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x24\x01\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x32\x01\x00\x00\x3d\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x53\x01\x03\x00\x03\x00\x00\x00\x46\x01\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\x4c\x01\x00\x00\x00\x00\x00\x00\x08\x00\x08\x00\x08\x00\xff\xff\xff\xff\x29\x74\xda\x00\xff\xff\xff\xff\x29\x74\xda\x00\x70\x69\x63\x31\x2e\x74\x69\x6e\x79\x2e\x74\x69\x66\x66\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x31\x38\x3a\x33\x39\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x78\x9c\xfb\xff\xff\x3f\x00\x05\xfd\x02\xfe\x00",
            "pic2.bmp": b"\x42\x4d\x8e\x00\x00\x00\x00\x00\x00\x00\x8a\x00\x00\x00\x7c\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x04\x00\x00\x00\x23\x2e\x00\x00\x23\x2e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\xff\x00\x00\xff\x00\x00\x00\x00\x00\x00\x00\x42\x47\x52\x73\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00",
            "pic2.jpg": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x01\x2c\x01\x2c\x00\x00\xff\xe1\x00\xf2\x45\x78\x69\x66\x00\x00\x49\x49\x2a\x00\x08\x00\x00\x00\x08\x00\x0e\x01\x02\x00\x12\x00\x00\x00\x6e\x00\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x80\x00\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x88\x00\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x90\x00\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x9e\x00\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\xb2\x00\x00\x00\x00\x00\x00\x00\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x31\x39\x3a\x32\x33\x00\x02\x00\x86\x92\x07\x00\x19\x00\x00\x00\xd0\x00\x00\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\xff\xdb\x00\x43\x00\x03\x02\x02\x03\x02\x02\x03\x03\x03\x03\x04\x03\x03\x04\x05\x08\x05\x05\x04\x04\x05\x0a\x07\x07\x06\x08\x0c\x0a\x0c\x0c\x0b\x0a\x0b\x0b\x0d\x0e\x12\x10\x0d\x0e\x11\x0e\x0b\x0b\x10\x16\x10\x11\x13\x14\x15\x15\x15\x0c\x0f\x17\x18\x16\x14\x18\x12\x14\x15\x14\xff\xdb\x00\x43\x01\x03\x04\x04\x05\x04\x05\x09\x05\x05\x09\x14\x0d\x0b\x0d\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xfe\x00\x14\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\xff\xc2\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03\x10\x00\x00\x01\x54\x9f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x05\x02\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x06\x3f\x02\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x21\x7f\xff\xda\x00\x0c\x03\x01\x00\x02\x00\x03\x00\x00\x00\x10\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x10\x7f\xff\xd9",
            "pic2.tiff": b"\x49\x49\x2a\x00\x08\x00\x00\x00\x15\x00\x00\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x02\x01\x03\x00\x03\x00\x00\x00\x0a\x01\x00\x00\x03\x01\x03\x00\x01\x00\x00\x00\x05\x00\x00\x00\x06\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x0e\x01\x02\x00\x12\x00\x00\x00\x10\x01\x00\x00\x11\x01\x04\x00\x01\x00\x00\x00\xa2\x01\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x15\x01\x03\x00\x01\x00\x00\x00\x03\x00\x00\x00\x16\x01\x03\x00\x01\x00\x00\x00\x80\x00\x00\x00\x17\x01\x04\x00\x01\x00\x00\x00\x05\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x22\x01\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x2a\x01\x00\x00\x1c\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1d\x01\x02\x00\x0f\x00\x00\x00\x32\x01\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x42\x01\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x50\x01\x00\x00\x3d\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x53\x01\x03\x00\x03\x00\x00\x00\x64\x01\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\x6a\x01\x00\x00\x00\x00\x00\x00\x08\x00\x08\x00\x08\x00\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x70\x69\x63\x32\x2e\x74\x69\x6e\x79\x2e\x74\x69\x66\x66\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x31\x39\x3a\x34\x39\x00\x01\x00\x01\x00\x01\x00\x02\x00\x86\x92\x07\x00\x19\x00\x00\x00\x88\x01\x00\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x44\x69\x66\x66\x65\x72\x65\x6e\x74\x20\x63\x6f\x6d\x6d\x65\x6e\x74\x00\x80\x3f\xe0\x50\x10\x00",
            "pic3.jpg": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x01\x2c\x01\x2c\x00\x00\xff\xe1\x00\xf2\x45\x78\x69\x66\x00\x00\x49\x49\x2a\x00\x08\x00\x00\x00\x08\x00\x0e\x01\x02\x00\x12\x00\x00\x00\x6e\x00\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x80\x00\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x88\x00\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x90\x00\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x9e\x00\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\xb2\x00\x00\x00\x00\x00\x00\x00\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x32\x30\x3a\x31\x33\x00\x02\x00\x86\x92\x07\x00\x19\x00\x00\x00\xd0\x00\x00\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\xff\xdb\x00\x43\x00\x03\x02\x02\x03\x02\x02\x03\x03\x03\x03\x04\x03\x03\x04\x05\x08\x05\x05\x04\x04\x05\x0a\x07\x07\x06\x08\x0c\x0a\x0c\x0c\x0b\x0a\x0b\x0b\x0d\x0e\x12\x10\x0d\x0e\x11\x0e\x0b\x0b\x10\x16\x10\x11\x13\x14\x15\x15\x15\x0c\x0f\x17\x18\x16\x14\x18\x12\x14\x15\x14\xff\xdb\x00\x43\x01\x03\x04\x04\x05\x04\x05\x09\x05\x05\x09\x14\x0d\x0b\x0d\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xfe\x00\x14\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\xff\xc2\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03\x10\x00\x00\x01\x2a\x1f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x05\x02\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x06\x3f\x02\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x21\x7f\xff\xda\x00\x0c\x03\x01\x00\x02\x00\x03\x00\x00\x00\x10\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x10\x7f\xff\xd9",
            "pic4.JPEG": b"\xff\xd8\xff\xe0\x00\x10\x4a\x46\x49\x46\x00\x01\x01\x01\x01\x2c\x01\x2c\x00\x00\xff\xe1\x00\xf2\x45\x78\x69\x66\x00\x00\x49\x49\x2a\x00\x08\x00\x00\x00\x08\x00\x0e\x01\x02\x00\x12\x00\x00\x00\x6e\x00\x00\x00\x12\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\x80\x00\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\x88\x00\x00\x00\x28\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x31\x01\x02\x00\x0d\x00\x00\x00\x90\x00\x00\x00\x32\x01\x02\x00\x14\x00\x00\x00\x9e\x00\x00\x00\x69\x87\x04\x00\x01\x00\x00\x00\xb2\x00\x00\x00\x00\x00\x00\x00\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x2c\x01\x00\x00\x01\x00\x00\x00\x47\x49\x4d\x50\x20\x32\x2e\x31\x30\x2e\x33\x30\x00\x00\x32\x30\x32\x33\x3a\x30\x31\x3a\x31\x37\x20\x31\x36\x3a\x32\x30\x3a\x33\x38\x00\x02\x00\x86\x92\x07\x00\x19\x00\x00\x00\xd0\x00\x00\x00\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\xff\xdb\x00\x43\x00\x03\x02\x02\x03\x02\x02\x03\x03\x03\x03\x04\x03\x03\x04\x05\x08\x05\x05\x04\x04\x05\x0a\x07\x07\x06\x08\x0c\x0a\x0c\x0c\x0b\x0a\x0b\x0b\x0d\x0e\x12\x10\x0d\x0e\x11\x0e\x0b\x0b\x10\x16\x10\x11\x13\x14\x15\x15\x15\x0c\x0f\x17\x18\x16\x14\x18\x12\x14\x15\x14\xff\xdb\x00\x43\x01\x03\x04\x04\x05\x04\x05\x09\x05\x05\x09\x14\x0d\x0b\x0d\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\x14\xff\xfe\x00\x14\x43\x72\x65\x61\x74\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x00\xff\xc2\x00\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x10\x03\x10\x00\x00\x01\x54\x9f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x05\x02\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x01\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x06\x3f\x02\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x21\x7f\xff\xda\x00\x0c\x03\x01\x00\x02\x00\x03\x00\x00\x00\x10\x9f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x03\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x11\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x02\x01\x01\x3f\x10\x7f\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x01\x3f\x10\x7f\xff\xd9",
        }
    },
}

