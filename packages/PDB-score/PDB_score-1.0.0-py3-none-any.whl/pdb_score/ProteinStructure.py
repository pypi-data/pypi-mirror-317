# 定义蛋白结构类
class ProteinStructure:
    def __init__(self, name, atom_control, atom_treatment):
        """
        初始化蛋白结构类
        :param name: 蛋白名称
        :param atom_control: 真实原子坐标数组
        :param atom_treatment: 预测原子坐标数组
        """
        self.name = name
        self.atom_control = atom_control
        self.atom_treatment = atom_treatment

    def length(self):
        """
        计算最大的原子数量
        :return: int: 原子数量
        """
        if len(self.atom_control) > len(self.atom_treatment):
            return len(self.atom_control)
        else:
            return len(self.atom_treatment)

    def name(self):
        """
        返回蛋白名称
        :return: str: 蛋白名称
        """
        return self.name

    def self_check(self):
        """
        自检蛋白原子数量是否一致
        :return: 一个 Bool 值，True 表示自检通过
        """
        if len(self.atom_control) != len(self.atom_treatment):
            return False
        else:
            return True

    def same_len(self):
        """
        修建两组坐标，使它们原子数量强制一致，通过裁剪较长的一部分对齐
        """
        if len(self.atom_control) > len(self.atom_treatment):
            # 裁剪 atom_control 的长度到与 atom_treatment 一致
            self.atom_control = self.atom_control[:len(self.atom_treatment)]
        else:
            # 裁剪 atom_treatment 的长度到与 atom_control 一致
            self.atom_treatment = self.atom_treatment[:len(self.atom_control)]

    def calculate_distances(self):
        """
        计算两组原子坐标中每个原子之间的欧几里得距离
        :return: 一个存储所有距离的列表
        """
        if len(self.atom_control) != len(self.atom_treatment):
            raise ValueError("两组原子坐标的数量不一致，无法比较")

        distances = []
        for atom_ctrl, atom_treat in zip(self.atom_control, self.atom_treatment):
            distance = ((atom_ctrl[0] - atom_treat[0]) ** 2 +
                        (atom_ctrl[1] - atom_treat[1]) ** 2 +
                        (atom_ctrl[2] - atom_treat[2]) ** 2) ** 0.5
            distances.append(distance)

        return distances