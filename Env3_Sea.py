import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def pos_cal(highw:float,loww:float,avgw:float)->str:
    a=loww-1
    b=highw-1
    c=highw+1.5
    if avgw<=a: return "Under"
    elif a<avgw<=b: return "Splash"
    elif b<avgw<=c: return "Tide"
    else: return "Air"
def Env3_1_cal(tempo:float)->int:
    x_T_range = np.arange(-60, 60, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_T = ctrl.Antecedent(x_T_range, 'tempo')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_T["N"]=fuzz.trapmf(x_T_range, [-60,-60, 10, 22])
    x_T["H"]=fuzz.trapmf(x_T_range, [18 ,25, 60, 60])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_T["N"])),consequent=y_E["E"],label="1")
    rule2=ctrl.Rule(antecedent=((x_T["H"])),consequent=y_E["F"],label="2")
    rule=[rule1,rule2]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["tempo"]=tempo
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def Env3_2_cal(dis:float)->int:
    x_D_range = np.arange(0, 1.2, 0.001,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_D = ctrl.Antecedent(x_D_range, 'distance')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_D["S"]=fuzz.trimf(x_D_range, [0.28, 1.2, 1.2])
    x_D["M"] =fuzz.trimf(x_D_range, [0.08, 0.20, 0.32])
    x_D["L"]=fuzz.trimf(x_D_range, [0, 0, 0.12])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_D["S"])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=((x_D["M"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_D["L"])),consequent=y_E["E"],label="3")
    rule=[rule1,rule2,rule3]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["distance"]=dis
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def check(dis:float)->bool:
    return dis<=1.2
def Env3_cal(dis:float,tempo:float,highw:float,loww:float,avgw:float)->int:
    if(not check(dis)): return 0
    pos=pos_cal(highw,loww,avgw)
    if(pos=="Under"): return 3
    elif(pos=="Splash" or pos=="Tide"): return Env3_1_cal(tempo)
    else: return Env3_2_cal(dis)