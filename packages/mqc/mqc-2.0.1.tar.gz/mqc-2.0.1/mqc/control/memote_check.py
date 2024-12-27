from cobra.io import read_sbml_model
from scipy.optimize import linprog
import numpy as np
from scipy.optimize import linprog
from cobra.flux_analysis import flux_variability_analysis
from pathlib import Path
import sys 
from memote.support import consistency, consistency_helpers
from memote.suite.tests import test_consistency
import time 

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]
print('FILE:',FILE,'ROOT:', ROOT)
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT)) # add ROOT to PATH

from mqc.utils import *


def get_stoichiometry_matrix(model):
    """
    从 cobra 模型构造标准化的化学计量矩阵 S。
    :param model: cobra.Model 对象
    :return: S (numpy.ndarray)
    """
    metabolites = model.metabolites
    reactions = model.reactions

    # 初始化化学计量矩阵 S
    S = np.zeros((len(metabolites), len(reactions)))

    # 填充矩阵
    for j, reaction in enumerate(reactions):
        for metabolite, coefficient in reaction.metabolites.items():
            i = metabolites.index(metabolite)
            S[i, j] = coefficient

    return S



# def verify_stoichiometric_consistency(model):
#     """
#     验证化学计量学一致性（使用线性规划法）。
#     返回结果是否一致。
#     """
#     S = get_stoichiometry_matrix(model)
#     m, n = S.shape

#     c = np.ones(m)  # 目标函数：最小化代谢物分子量之和
#     A_eq = S.T      # 等式约束：化学计量矩阵
#     b_eq = np.zeros(n)  # 等式右侧全为零
#     bounds = [(1e-6, None) for _ in range(m)]  # 每个分子量为正

#     try:
#         result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
#         if result.success:
#             return True
#         else:
#             print(f"线性规划失败: {result.message}")
#             return False
#     except Exception as e:
#         print(f"发生错误: {e}")
#         return False
def verify_stoichiometric_consistency(model):
    """
    验证化学计量学一致性（使用线性规划法），并返回化学计量学不一致的反应 ID。
    :param model: cobra.Model 对象
    :return: 一致性状态（bool）和不一致的反应 ID 列表
    """
    S = get_stoichiometry_matrix(model)  # 构造化学计量矩阵
    m, n = S.shape

    c = np.ones(m)  # 目标函数：最小化代谢物分子量之和
    A_eq = S.T      # 等式约束：化学计量矩阵
    b_eq = np.zeros(n)  # 等式右侧全为零
    bounds = [(1e-6, None) for _ in range(m)]  # 每个分子量为正

    try:
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        if result.success:
            # 如果成功，返回一致性状态和空列表
            return True, []
        else:
            print(f"线性规划失败: {result.message}")

            # 确定不一致反应：无解时检查等式约束不满足的反应
            inconsistent_reactions = []
            for j in range(n):
                reaction_flux = S[:, j] @ result.x if result.x is not None else None
                if reaction_flux is None or abs(reaction_flux) > 1e-6:
                    inconsistent_reactions.append(model.reactions[j].id)
            return False, inconsistent_reactions
    except Exception as e:
        print(f"发生错误: {e}")
        return False, []



def detect_unconserved_metabolites(model):
    """
    使用 MILP 检测不可守恒代谢物，添加下界约束以避免无界问题。
    """
    S = get_stoichiometry_matrix(model)
    m, n = S.shape

    # 构建 MILP 问题
    c = [-1] * m  # 目标函数：最大化质量守恒向量的正分量
    A_eq = S.T  # 等式约束
    b_eq = [0] * n  # 等式右侧
    bounds = [(1e-6, None) for _ in range(m)]  # 添加正值下界

    try:
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        if not result.success:
            print(f"线性规划失败: {result.message}")
            return []

        # 解析结果
        conservation_vector = result.x
        unconserved_metabolites = [
            model.metabolites[i].id for i, value in enumerate(conservation_vector) if value < 1e-6
        ]
        return unconserved_metabolites

    except Exception as e:
        print(f"线性规划发生错误: {e}")
        return []





def detect_inconsistent_minimal_net_stoichiometries(model):
    """
    检测不一致的最小净化学计量。
    """
    S = get_stoichiometry_matrix(model)  # 构造化学计量矩阵
    print("化学计量矩阵形状:", S.shape)  # 确保其为二维

    # 计算化学计量矩阵的左零空间
    try:
        null_space = np.linalg.svd(S)[2]
    except np.linalg.LinAlgError as e:
        print("SVD 计算错误:", e)
        return []

    # 检测不一致的反应
    inconsistent_reactions = []
    for row in null_space:
        if any(row > 0) and any(row < 0):
            inconsistent_reactions.append(row)

    return inconsistent_reactions





def detect_elementary_leakage_modes(model):
    """
    使用 ScrumPy 检测基本泄漏模式 (Elementary Leakage Modes, ELMs)。

    基于扩展化学计量矩阵的线性规划方法，逐一优化伪反应通量，检测泄漏模式。

    Parameters
    ----------
    model : scrumpy.Model
        ScrumPy 格式的代谢网络模型。

    Returns
    -------
    leakage_modes : list of list
        每个泄漏模式是一个反应 ID 的列表。
    """
    # 获取化学计量矩阵
    stoich_matrix = model.stoich_matrix()  # 返回化学计量矩阵 S
    metabolites = model.metabolites()     # 获取代谢物列表
    reactions = model.reactions()         # 获取反应列表

    # 扩展化学计量矩阵：为每个代谢物添加一个伪反应
    num_metabolites, num_reactions = stoich_matrix.shape
    extended_stoich = stoich_matrix.copy()
    for i, met in enumerate(metabolites):
        # 为每个代谢物添加一个伪反应
        extended_stoich.add_reaction(f"Leak_{met}", {met: 1})

    # 初始化泄漏模式列表
    leakage_modes = []

    # 逐一优化伪反应的通量
    for i, met in enumerate(metabolites):
        # 设置目标函数：最小化当前伪反应通量
        objective = {f"Leak_{met}": 1}
        solution = model.optimize(objective)

        # 检查伪反应的最优值是否显著大于 0
        if solution[f"Leak_{met}"] > 1e-6:
            # 提取活跃的原反应（非伪反应）
            active_reactions = [
                rxn for rxn in reactions
                if abs(solution[rxn]) > 1e-6
            ]
            leakage_modes.append(active_reactions)

    return leakage_modes

   



def detect_unbalance_rxn(model):
    """"""
    unbalance_rxn = []
    for rxn in model.reactions:
        if rxn not in model.boundary and 'biomass' not in rxn.id.lower():
            if len(rxn.check_mass_balance()) != 0:
                unbalance_rxn.append(rxn.id)
    return unbalance_rxn

def detect_connectivity_metabolites(model):
    """"""
    connectivity_metabolites = []
    # 遍历模型中的所有代谢物
    for metabolite in model.metabolites:
        # 检查代谢物是否参与了任何反应
        if len(metabolite.reactions) == 0:
            connectivity_metabolites.append(metabolite)
    return connectivity_metabolites 

def analyze_flux_variability(model):
    """
    在不更改默认约束的情况下运行通量变化分析 (FVA)。
    从 FVA 结果中确定那些承载通量等于模型最大或最小通量的反应。
    
    :param model: cobra.Model 对象
    :return: 两个列表，分别是达到最大通量和最小通量的反应
    """
    # 运行 FVA 分析
    fva_results = flux_variability_analysis(model, fraction_of_optimum=1.0)

    # 存储达到模型最大或最小通量的反应
    max_flux_reactions = []
    min_flux_reactions = []

    # 遍历 FVA 结果，检查每个反应的通量范围
    for reaction_id, flux_range in fva_results.iterrows():
        min_flux, max_flux = flux_range['minimum'], flux_range['maximum']
        reaction = model.reactions.get_by_id(reaction_id)

        # 获取每个反应的默认上下界
        reaction_max_bound = reaction.upper_bound
        reaction_min_bound = reaction.lower_bound

        # 如果反应通量等于模型最大或最小通量
        if max_flux >= reaction_max_bound:
            max_flux_reactions.append((reaction.id, reaction.reaction, max_flux))
        if min_flux <= reaction_min_bound:
            min_flux_reactions.append((reaction.id, reaction.reaction, min_flux))

    return max_flux_reactions, min_flux_reactions

import functools
import inspect
def monitor_functions(module):
    """
    Automatically wrap all functions in a module to monitor execution time.
    """
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            setattr(module, name, time_it(obj))  # Wrap the function with the decorator

# Decorator to measure execution time
def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper
def main():
    
    # 输入SBML文件路径
    # file_path = input("请输入SBML文件路径：").strip()
    file_path = '/home/dengxg/project/mqc/mqc/local_test_data/bigg_data/iML1515.xml'
    model = read_sbml_model(file_path)
    print(f"模型 {model.id} 加载成功，包含 {len(model.reactions)} 个反应和 {len(model.metabolites)} 个代谢物。")

    # 1. 验证化学计量学一致性 -- Stoichiometric Consistency
    is_consistent = consistency.check_stoichiometric_consistency(model)
    print(f"化学计量学一致性检测结果：{'通过' if is_consistent else '不一致'}")

    # 2. 检测不可守恒代谢物 -- Unconserved Metabolites
    unconserved_metabolites = []
    if not is_consistent:
        unconserved_metabolites = get_ids(consistency.find_unconserved_metabolites(model))
    print(f"检测到 {len(unconserved_metabolites)} 个不可守恒代谢物")

    # 3. 检测不一致的最小净化学计量 -- Minimal Inconsistent Net Stoichiometries
    # 仅报告并考虑10个非保守代谢物，以避免计算时间过长
    t1=time.time()
    inconsistent_min_stoichiometry = [
            get_ids(mets)
            for mets in consistency.find_inconsistent_min_stoichiometry(model)
        ]
    print(f"检测到 {len(inconsistent_min_stoichiometry)} 个不一致的最小净化学计量反应:{inconsistent_min_stoichiometry}")
    t2=time.time()
    print(f"detect_inconsistent_minimal_net_stoichiometries 耗时：{t2-t1}")
    # 4. 检测基本泄漏模式
    # leakage_modes = detect_elementary_leakage_modes(model)
    # if leakage_modes:
    #     print(f"检测到 {len(leakage_modes)} 个基本泄漏模式：")
    #     for idx, mode in enumerate(leakage_modes, start=1):
    #         print(f"模式 {idx}: {mode}")
    # else:
    #     print("未检测到基本泄漏模式。")

    internal_rxns = consistency_helpers.get_internals(model)
    # Mass Balance 
    mass_unbalanced_reactions = get_ids(consistency.find_mass_unbalanced_reactions(internal_rxns))
    print(f"检测到 {len(mass_unbalanced_reactions)} 个不平衡反应：{mass_unbalanced_reactions}")

    # Charge Balance
    charge_unbalanced_reactions = get_ids(consistency.find_charge_unbalanced_reactions(internal_rxns))
    print(f"检测到 {len(charge_unbalanced_reactions)} 个不电荷不守恒反应：{charge_unbalanced_reactions}")

    # Metabolite Connectivity
    disconnected_metabolites = get_ids(consistency.find_disconnected(model))
    print(f"检测到 {len(disconnected_metabolites)} 个不连通的代谢物：{disconnected_metabolites}")

    # Unbounded Flux In Default Medium
    ann = {}
    (
        unbounded_rxn_ids,
        fraction,
        _,
    ) = consistency.find_reactions_with_unbounded_flux_default_condition(model)
    ann["data"] = unbounded_rxn_ids
    ann["metric"] = fraction
    print(f"检测到 {len(unbounded_rxn_ids)} 个反应的通量在默认条件下无界")
    print(
        """ A fraction of {:.2%} of the non-blocked reactions (in total {}
        reactions) can carry unbounded flux in the default model
        condition. Unbounded reactions may be involved in
        thermodynamically infeasible cycles: {}""".format(
            ann["metric"], len(ann["data"]), truncate(ann["data"])
        )
    )

if __name__ == "__main__":
    monitor_functions(sys.modules[__name__])
    main()
