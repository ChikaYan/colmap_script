from poses.pose_utils import gen_poses
import sys
import cv2
from pathlib import Path
import imageio
import shutil

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--match_type', type=str, 
					default='exhaustive_matcher', help='type of matcher used.  Valid options: \
					exhaustive_matcher sequential_matcher.  Other matchers not supported at this time')
parser.add_argument('--scenedir', type=str,
                    help='input scene directory, raw images are at [scenedir]/raw')
parser.add_argument('--downscale', type=int, default=1)
parser.add_argument('--no_rerun_colmap', action='store_true', default=False)
args = parser.parse_args()

if args.match_type != 'exhaustive_matcher' and args.match_type != 'sequential_matcher':
	print('ERROR: matcher type ' + args.match_type + ' is not valid.  Aborting')
	sys.exit()

if __name__=='__main__':
	# downscale images
    scene_dir = Path(args.scenedir)
    raw_img_dir = scene_dir / 'raw'
    img_dir = scene_dir / 'images'
	img_dir.mkdir(exist_ok=True, parents=True)

	H, W, _ = imageio.imread(str(next(raw_img_dir.glob('*')))).shape
	tH, tW = H // args.downscale, W // args.downscale

	for im_p in raw_img_dir.glob('*'):
		im = imageio.imread(str(im_p))
		im = cv2.resize(im, [tH, tW])
		imageio.imwrite(str(img_dir / f'{im_p.stem}.png' ), im)


	if not args.no_rerun_colmap:
		if (scene_dir / 'sparse').exists():
			shutil.rm_tree(str(scene_dir / 'sparse'))
    
    gen_poses(str(img_dir), args.match_type)