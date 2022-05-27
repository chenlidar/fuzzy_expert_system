import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def check_1(p:float,dw:float)->bool:
    return p>0.2 and dw>0.4
def check_2(p:float,dw:float)->bool:
    return p>0.3 and dw>0.4

def Env5_1_cal(p:float,dtempo:float,dw:float)->int:
    if(not check_1(p,dw)): return 0
    x_P_range = np.arange(0.1, 100, 0.01,np.float32)
    x_W_range = np.arange(0.4, 1, 0.01,np.float32)
    x_T_range = np.arange(0, 100, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P = ctrl.Antecedent(x_P_range, 'density')
    x_W = ctrl.Antecedent(x_W_range, 'wetdry')
    x_T = ctrl.Antecedent(x_T_range, 'tempo')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P["S"]=fuzz.trimf(x_P_range, [0.1, 0.1, 0.53])
    x_P["M"]=fuzz.trimf(x_P_range, [0.47 ,3.5, 5.3])
    x_P["L"]=fuzz.trapmf(x_P_range, [4.7 ,6, 100,100])
    x_W["M"]=fuzz.trimf(x_W_range, [0.4, 0.5, 0.65])
    x_W["H"]=fuzz.trimf(x_W_range, [0.55, 1, 1])
    x_T["S"]=fuzz.trimf(x_T_range, [0,0,12])
    x_T["L"]=fuzz.trimf(x_T_range, [8,15,100])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P["S"] & x_T["S"] & x_W["M"])),consequent=y_E["D"],label="1")
    rule2=ctrl.Rule(antecedent=((x_P["S"] & x_T["S"] & x_W["H"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_P["S"] & x_T["L"] & x_W["M"])),consequent=y_E["D"],label="3")
    rule4=ctrl.Rule(antecedent=((x_P["S"] & x_T["L"] & x_W["H"])),consequent=y_E["E"],label="4")
    rule5=ctrl.Rule(antecedent=((x_P["M"])),consequent=y_E["E"],label="5")
    rule6=ctrl.Rule(antecedent=((x_P["L"])),consequent=y_E["F"],label="6")
    rule=[rule1,rule2,rule3,rule4,rule5,rule6]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["density"]=p
    sim.input["wetdry"]=dw
    sim.input["tempo"]=dtempo
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def Env5_2_cal(p:float,dtempo:float,dw:float)->int:
    if(not check_2(p,dw)): return 0
    x_P_range = np.arange(0.1, 100, 0.01,np.float32)
    x_W_range = np.arange(0.4, 1, 0.01,np.float32)
    x_T_range = np.arange(0, 100, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P = ctrl.Antecedent(x_P_range, 'density')
    x_W = ctrl.Antecedent(x_W_range, 'wetdry')
    x_T = ctrl.Antecedent(x_T_range, 'tempo')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P["S"]=fuzz.trimf(x_P_range, [0.1, 0.1, 0.53])
    x_P["M"]=fuzz.trimf(x_P_range, [0.47 ,3.5, 5.3])
    x_P["L"]=fuzz.trapmf(x_P_range, [4.7 ,6, 100,100])
    x_W["M"]=fuzz.trimf(x_W_range, [0.4, 0.5, 0.65])
    x_W["H"]=fuzz.trimf(x_W_range, [0.55, 1, 1])
    x_T["M"]=fuzz.trimf(x_T_range, [0,0,12])
    x_T["H"]=fuzz.trimf(x_T_range, [8,15,100])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P["S"] & x_T["M"] & x_W["M"])),consequent=y_E["D"],label="1")
    rule2=ctrl.Rule(antecedent=((x_P["S"] & x_T["M"] & x_W["H"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_P["S"] & x_T["H"] & x_W["M"])),consequent=y_E["D"],label="3")
    rule4=ctrl.Rule(antecedent=((x_P["S"] & x_T["H"] & x_W["H"])),consequent=y_E["E"],label="4")
    rule5=ctrl.Rule(antecedent=((x_P["M"])),consequent=y_E["E"],label="5")
    rule6=ctrl.Rule(antecedent=((x_P["L"])),consequent=y_E["F"],label="6")
    rule=[rule1,rule2,rule3,rule4,rule5,rule6]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["density"]=p
    sim.input["wetdry"]=dw
    sim.input["tempo"]=dtempo
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def Env5_cal(type:float,p:float,dtempo:float,dw:float)->int:
    if(type=="Water"): return Env5_1_cal(p,dtempo,dw)
    elif(type=='Solid'): return Env5_2_cal(p,dtempo,dw)
    else: return 0