import os
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from Bio.PDB import PDBParser


# 提取中心碳原子坐标
def extract_ca_coordinates(structure):
    ca_coords = []
    for model in structure:
        for chain in model:
            for residue in chain.get_residues():
                if residue.id[0] == ' ' and 'CA' in residue:
                    ca_coords.append(residue['CA'].coord)
    return ca_coords


# 单个文件解析
def parse_single_pdb_file(file_path):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(file_path, file_path)
    return os.path.splitext(os.path.basename(file_path))[0], extract_ca_coordinates(structure)


# 多进程解析多个文件
def parse_pdb_files(directory):
    pdb_path = Path(directory)
    pdb_files = [pdb_file.as_posix() for pdb_file in pdb_path.glob("*.pdb")]

    with Pool() as pool:
        results = pool.map(parse_single_pdb_file, pdb_files)
    return dict(results)


# 优化的 protein 评分计算
def calculate_score(protein, limit):
    limit = float(limit)
    protein.same_len()
    distances = np.array(protein.calculate_distances())
    score = np.sum(distances < limit)
    return int(score / protein.length() * 100)