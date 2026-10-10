import argparse
import json
from pathlib import Path
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent


def find_ore(image, template, threshold=0.72):
    scale = min(1.0, 1000 / image.shape[1])
    small = cv2.resize(image, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    candidates = []
    for size in np.geomspace(22, min(400, *gray.shape), 65).astype(int):
        resized = cv2.resize(template, (int(size), int(size)), interpolation=cv2.INTER_AREA)
        for rotation in range(4):
            rotated = np.ascontiguousarray(np.rot90(resized, rotation))
            scores = cv2.matchTemplate(gray, rotated, cv2.TM_CCOEFF_NORMED)
            maxima = cv2.dilate(scores, np.ones((9, 9), np.uint8))
            ys, xs = np.where((scores >= threshold) & (scores >= maxima))
            for x, y in zip(xs, ys):
                candidates.append((float(scores[y, x]), int(x), int(y), int(size)))
    selected = []
    for score, x, y, size in sorted(candidates, reverse=True):
        duplicate = False
        for _, a, b, other_size in selected:
            intersection = max(0, min(x+size, a+other_size)-max(x, a)) * max(0, min(y+size, b+other_size)-max(y, b))
            if intersection / min(size*size, other_size*other_size) > 0.35:
                duplicate = True
                break
        if not duplicate:
            selected.append((score, x, y, size))
    return [{'box_xyxy': [round(x/scale), round(y/scale), round((x+s)/scale), round((y+s)/scale)],
             'match_score': round(score, 4)} for score, x, y, s in selected]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('images', nargs='+', type=Path)
    parser.add_argument('--template', type=Path, default=ROOT/'template.png')
    parser.add_argument('--threshold', type=float, default=0.72)
    parser.add_argument('--output', type=Path, default=ROOT/'output')
    args = parser.parse_args()
    if not 0 < args.threshold <= 1:
        parser.error('Threshold must be greater than 0 and at most 1.')
    template = cv2.imread(str(args.template), cv2.IMREAD_GRAYSCALE)
    if template is None:
        parser.error(f'Cannot read template: {args.template}')
    args.output.mkdir(parents=True, exist_ok=True)
    for path in args.images:
        image = cv2.imread(str(path))
        if image is None:
            parser.error(f'Cannot read screenshot: {path}')
        detections = find_ore(image, template, args.threshold)
        for detection in detections:
            x1, y1, x2, y2 = detection['box_xyxy']
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 220, 0), 3)
            cv2.putText(image, f"Diamond ore {detection['match_score']:.2f}",
                        (x1, max(25, y1-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 120, 0), 2)
        title = f'Diamond ore faces: {len(detections)}'
        if not detections:
            title += ' - No ore detected'
        cv2.rectangle(image, (0, 0), (min(850, image.shape[1]), 65), (255, 255, 255), -1)
        cv2.putText(image, title, (15, 42), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        destination = args.output / f'{path.stem}_detected.png'
        if not cv2.imwrite(str(destination), image):
            raise OSError(f'Could not save {destination}')
        (args.output / f'{path.stem}_counts.json').write_text(json.dumps({
            'source': path.name, 'visible_face_count': len(detections),
            'threshold': args.threshold, 'detections': detections}, indent=2), encoding='utf-8')
        print(f'{path.name}: {len(detections)} faces')


if __name__ == '__main__':
    main()
