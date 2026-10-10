# Diamond Ore Screenshot Detector

This Python program finds visible regular diamond ore faces in Minecraft Java Edition screenshots using default textures. It draws labeled boxes, counts matches, and saves an annotated PNG and JSON event summary. It handles screenshots without matches with a zero count and a message.

## Approach

OpenCV template matching compares screenshot patches against a reference face. The detector searches multiple sizes and four rotations, then suppresses overlapping matches. Counting and exporting the matches are the custom behaviors. Match scores measure texture similarity; they are not probabilities.

This is classical computer vision, not a trained neural network. It avoids dataset training for a small, reproducible project. The reference is cropped from the author's single-block screenshot `2026-10-10_11.18.17.png`; that screenshot is a reference example, not independent evaluation data.

## Install and run

From PowerShell in this folder, with Python installed:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe detect.py "samples\2026-10-10_11.21.43.png"
.\.venv\Scripts\python.exe detect.py "samples\2026-10-10_11.21.14.png" "samples\2026-10-10_11.22.03.png"
```

If your shell does not expand wildcards, pass screenshot filenames individually instead. The program accepts multiple filenames. Output goes into `output/`. Use `--threshold 0.8` for stricter matching or `--output another_folder` to change the destination.

## Limitations

The detector counts matching faces, not hidden blocks or guaranteed unique physical blocks. Multiple visible faces can belong to one block. Perspective distortion, shadows, other texture packs, deepslate ore, occlusion, and very small or large faces can reduce accuracy. The initial examples have simple backgrounds and do not establish general gameplay performance. More negative examples, perspective-aware matching, or a trained detector would improve coverage.

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

The reference-source match is a sanity check. The first four other examples were used during development. The last two screenshots were supplied afterward and tested without changing the template, algorithm, or threshold. The mixed-ore output boxes were inspected: both diamond faces were detected and no redstone, emerald, gold, or lapis faces were labeled. This small controlled test does not establish general gameplay accuracy. The close-up miss illustrates perspective distortion.

## Submission

Include the scripts, dependency file, reference template, sample inputs and annotated outputs in a public GitHub repository. Review the results before submitting and describe mistakes honestly. No repository has been published by this starter project.
