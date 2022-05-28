import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def check():
    pass
def Env1_cal(water:float,humidity:float)->int:
    check()
    x_W_range = np.arange(0, 1, 0.01,np.float32)
    x_H_range = np.arange(0, 1, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    # 定义模糊控制变量
    x_W = ctrl.Antecedent(x_W_range, 'water')
    x_H = ctrl.Antecedent(x_H_range, 'humidity')
    y_E = ctrl.Consequent(y_E_range, 'env')
    # 隶属度函数
    x_W["NL"]=fuzz.trimf(x_W_range, [0.00, 0.00, 0.35])
    x_W["O"] =fuzz.trimf(x_W_range, [0.35, 0.60, 0.90])
    x_W["F"] =fuzz.trimf(x_W_range, [0.85, 1.00, 1.00])
    x_H["D"] =fuzz.trimf(x_H_range, [0.00, 0.00, 0.25])
    x_H["LD"]=fuzz.trimf(x_H_range, [0.15, 0.30, 0.45])
    x_H["LW"]=fuzz.trimf(x_H_range, [0.35, 0.50, 0.65])
    x_H["W"] =fuzz.trimf(x_H_range, [0.55, 0.70, 0.85])
    x_H["VW"]=fuzz.trimf(x_H_range, [0.75, 1.00, 1.00])
    y_E["A"] =fuzz.trimf(y_E_range, [1, 1, 2])
    y_E["B"] =fuzz.trimf(y_E_range, [1, 2, 3])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    # 解模糊器
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_W["NL"] & x_H["D"])),consequent=y_E["A"],label="1")
    rule2=ctrl.Rule(antecedent=((x_W["NL"] & x_H["LD"])),consequent=y_E["B"],label="2")
    rule3=ctrl.Rule(antecedent=((x_W["NL"] & x_H["LW"])),consequent=y_E["B"],label="3")
    rule4=ctrl.Rule(antecedent=((x_W["O"] & x_H["LD"])),consequent=y_E["C"],label="4")
    rule5=ctrl.Rule(antecedent=((x_W["O"] & x_H["LW"])),consequent=y_E["C"],label="5")
    rule6=ctrl.Rule(antecedent=((x_W["O"] & x_H["W"])),consequent=y_E["C"],label="6")
    rule7=ctrl.Rule(antecedent=((x_W["O"] & x_H["VW"])),consequent=y_E["A"],label="7")
    rule8=ctrl.Rule(antecedent=((x_W["F"])),consequent=y_E["A"],label="8")
    rule9=ctrl.Rule(antecedent=((x_W["NL"] & x_H["W"])),consequent=y_E["A"],label="9")
    rule10=ctrl.Rule(antecedent=((x_W["NL"] & x_H["VW"])),consequent=y_E["A"],label="10")
    rule11=ctrl.Rule(antecedent=((x_W["O"] & x_H["D"])),consequent=y_E["A"],label="11")
    rule=[rule1,rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["water"]=water
    sim.input["humidity"]=humidity
    sim.compute()
    env=sim.output["env"]
    return round(env)