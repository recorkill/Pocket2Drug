"""
Generate pdbqt files from smi files
"""
import argparse
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import subprocess


def get_args():
    parser = argparse.ArgumentParser("python")

    parser.add_argument("-in_dir",
                        required=False,
                        default="../../../p2d_results_selfie/cv_results/cross_val_fold_0/val_pockets_sample_clustered_smi/",
                        help="directory of yaml files after being selected by clustering algorithm")

    parser.add_argument("-out_dir",
                        required=False,
                        default="../../../p2d_results_selfie/cv_results/cross_val_fold_0/val_pockets_sample_clustered_pdbqt/",
                        help="directory of yaml files where each yaml is a list of sampled SMILES")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    in_dir = args.in_dir
    out_dir = args.out_dir
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    pocket_subset_files = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]

    for pocket_subset_file in tqdm(pocket_subset_files):
        pocket_name = pocket_subset_file.split('.')[0]
        
        # make a folder for each pocket
        pocket_out_dir = join(out_dir, pocket_name)
        if not os.path.exists(pocket_out_dir):
            os.makedirs(pocket_out_dir)

        # input .smi file name
        in_file = join(in_dir, pocket_subset_file)

        # run openbabel to convert files
        p = subprocess.run(
            'obabel' + 
            ' -ismi {}'.format(in_file) +
            ' -opdbqt' +
            ' -O {}'.format(join(pocket_out_dir, pocket_name + '-.pdbqt')) +
            ' -h -m --gen3D',
            shell=True,
            capture_output=True
        )

        if p.returncode != 0:
            print('Something went wrong! pocket: ', pocket_name)