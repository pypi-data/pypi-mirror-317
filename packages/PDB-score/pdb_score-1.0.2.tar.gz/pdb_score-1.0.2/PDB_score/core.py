import os
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from Bio.PDB import PDBParser


# 提取中心碳原子坐标
def extract_ca_coordinates(structure):
    ca_coords = [
        residue['CA'].coord
        for model in structure
        for chain in model
        for residue in chain.get_residues()
        if residue.id[0] == ' ' and 'CA' in residue
    ]
    return ca_coords


# 批量解析最多 5000 个 PDB 文件
def parse_pdb_files(directory, batch_size=5000, thread_count=4):
    pdb_path = Path(directory)
    pdb_files = [pdb_file.as_posix() for pdb_file in pdb_path.glob("*.pdb")]
    print(f"Batch size = {batch_size}, Total files = {len(pdb_files)}")
    print(f"Using {thread_count} CPU cores...")


    # 每次处理 batch_size 数量的文件
    all_results = {}
    for i in range(0, len(pdb_files), batch_size):
        batch_files = pdb_files[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1}: {len(batch_files)} files...")

        # 使用多进程处理每个文件
        with Pool(thread_count) as pool:
            batch_results = pool.map(parse_single_pdb_file, batch_files)

        # 将结果保存到总结果字典
        all_results.update(dict(batch_results))

    return all_results


# 单个文件解析，提取 CA 原子坐标
def parse_single_pdb_file(file_path):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(file_path, file_path)
    return os.path.splitext(os.path.basename(file_path))[0], extract_ca_coordinates(structure)




# 优化的 protein 评分计算
def calculate_score(protein, limit):
    limit = float(limit)
    distances = protein.get_distances()

    score = np.sum(distances < limit)
    return int(score / protein.initial_length * 100)