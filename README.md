# Diamond Ore Detector

This Python program finds visible regular diamond ore faces in Minecraft Java Edition screenshots and images using default textures. It draws labeled boxes, counts matches, and saves an annotated PNG and JSON event summary. It handles screenshots without matches with a zero count and a message.

## Model:

OpenCV template matching compares screenshot patches against a reference face. The program searches multiple sizes and four rotations, then suppresses overlapping matches. Counting and exporting the matches are the custom behaviors.

## Install and run

In PowerShell with Python installed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe detect.py "samples\2026-10-10_11.21.43.png"
.\.venv\Scripts\python.exe detect.py "samples\2026-10-10_11.21.14.png" "samples\2026-10-10_11.22.03.png"
```
Or if you want to try your own:
```powershell
.\.venv\Scripts\python.exe detect.py "C:\path\to\your\screenshot.png"
```

If it doesn't expand wildcards, pass the screenshot filenames individually instead. The program should accept multiple filenames. Output goes into `output/`. Use `--threshold 0.8` for stricter matching or `--output another_folder` to change destinations.

## Limitations

The detector counts matching faces, not hidden blocks or guaranteed unique physical blocks. Multiple visible faces can belong to one block. Perspective distortion, shadows, other texture packs, deepslate ore, and very small or large faces can reduce accuracy. The initial examples have simple backgrounds and do not establish general gameplay performance.

## Observed example results

Tested with OpenCV 5.0.0.93 and NumPy 2.3.5 at the default 0.72 threshold:

| Screenshot | Visible blocks | Detected faces |
| --- | ---: | ---: |
| 11.18.17 (reference source) | 1 | 1 |
| 11.19.14 (angled close-up) | 1 | 0 |
| 11.21.14 (distant group) | 5 | 5 |
| 11.21.43 (close group) | 5 | 5 |
| 11.22.03 (empty background) | 0 | 0 |
| 11.32.09 (new three-block arrangement) | 3 | 3 |
| 11.31.39 (diamond mixed with other ores) | 2 diamond | 2 |

## Improvement

An improvement I would make to this program would be accurate detection of more viewing angles of the diamond ore. This program is good at capturing straight-on faces but adding more reference angles could help the program accurately recognize distorted faces.

