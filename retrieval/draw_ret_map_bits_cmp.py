# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import hdf5storage


if __name__ == "__main__":
    all_ret = {}
    roiFeaRetRoot = "./roiFeas"
    sample_arr = np.arange(50, 501, 50)
    fea_list = ['gist', 'vgg16bn', 'inceptionv3', 'resnet50']
    ksh_str, cosdish_str, sdh_str = "02", "06", "10"
    cur_hash_str = ksh_str

    save_pdf_str = "ksh_retrieval_map_bits_cmp.pdf"
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(16, 5))

    # bit_index, bit_str = 0, "8 bits"
    bit_indices, bit_strs = [0, 1, 2], ["8 bits", "16 bits", "32 bits"]
    for ind, (bit_index, bit_str) in enumerate(zip(bit_indices, bit_strs)):
        splits = ["S1", "S2", "S3", "S4", "S5"]
        for ele in fea_list:
            ret_dict = {}
            ttl_split_map = np.zeros((3, 10), dtype=np.float32)
            for split in splits:
                cur_mat_path = os.path.join(roiFeaRetRoot, split, ele, 'TM'+cur_hash_str+'.mat')
                MAPdata = hdf5storage.loadmat(cur_mat_path)
                ttl_split_map += MAPdata['TM'+cur_hash_str]
            ret_dict['sample_num'] = sample_arr
            ret_dict['map'] = ttl_split_map / len(splits)
            all_ret[ele] = ret_dict

        # drawing
        markers = ('o', 'v', '8', 's', 'p', '^', '<', '>')
        colors = ('r', 'b', 'g', 'k', 'm')

        ax = axes[ind]
        ax.set_xlabel('The number of retrieved samples')
        ax.set_ylabel('Mean Average Precision @ ' + bit_str)
        ax.set_xlim(0, 500)
        ax.set_ylim(0.60, 1.00)
        for index, key in enumerate(all_ret):
            ax.plot(all_ret[key]['sample_num'], all_ret[key]['map'][bit_index], label=key, color=colors[index], marker=markers[index])
        ax.legend(loc='lower right')

        plt.tight_layout()
        # plt.show()
    fig.savefig(save_pdf_str)
