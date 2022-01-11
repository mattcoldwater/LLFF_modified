from llff.poses.pose_utils import gen_poses
import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--match_type', type=str, 
					default='exhaustive_matcher', help='type of matcher used.  Valid options: \
					exhaustive_matcher sequential_matcher.  Other matchers not supported at this time')
parser.add_argument('--dense', action='store_true')
parser.add_argument('--colmap_dir', type=str, default='/content/drive/My Drive/nerfies/captures/pizza_salad/colmap/1x',
					help='input scene directory')
parser.add_argument('--rgb_dir', type=str, default='/content/drive/My Drive/nerfies/captures/pizza_salad/rgb/1x',
					help='input scene directory')
args = parser.parse_args()

if args.match_type != 'exhaustive_matcher' and args.match_type != 'sequential_matcher':
	print('ERROR: matcher type ' + args.match_type + ' is not valid.  Aborting')
	sys.exit()

if __name__=='__main__':
    gen_poses(args.colmap_dir, args.match_type, img_dir=args.img_dir, dense=args.dense)