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
      - id: mode
        type: u1
        doc: has a higher part and a lower part, the lower seems to be type of the asset. It can be 0, 1, 5, 8, 9
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

The HLIB contains graphics data, such as sprites, images and palettes. The code mentions two versions "TILE" and "TIL2", however, only "TIL2" is used in the game files.

## TIL2 Format

These are the items that are contained inside the HLIB file with the "TIL2" magic. The items are stored in a specific format, which is described below.

```ksy
meta:
  id: til2
  file-extension: TIL2
  endian: le

seq:
  - id: height
    type: u2le
    doc: Original height (rows) of the image.

  - id: top_offset
    type: s2le
    doc: Y-drawing offset (signed).

  - id: left_offset
    type: s2le
    doc: X-drawing offset (signed).

  - id: pixel_count
    type: u1
    doc: Number of 4-pixel groups per row.  
         Full image width in px = `pixel_count * 4`.

  - id: mode_flags
    type: u1
    doc: Low nibble = primary mode (0=generic,1=planar,5=8-bit chunky,8=palette,9=composite);  
         High nibble = secondary flags.

  - id: unknown1
    type: u2le
    doc: Reserved / unknown.

  - id: unknown2
    type: u2le
    doc: Reserved / unknown.
```

The low nibble of the `mode_flags` field indicates the primary mode of the image, while the high nibble contains secondary flags that may provide additional information about the image format or rendering options.

### Mode 0: Generic/chunky fallback

Identical to Mode 5 (8-bit chunky). Treated as a simple row-major array of 8-bit palette indices, two pixels per 16-bit word, with 0xFF meaning “transparent.”

### Mode 1 Planar (ILBM-style)

Needs confirmation, but likely uses a planar format similar to ILBM.

### Mode 5: Chunky 8-bit palettized

Standard sprite format:
 - Each 16-bit word holds two 8-bit palette indices.
 - 0xFF = transparent pixel, otherwise alpha=0xFF.
 - After unpacking, each index is looked up in the 256-entry palette to produce RGBA.


### Mode 8: Palette block

Instead of image data, this item is a 256-entry RGB palette (768 bytes total). 

### Mode 9: Composite image

A “meta-sprite” that references multiple sub-images (other TIL2 items) and their offsets.
 - The data for Mode 9 is a small table of (sub_index, dx, dy) triplets.
 - The renderer iterates through each entry, pulls in the referenced TIL2 image, and blits it at (base_x + dx, base_y + dy).