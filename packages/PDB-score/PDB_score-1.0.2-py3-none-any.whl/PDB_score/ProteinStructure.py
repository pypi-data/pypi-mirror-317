import numpy as np


class ProteinStructure:
    def __init__(self, name, atom_control, atom_treatment):
        """
        初始化蛋白结构类
        :param name: 蛋白名称
        :param atom_control: 真实原子坐标数组
        :param atom_treatment: 预测原子坐标数组
        """
        self.name = name
        self.atom_control = np.array(atom_control)  # 使用 NumPy 数组
        self.atom_treatment = np.array(atom_treatment)
        self.initial_length = self.length()
        self.distances = None  # 延迟计算

    def length(self):
        """
        计算最大的原子数量
        :return: int: 原子数量
        """
        return max(len(self.atom_control), len(self.atom_treatment))

    def self_check(self):
        """
        自检蛋白原子数量是否一致
        :return: 一个 Bool 值，True 表示自检通过
        """
        return len(self.atom_control) == len(self.atom_treatment)

    def same_len(self):
        """
        修建两组坐标，使它们原子数量强制一致，通过裁剪较长的一部分对齐
        """
        min_len = min(len(self.atom_control), len(self.atom_treatment))
        self.atom_control = self.atom_control[:min_len]
        self.atom_treatment = self.atom_treatment[:min_len]

    def calculate_distances(self):
        """
        强制使原子数量一致后，计算两组原子坐标中每个原子之间的欧几里得距离 (向量化优化)
        :return: 一个存储所有距离的 NumPy 数组
        """
        if len(self.atom_control) != len(self.atom_treatment):
            self.same_len()  # 确保两组坐标长度一致

        # 通过NumPy进行矢量化计算
        differences = self.atom_control - self.atom_treatment  # 每一对坐标点的差值
        distances = np.linalg.norm(differences, axis=1)  # 计算模长
        return distances

    def get_distances(self):
        """
        获取距离，如果尚未计算则执行计算
        """
        if self.distances is None:
            self.distances = self.calculate_distances()  # 延迟计算
        return self.distances