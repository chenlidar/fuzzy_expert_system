import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def check_1(p:float)->bool:
    return p>0.1
def check_2(p:float)->bool:
    return p>0.15

def Env4_1_cal(p:float)->int:
    if(not check_1(p)): return 0
    x_P_range = np.arange(0.1, 100, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P = ctrl.Antecedent(x_P_range, 'density')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P["S"]=fuzz.trimf(x_P_range, [0.1, 0.1, 0.53])
    x_P["M"]=fuzz.trimf(x_P_range, [0.47 ,3.5, 5.3])
    x_P["L"]=fuzz.trapmf(x_P_range, [4.7 ,6, 100,100])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P["S"])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=((x_P["M"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_P["L"])),consequent=y_E["E"],label="3")
    rule=[rule1,rule2,rule3]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["density"]=p
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def Env4_2_cal(p:float)->int:
    if(not check_2(p)): return 0
    x_P_range = np.arange(0.1, 100, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P = ctrl.Antecedent(x_P_range, 'density')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P["S"]=fuzz.trimf(x_P_range, [0.15, 0.15, 0.78])
    x_P["M"]=fuzz.trimf(x_P_range, [0.72 ,4, 7.8])
    x_P["L"]=fuzz.trapmf(x_P_range, [7.2 ,8.5, 100,100])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P["S"])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=((x_P["M"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_P["L"])),consequent=y_E["E"],label="3")
    rule=[rule1,rule2,rule3]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["density"]=p
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def Env4_cal(type:float,p:float)->int:
    if(type=="Water"): return Env4_1_cal(p)
    elif(type=='Solid'): return Env4_2_cal(p)
    else: return 0