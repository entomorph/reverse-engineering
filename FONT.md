# Fonts

Fonts are stored inside .LIB archives using the [Apple IIGS Font File format](https://ciderpress2.com/formatdoc/BitmapFont-notes.html).

Known fonts in the game include:

- GENEVA.9: Geneva font, size 9. Located in `SYSFILE.LIB` at index 3.
- Round: Font with internal name “Round”. Located in `SYSFILE.LIB` at index 4.
- PLAGUE.18: Custom font. Located in `SYSFILE.LIB` at index 5.

The format is described by the following Kaitai struct:

```ksy
meta:
  id: quickdraw_iigs_font
  title: Apple IIgs QuickDraw II Bitmap Font
  file-extension: fon
  endian: le

seq:
  - id: name_len
    type: u1
    doc: Length of Pascal-style family name in bytes (0–255). #  [oai_citation:0‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
  - id: name
    type: str
    size: name_len
    encoding: ascii
    doc: ASCII/MacRoman family name, immediately following the length byte, not NUL-terminated. #  [oai_citation:1‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
  - id: header
    type: iigs_header
    doc: QuickDraw II header that precedes the embedded Macintosh FONT record. #  [oai_citation:2‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)

instances:
  mac_font:
    pos: (name_len + 1) + (header.offset_to_mf * 2)
    type: mac_font_record
    doc: Little-endian variant of the Macintosh FontRec structure. #  [oai_citation:3‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)

types:
  iigs_header:
    seq:
      - id: offset_to_mf
        type: u2
        doc: Offset (in words) from this field to the Macintosh FONT record; normally 6 (=12 bytes). #  [oai_citation:4‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
      - id: family
        type: u2
        doc: QuickDraw font-family number shared across point sizes. #  [oai_citation:5‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:6‡kreativekorp.com](https://www.kreativekorp.com/miscpages/a2info/filetypes.shtml)
      - id: style
        type: u2
        doc: Design-time style flags (bold =1, italic =2, underline =4, outline =8, shadow =16). #  [oai_citation:7‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
      - id: size_pt
        type: u2
        doc: Nominal point size of this bitmap strike. #  [oai_citation:8‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
      - id: version
        type: u2
        doc: Header format version, usually 0x0101 (v1.1). #  [oai_citation:9‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
      - id: fbr_extent
        type: u2
        doc: Maximum glyph width including kerning (QuickDraw II fbrExtent). #  [oai_citation:10‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)
      - id: high_ow_t_loc
        type: u2
        if: offset_to_mf > 6
        doc: High word of owTLoc for fonts whose tables lie beyond 32 KB. #  [oai_citation:11‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html)

  mac_font_record:
    seq:
      - id: font_type
        type: u2
        doc: Macintosh fontType word describing proportional/fixed and optional tables; ignored on IIgs. #  [oai_citation:12‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:13‡fontforge.org](https://fontforge.org/docs/techref/macformats.html)
      - id: first_char
        type: u2
        doc: Character code of first defined glyph. #  [oai_citation:14‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: last_char
        type: u2
        doc: Character code of last defined glyph. #  [oai_citation:15‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: wid_max
        type: u2
        doc: Maximum advance width among all glyphs, in pixels. #  [oai_citation:16‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html) [oai_citation:17‡leopard-adc.pepas.com](https://leopard-adc.pepas.com/documentation/Carbon/Reference/Font_Manager/Reference/reference.html)
      - id: kern_max
        type: s2
        doc: Most negative left-side bearing (signed pixels). #  [oai_citation:18‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: n_descent
        type: s2
        doc: Originally −descent; later reused as high word of owTLoc on large fonts and ignored on IIgs. #  [oai_citation:19‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:20‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: frect_width
        type: u2
        doc: Width of font rectangle that encloses every glyph (pixels). #  [oai_citation:21‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: frect_height
        type: u2
        doc: Height of font rectangle; equals ascent + descent (pixels). #  [oai_citation:22‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: ow_t_loc
        type: u2
        doc: Offset (words from here) to offset/width table. #  [oai_citation:23‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:24‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: ascent
        type: u2
        doc: Pixels from baseline to top of tallest glyph. #  [oai_citation:25‡leopard-adc.pepas.com](https://leopard-adc.pepas.com/documentation/Carbon/Reference/Font_Manager/Reference/reference.html) [oai_citation:26‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: descent
        type: u2
        doc: Pixels from baseline to bottom of lowest glyph. #  [oai_citation:27‡leopard-adc.pepas.com](https://leopard-adc.pepas.com/documentation/Carbon/Reference/Font_Manager/Reference/reference.html) [oai_citation:28‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: leading
        type: u2
        doc: Recommended inter-line spacing (pixels). #  [oai_citation:29‡leopard-adc.pepas.com](https://leopard-adc.pepas.com/documentation/Carbon/Reference/Font_Manager/Reference/reference.html) [oai_citation:30‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: row_words
        type: u2
        doc: Width of bitmap strike in 16-bit words; each row uses this many words. #  [oai_citation:31‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:32‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: bit_image
        size: row_words * frect_height * 2
        doc: Contiguous glyph bitmap data, row-major, 1 bit = set pixel. #  [oai_citation:33‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:34‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: loc_table
        type: u2
        repeat: expr
        repeat-expr: (last_char - first_char + 3)
        doc: Bitmap-location table; entry n gives bit offset of glyph n in bit_image, plus trailing sentinel. #  [oai_citation:35‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:36‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
      - id: ow_table
        type: u2
        repeat: expr
        repeat-expr: (last_char - first_char + 3)
        doc: Offset/width table: high byte = origin shift, low byte = glyph width; −1 means glyph missing. #  [oai_citation:37‡ciderpress2.com](https://ciderpress2.com/formatdoc/BitmapFont-notes.html) [oai_citation:38‡dev.os9.ca](https://dev.os9.ca/techpubs/mac/Text/Text-250.html)
```