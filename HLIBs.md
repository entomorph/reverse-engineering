# HLIB Format documentation

The HLIB is a data format that is contained in the `.LIB` files. It is used to store a collection of items, each with a variable size. The header of the file contains the number of elements in the collection, and the offsets to each item in the file.

```ksy
meta:
  id: hlib
  file-extension: hlib
  endian: le
seq:
  - id: header
    type: header
  - id: item_offsets
    type: u4
    repeat: expr
    repeat-expr: header.num_elements + 1
instances:
  items:
    type: item(_index)
    repeat: expr
    repeat-expr: header.num_elements
types:
  header:
    seq:
      - id: magic
        contents: "HLIB"
      - id: size
        type: u4
      - id: num_elements
        type: u2
      - id: compression_mode
        type: u1
      - id: unk2
        type: u1
      - id: magic2
        type: str
        size: 4
        encoding: ASCII
        doc: Seems to be always TIL2, but the code supports other types.
  item:
    params:
      - id: idx
        type: s4
    instances:
      content:
        pos: _root.item_offsets[idx]
        size: _root.item_offsets[idx + 1] - _root.item_offsets[idx]
        type: data
  data:
    seq:
      - id: bytes
        type: u1
        repeat: eos
```

The HLIB contains several other types of data, here are some examples:

### Palette

Found in `ENGINE/SYSFILE.LIB` at index 0.

It contains a header of 12 bytes, followed by 256 RGB colors (768 bytes).


### Interleaved Bitmap (ILBM)

Located in ENGINE/SYSFILE.LIB and ENGINE/PC.LIB, these files are [ILBM](https://en.wikipedia.org/wiki/ILBM) (Interleaved Bitmap) format images, specifically of the PBM (Planar Bitmap) variant, used for full-screen graphics. The ILBM format, originating from an earlier era, lacks support from most current image viewers. To view these images, Graphics Workshop 1.1Y is recommended and available for download at [settlers2.net](https://settlers2.net/wp-content/uploads/2011/06/gwsw95.exe).