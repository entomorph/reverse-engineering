# Entomorph's reverse engineering attempt

This project is dedicated to reverse engineering the 1995 game [Entomorph: Plague of the Darkfall][1], with the goal of understanding its internal workings and documenting its assets.

![world-of-aden-entomorph-plague-of-the-darkfall_3](https://user-images.githubusercontent.com/288227/233727285-208a047a-477c-4246-a763-d77de3105934.jpeg)

## Tools used

- [Ghidra](https://ghidra-sre.org/)
- [x64dbg](https://x64dbg.com/)
- [Kaitai Struct](https://kaitai.io/)
- LLM's

## Phase 1: Disassembly (76% complete)

The initial phase involves disassembling the game's executable and thoroughly documenting the code. Ghidra and ChatGPT 4 are employed to assist in this process, with LLM's being particularly helpful in deciphering decompiled functions.

When a function is not easily comprehensible, x64dbg is used to step through the code for better understanding. However, Ghidra and LLM's have been mostly sufficient for this task.

### Challenges:

- Entomorph was compiled for Windows 3.1 using the Watcom compiler, resulting in a 32-bit executable. Ghidra does not support the Watcom calling convention, so manual adjustments to the calling convention for each function are necessary.
- Ghidra 10.2.X does not support function typedefs with custom calling conventions, complicating the understanding of function pointers.
- The game employs a custom memory allocator, making it difficult to comprehend the memory layout.
- Globals are ubiquitous and require documentation, with some needing to be merged into structs.

## Phase 2: Assets documentation (30% complete)

The second phase focuses on documenting the game's assets and developing a tool to visualize them. Kaitai Struct is used to facilitate this process.

### VOICE

Located in the VOICE directory, these files contain the game's voice audio. They are 8-bit unsigned PCM audio files with a 22050 Hz sample rate and 1 channel (mono). To play them, use:

```
ffplay -autoexit -f u8 -ar 22050 -ac 2 5_1.RAW
```

### WORLDS

Check the [WORLDS.md](WORLDS.md) file for more information.

### CINE

The game's cinematics are stored in the CINE directory as Smacker video files, which can be played using VLC.

### ENGINE

The `ENGINE` directory contains .LIB files used by the game's engine. See the [LIBs documentation](LIBs.md) file for more information.

### SFX

#### .BNK

.BNK files serve as sound databases within the game, detailing attributes for how each sound should be executed by the engine. Interestingly, the game engine disregards the first 20 entries for reasons not made clear. Each entry within the .BNK file maps to a .MEL file by specifying the file number along with other playback attributes. The structure of a .BNK file is as follows:

```ksy
meta:
  id: bnk_file
  file-extension: bnk
  endian: le
seq:
  - id: audio_entries
    type: audio_entry
    repeat: eos
types:
  audio_entry:
    seq:
      - id: audio_number
        type: u4
        doc: The number corresponding to a .MEL audio file.
      - id: audio_size
        type: u4
      - id: file_buffer
        type: u4
      - id: unknown
        type: u4
      - id: playback_rate
        type: u4
      - id: playback_rate_upper
        type: u4
      - id: playback_rate_lower
        type: u4
      - id: loop_count
        type: u4
      - id: volume_adjustment_offset
        type: u4
```

Note: The final entry in the .BNK file may be invalid or serve as a placeholder.

#### .MEL

.MEL (Melody?) files contain audio data in an 8-bit unsigned PCM format. Although the playback sample rate is specified within the corresponding .BNK file, it generally defaults to 11025 Hz. To play a .MEL file outside the game engine, the following command can be used:

```
ffplay -autoexit -f u8 -ar 11025 -ac 2 155.MEL
```

### GPLS

Entomorph features a bespoke interpreted programming language!

Abbreviated as "GPL" - which could stand for "General Programming Language" or "Game Programming Language". These GPL files consist of bytecodes that a built-in interpreter within the game processes. This design choice suggests an ambition to repurpose the engine for subsequent games, highlighting its adaptability and potential for future development.

This system's efficiency is demonstrated by the fact that the initial patch for Entomorph consisted solely of updated GPL files.

[1]: https://en.wikipedia.org/wiki/Entomorph:_Plague_of_the_Darkfall
