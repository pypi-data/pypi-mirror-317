import argparse
import os
import pandas as pd
from .core import parse_pdb_files, calculate_score
from .ProteinStructure import ProteinStructure


def main():
    parser = argparse.ArgumentParser(description="Calculate protein scores based on PDB files.")
    parser.add_argument("-c", "--control", required=True, help="实验值 PDB 文件存放目录")
    parser.add_argument("-t", "--treatment", required=True, help="预测值 PDB 文件存放目录")
    parser.add_argument("-o", "--output", required=True, help="保存分数的输出目录")
    args = parser.parse_args()

    control_dir = args.control
    treatment_dir = args.treatment
    output_dir = args.output

    # 解析 PDB 文件
    atoms_control = parse_pdb_files(control_dir)
    atoms_treatment = parse_pdb_files(treatment_dir)

    # 创建 ProteinStructure 对象
    protein_structures = []
    for file_name in atoms_control.keys():
        if file_name in atoms_treatment:
            protein_structure = ProteinStructure(
                name=file_name,
                atom_control=atoms_control[file_name],
                atom_treatment=atoms_treatment[file_name],
            )
            protein_structures.append(protein_structure)

    protein_scores_list = []
    for protein in protein_structures:
        scores = {}
        for times in range(8):  # 计算8次，阈值分别为 2^0, 2^1,..., 2^7
            limit = 2 ** times
            score = calculate_score(protein, limit)
            scores[f"{limit}A"] = score
        # 求平均
        scores["Average"] = int(sum(scores.values()) / len(scores))
        protein_scores_list.append(  # 将 DataFrame 添加到列表
            pd.DataFrame(scores, index=[protein.name])
        )

    # 保存到 CSV 文件
    protein_scores = pd.concat(protein_scores_list)
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "protein_scores.csv")
    protein_scores.to_csv(output_file)
    print(f"Protein scores saved to: {output_file}")


if __name__ == "__main__":
    main()