# Doki Doki Ohayou Sayori — Visual Novel Prototypes

## Overview

This repository records a personal learning project from September to November in 2025: building a branching visual novel first as a custom Windows console program in C, and later rebuilding it as a Ren'Py MVP.

The project began as an experiment in turning a long, branching story into an interactive program. The C version gradually grew from a basic dialogue player into a small data-driven narrative engine with choices, route variables, save files, achievements, and unlockable side stories. I later moved to Ren'Py so that I could spend less time recreating basic visual-novel infrastructure and more time working on story structure, presentation, and interaction design.

The project is now archived as a record of that learning process rather than maintained as a finished game.

## Technical Highlights

### C prototype

- A custom parser reads dialogue and control instructions from external text files instead of hard-coding the entire story in C.
- Branching choices can jump between numbered chapters and update route-related state.
- Manual saving, loading, and autosaving are supported through fifteen save slots.
- Text speed, display behavior, and a pause menu can be configured at runtime.
- An achievement system tracks conditions and unlocks optional side stories.
- A loop guard prevents malformed story routes from running indefinitely.

### Ren'Py MVP

- The story was migrated to Ren'Py labels, menus, and conditional branches.
- Persistent achievement data is retained between sessions.
- Conditional menus unlock additional side stories as achievements are collected.
- The route design includes nine planned endings across several story branches.
- Character sprites, backgrounds, music, and a graphical interface replace the console presentation of the C version.

## Design and Decisions

The two implementations reflect different stages of the same project.

In the C version, I wanted to understand what happens underneath a narrative engine. I created a simple story-file format containing chapter numbers, speakers, dialogue, choices, jump targets, effects, and achievement events. The program interprets these records at runtime and maintains the current narrative state.

This approach was useful for learning, but it also exposed several limitations. As the story expanded, the parser, save format, interface, and story logic all had to be maintained manually. Adding visual presentation would have required even more infrastructure unrelated to the narrative itself.

Ren'Py provided those standard visual-novel features directly. Migrating the project therefore became an exercise in choosing an appropriate abstraction: the C prototype emphasized implementation details and state management, while the Ren'Py version emphasized content organization, branching design, and presentation.

## Repository Structure

```text
.
├── C-V4.2/
│   ├── game4.2.c          # C implementation of the narrative engine
│   ├── story.txt          # Main story data used by the C program
│   ├── playoff_*.txt      # Unlockable side-story data
│   ├── READMEPLEASE.txt   # Original player notes and version history
│   ├── 结局表.xlsx         # Route and ending design notes
│   └── *.png              # Images associated with the C prototype
├── Ren'Py-MVP/
│   ├── script.rpy         # Story flow, choices, and achievement logic
│   ├── gui.rpy            # Ren'Py interface configuration
│   ├── options.rpy        # Project configuration
│   ├── images/            # Character and background images
│   ├── audio/             # Audio used by the MVP
│   └── gui/               # Ren'Py GUI assets
└── README.md
```

Generated files, local saves, caches, and packaged builds are intentionally excluded from version control.

## How to Play the C Version

The C prototype is designed for Windows and uses `windows.h` for console behavior.

### Using an existing executable

If `game4.2.exe` is included in your local copy:

1. Keep the executable in the `C-V4.2` directory together with `story.txt`, the `playoff_*.txt` files, and the other project resources.
2. Read `READMEPLEASE.txt` for the original gameplay notes and content notice.
3. Open a terminal in `C-V4.2` and run:

   ```powershell
   .\game4.2.exe
   ```

Running the program from its own directory is important because it loads story and save files using relative paths.

### Building from source

With GCC or MinGW-w64 installed on Windows:

```powershell
cd C-V4.2
gcc -std=c11 game4.2.c -o game4.2.exe
.\game4.2.exe
```

The program reads and writes files in the current directory. Save files and achievement data created while playing should remain local and are not part of the repository.

## What I Have Learned

- How to represent a branching narrative as data instead of a long sequence of hard-coded output statements.
- How program state connects choices, route variables, saves, achievements, and unlockable content.
- Why input parsing and fixed-size buffers require careful validation in C.
- Why save-file compatibility should be considered before a data structure begins to change frequently.
- How quickly a single source file becomes difficult to maintain as a project grows.
- When a custom implementation is valuable for learning, and when a specialized framework is the better engineering choice.
- How iterative development, debugging, and version history reveal design problems that are difficult to predict at the beginning of a project.

## Statement

This is an unofficial, non-commercial fan-made learning project inspired by *Doki Doki Literature Club*. It is not affiliated with or endorsed by Team Salvato. The original game and its characters belong to their respective rights holders.

AI tools were used during development, particularly to assist with parts of the C implementation and the creation of some visual assets. I designed the project requirements, branching story structure, narrative content, and integration of the different components, and I repeatedly tested and revised the project as it developed. Zhou Feiyang also helped with debugging the C version.

The repository is published to document a programming-learning process, not as a commercial release or an official continuation of the original game. For the current fan-content guidelines, see the [Team Salvato IP Guidelines](https://teamsalvato.com/ip-guidelines).
