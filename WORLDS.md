# WORLDs files

Those are [.LIB](LIBs.md) files stored in the `WORLDS` directory. They all seem to contain 12 entries. They are as follows:

## Index 0

- Format: WLD
- Internal name: WORLD_NAME.WLD
- Description: Contains the world map tiles, 2 hitboxes and 2 palettes.
- Group id: 2

```ksy
meta:
  id: wld
  file-extension: WLD
  endian: le

seq:
  - id: magic
    type: u4

  - id: grp2
    contents: "GRP2"

  - id: wld2
    contents: "WLD2"

  - id: offset_to_player_initial_action
    type: u4

  - id: offset_to_player_initial_action_size
    doc: |
      Always hard-coded to 4 in the game’s code.
    type: u4

  - id: offset_to_screen_buffer_info
    type: u4
    doc: Points into the file at the screen-buffer layout block.

  - id: offset_to_screen_buffer_info_size
    type: u4

  - id: offset_to_some_hitbox_1
    type: u4

  - id: offset_to_some_hitbox_1_size
    type: u4

  - id: offset_to_some_hitbox_2
    type: u4

  - id: offset_to_some_hitbox_2_size
    type: u4

  - id: palette1
    type: u4

  - id: palette1_size
    type: u4

  - id: palette2
    type: u4

  - id: palette2_size
    type: u4

  - id: unkx
    doc: Doesn’t appear in any code – could be another palette
    type: u4

  - id: unkx1
    doc: Same as `unkx`
    type: u4

instances:
  screen_buffer_info_block:
    io: _root._io
    pos: offset_to_screen_buffer_info
    size: offset_to_screen_buffer_info_size
    type: screen_buffer_info_type

  hitbox1_list:
    io: _root._io
    pos: offset_to_some_hitbox_1
    size: offset_to_some_hitbox_1_size
    type: hitbox_type

  hitbox2_list:
    io: _root._io
    pos: offset_to_some_hitbox_2
    size: offset_to_some_hitbox_2_size
    type: hitbox_type

  palette1_list:
    io: _root._io
    pos: palette1
    size: palette1_size
    type: palette1_array

  palette2_list:
    io: _root._io
    pos: palette2
    size: palette2_size
    type: palette2_array

types:
  screen_buffer_info_type:
    seq:
      - id: num_tiles_x
        type: u2
      - id: num_tiles_y
        type: u2
      - id: tile_size_x
        type: u2
      - id: tile_size_y
        type: u2
      - id: initial_y_offset
        type: u2
      - id: bitplane_count
        type: u2
      - id: viewport_tile_rows
        type: u2
      - id: column_shift
        type: u2
      - id: row_stride_bytes
        type: u2
      - id: pixel_data
        type: u2
        repeat: expr
        repeat-expr: num_tiles_y * tile_size_y * 2
        doc: |
          bit 15    = visibility flag   (0 = draw, 1 = skip)
          bits 14–11 = attribute flags  (palette, H/V flips, etc.)
          bits 10– 0 = tile index        (which graphic in the .OJT to pull)

  hitbox_type:
    seq:
      - id: width
        type: s2
        doc: Hitbox width in pixels (e.g. 286).

      - id: height
        type: s2
        doc: Hitbox height in pixels (e.g. 336).

      - id: shift_bits
        type: s2
        doc: Amount to shift bitmasks in various routines.

      - id: unk1
        type: s2
        doc: Not used by the code. 

      - id: row_stride
        type: s2
        doc: >
          Number of **bytes per column** of mask_data
          = ceil(height / 8). I.e. how many bytes you need
          to cover `height` bits (one bit per pixel).

      - id: mask_data
        type: u1
        repeat: expr
        repeat-expr: width * row_stride
        doc: |
          The actual hit-mask, **column-major**, 1 bit = 1 pixel.
          Each column of `height` pixels is packed into `row_stride` bytes,
          so the total number of mask bytes is exactly  
          `width * row_stride`. 
          
  palette1_array:
    seq:
      - id: entries
        type: u1
        repeat: expr
        repeat-expr: _root.palette1_size

  palette2_array:
    seq:
      - id: entries
        type: u1
        repeat: expr
        repeat-expr: _root.palette2_size
          
``` 

## Index 1

- Format: [HLIB](HLIB.md)
- Internal name: <WORLD_NAME>.TLB
- Description: Contains the tile graphics for this world.
- Group id: 1

## Index 2

- Format: [HLIB](HLIB.md)
- Description: The tileset for this world. The item at index 0 is always the palette.

## Index 3

- Format: OJI
- Internal name 1.OJI
- Group id: 3

## Index 4

Format: [HLIB](HLIB.md)

## Index 5

- Format: OJI
- Internal name 2.OJI
- Group id: 19

## Index 6

Format: [HLIB](HLIB.md)

## Index 7

- Format: OJI
- Internal name 3.OJI
- Group id: 20

## Index 8

Format: [HLIB](HLIB.md)

## Index 9

- Format: OJI
- Internal name 4.OJI
- Group id: 21

## Index 10

These are <WORLD_NAME>.OJT files. They seem to contain tile data for a particular world.

```ksy
meta:
  id: ojt
  file-extension: OJT
  endian: le

seq:
  - id: unk1
    type: u1
    doc: Always 1, doesn't seem to be used by the code. Maybe a magic number
    
  - id: unk2
    type: u1
    doc: Always 128, doesn't seem to be used by the code. Maybe a magic number
    
  - id: total_tiles
    type: u2
    doc: The total amount of `active` tiles (type !== 0)
    
  - id: some_offset
    type: u2
    doc: Always 8006, this seems to be offset to tile that will be used for type 0. Which is probably always the tile 8
    
  - id: entries
    type: ojt_entry
    doc: A fixed array of size 1000 containing the type, offset and size.
    repeat: expr
    repeat-expr: 1000

types:
  ojt_entry:
    seq:
      - id: data_offset
        type: u4
        
      - id: size
        type: u2
        doc: the size of the data. it varies depending of the type (type: 0 size: 0, type: 1 size: 260, type: 2 size: 168, type: 3 size: 26)
        
      - id: type
        type: u2
        doc: type con be 0, 1, 2 or 3
    instances:
      file_data:
        pos: data_offset
        size: size
        type: data_block
        if: type != 0

  data_block:
    seq:
      - id: tile_idx
        type: u2
      - id: unk11
        type: u2
      - id: unk2
        type: u2
      - id: unk21
        type: u2
      - id: x1
        type: u2
      - id: y2
        type: u2
      - id: unk3
        type: u1
      - id: field_c
        type: u1
      - id: unk4
        type: u2
      - id: unk41
        type: u2
      - id: field_d
        type: u1
      - id: pad31
        type: u2
      - id: pad3
        size: 17
      - id: field_e
        type: u2
      - id: rest
        size-eos: true
```

The data_block structure is not well understood yet.

## Index 11

- Format: PTH
- Internal name <WORLD_NAME>.PTH
- Group id: 38
