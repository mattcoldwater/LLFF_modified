import os
import subprocess



# $ DATASET_PATH=/path/to/dataset

# $ colmap feature_extractor \
#    --database_path $DATASET_PATH/database.db \
#    --image_path $DATASET_PATH/images

# $ colmap exhaustive_matcher \
#    --database_path $DATASET_PATH/database.db

# $ mkdir $DATASET_PATH/sparse

# $ colmap mapper \
#     --database_path $DATASET_PATH/database.db \
#     --image_path $DATASET_PATH/images \
#     --output_path $DATASET_PATH/sparse

# $ mkdir $DATASET_PATH/dense
def run_colmap(basedir, match_type):
    
    logfile_name = os.path.join(basedir, 'colmap_output.txt')
    logfile = open(logfile_name, 'w')
    
    ###############################
    feature_extractor_args = [
        'colmap', 'feature_extractor', 
            '--database_path', os.path.join(basedir, 'database.db'), 
            '--image_path', os.path.join(basedir, 'images'),
            '--ImageReader.single_camera', '1',
            # '--SiftExtraction.use_gpu', '0',
    ]
    feat_output = ( subprocess.check_output(feature_extractor_args, universal_newlines=True) )
    logfile.write(feat_output)
    print('Features extracted')
    ###############################

    ###############################
    exhaustive_matcher_args = [
        'colmap', match_type, 
            '--database_path', os.path.join(basedir, 'database.db'), 
    ]

    match_output = ( subprocess.check_output(exhaustive_matcher_args, universal_newlines=True) )
    logfile.write(match_output)
    print('Features matched')
    ###############################
    
    ###############################
    p = os.path.join(basedir, 'sparse')
    if not os.path.exists(p):
        os.makedirs(p)

    mapper_args = [
        'colmap', 'mapper',
            '--database_path', os.path.join(basedir, 'database.db'),
            '--image_path', os.path.join(basedir, 'images'),
            '--output_path', os.path.join(basedir, 'sparse'), # --export_path changed to --output_path in colmap 3.6
            '--Mapper.num_threads', '16',
            '--Mapper.init_min_tri_angle', '4',
            '--Mapper.multiple_models', '0',
            '--Mapper.extract_colors', '0',
    ]

    map_output = ( subprocess.check_output(mapper_args, universal_newlines=True) )
    logfile.write(map_output)
    print('Sparse map created')
    ###############################

    ##################################################################

    ###############################
    p = os.path.join(basedir, 'dense')
    if not os.path.exists(p):
        os.makedirs(p)
    ###############################

    ###############################
    image_undistorter_args = [
        'colmap', 'image_undistorter',
            '--image_path', os.path.join(basedir, 'images'),
            '--input_path', os.path.join(basedir, 'sparse/0'),
            '--output_path', os.path.join(basedir, 'dense'),
            '--output_type', 'COLMAP',
            '--max_image_size', '2000'
    ]

    image_undistorter_output = ( subprocess.check_output(image_undistorter_args, universal_newlines=True) )
    logfile.write(image_undistorter_output)
    print('image_undistorter')
    ###############################

    ###############################
    patch_match_stereo_args = [
        'colmap', 'patch_match_stereo',
            '--workspace_path', os.path.join(basedir, 'dense'),
            '--workspace_format', 'COLMAP',
            '--PatchMatchStereo.geom_consistency', 'true'
    ]

    patch_match_stereo_output = ( subprocess.check_output(patch_match_stereo_args, universal_newlines=True) )
    logfile.write(patch_match_stereo_output)
    print('patch_match_stereo')
    ###############################

    ###############################
    stereo_fusion_args = [
        'colmap', 'stereo_fusion',
            '--workspace_path', os.path.join(basedir, 'dense'),
            '--workspace_format', 'COLMAP',
            '--input_type', 'geometric',
            '--output_path', os.path.join(basedir, 'dense/fused.ply'),
    ]

    stereo_fusion_output = ( subprocess.check_output(stereo_fusion_args, universal_newlines=True) )
    logfile.write(stereo_fusion_output)
    print('stereo_fusion')
    ###############################

    ###############################
    poisson_mesher_args = [
        'colmap', 'poisson_mesher',
            '--input_path', os.path.join(basedir, 'dense/fused.ply'),
            '--output_path', os.path.join(basedir, 'dense/meshed-poisson.ply'),
    ]

    poisson_mesher_output = ( subprocess.check_output(poisson_mesher_args, universal_newlines=True) )
    logfile.write(poisson_mesher_output)
    print('poisson_mesher')
    ###############################

    ###############################
    delaunay_mesher_args = [
        'colmap', 'delaunay_mesher',
            '--input_path', os.path.join(basedir, 'dense'),
            '--output_path', os.path.join(basedir, 'dense/meshed-delaunay.ply'),
    ]

    delaunay_mesher_output = ( subprocess.check_output(delaunay_mesher_args, universal_newlines=True) )
    logfile.write(delaunay_mesher_output)
    print('delaunay_mesher')
    ###############################

    ###############################
    model_converter_args = [
        'colmap', 'model_converter',
            '--input_path', os.path.join(basedir, 'sparse/0'),
            '--output_path', os.path.join(basedir, 'sparse/0'),
            '--output_type', 'TXT'
    ]

    model_converter_output = ( subprocess.check_output(model_converter_args, universal_newlines=True) )
    logfile.write(model_converter_output)
    print('model_converter')
    ###############################

    ##################################################################
    
    logfile.close()
    print( 'Finished running COLMAP, see {} for logs'.format(logfile_name) )


