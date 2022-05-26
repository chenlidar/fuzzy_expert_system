import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def check(tempo:float,dtempo:float)->bool:
    return tempo<2.5 and dtempo>10
def Env2_cal(saturate:float,tempo:float,dtempo:float)->int:
    if(not check(tempo,dtempo)): return 0
    x_S_range = np.arange(0, 1, 0.01,np.float32)
    x_T_range = np.arange(-60, 2.5, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    # 定义模糊控制变量
    x_S = ctrl.Antecedent(x_S_range, 'saturate')
    x_T = ctrl.Antecedent(x_T_range, 'tempo')
    y_E = ctrl.Consequent(y_E_range, 'env')
    # 隶属度函数
    x_S["M"] =fuzz.trimf(x_S_range, [0.00, 0.40, 0.7])
    x_S["H"]=fuzz.trimf(x_S_range, [0.50, 1.00, 1.00])
    x_T["LC"]=fuzz.trimf(x_T_range, [-4, 0, 2.5])
    x_T["C"] =fuzz.trimf(x_T_range, [-9, -5, -2])
    x_T["VC"]=fuzz.trapmf(x_T_range, [-60 ,-60, -10, -7])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    # 解模糊器
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_S["M"] & x_T["LC"])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=((x_S["M"] & x_T["C"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_S["M"] & x_T["VC"])),consequent=y_E["D"],label="3")
    rule4=ctrl.Rule(antecedent=((x_S["H"] & x_T["LC"])),consequent=y_E["D"],label="4")
    rule5=ctrl.Rule(antecedent=((x_S["H"] & x_T["C"])),consequent=y_E["E"],label="5")
    rule6=ctrl.Rule(antecedent=((x_S["H"] & x_T["VC"])),consequent=y_E["E"],label="6")
    rule=[rule1,rule2,rule3,rule4,rule5,rule6]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["saturate"]=saturate
    sim.input["tempo"]=tempo
    sim.compute()
    env=sim.output["env"]
    return round(env)