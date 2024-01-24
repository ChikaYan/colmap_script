from pathlib import Path
import numpy as np
import argparse
import shutil
import json


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--scene', type=str, default='ship_re')
    args = parser.parse_args()

    source_dir = Path('/rds/project/rds-qxpdOeYWi78/plenoxels/data/nerf_synthetic') / args.scene
    out_dir = Path('/rds/project/rds-qxpdOeYWi78/plenoxels/data/synthetic_colmap') / args.scene

    img_dir:Path = out_dir / 'images'
    img_dir.mkdir(exist_ok=True, parents=True)

    for im_p in (source_dir / 'train').glob('*'):
        shutil.copy(str(im_p), str(img_dir / f"{int(im_p.stem.strip('r_')):03d}.png"))


    model_dir = out_dir / 'sparse_txt'
    model_dir.mkdir(exist_ok=True, parents=True)

    with (model_dir / 'cameras.txt').open('w') as f:
        f.write('1 SIMPLE_PINHOLE 800 800 1111.1110311937682 400 400')

    (model_dir / 'points3D.txt.txt').open('w')

    with (model_dir / 'images.txt').open('w') as f:
        with (source_dir / 'transforms_train.json').open('r') as file:
            meta = json.load(file)

        




