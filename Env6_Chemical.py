import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def check_1(ps:float)->bool:
    return ps>0.2
def check_2(ps:float)->bool:
    return ps>0.3

def Env6_1_cal(ps:float,pm:float,ph:float,pc:float,h:float,d:float)->int:
    pass
    
def Env6_2_cal(ps:float,h:float,d:float)->int:
    if(not check_2(ps)): return 0
    x_P_1_range = np.arange(0, 30, 0.01,np.float32)
    x_P_2_range = np.arange(0, 7.5, 0.01,np.float32)
    x_H_range = np.arange(-10, 10, 0.01,np.float32)
    x_D_range = np.arange(0, 10, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P_1 = ctrl.Antecedent(x_P_1_range, 'pSO4_1')
    x_P_2 = ctrl.Antecedent(x_P_2_range, 'pSO4_2')
    x_H = ctrl.Antecedent(x_H_range, 'height')
    x_D = ctrl.Antecedent(x_D_range, 'dry')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P_1["S"]=fuzz.trimf(x_P_1_range, [0.3, 0.3, 1.7])
    x_P_1["M"]=fuzz.trimf(x_P_1_range, [1.3 ,5, 6.3])
    x_P_1["L"]=fuzz.trimf(x_P_1_range, [5.7 ,10,15.3])
    x_P_1["VL"]=fuzz.trimf(x_P_1_range, [14.7 ,30,30])
    x_P_2["S"]=fuzz.trimf(x_P_2_range, [0.3, 0.3, 0.8])
    x_P_2["M"]=fuzz.trimf(x_P_2_range, [0.7 ,2.5, 3.2])
    x_P_2["L"]=fuzz.trimf(x_P_2_range, [2.8 ,6,7.5])
    x_H["Y"]=fuzz.trapmf(x_H_range,[2.8,3.2,10,10])
    x_H["N"]=fuzz.trapmf(x_H_range,[-10,-10,2.5,3.2])
    x_D["Y"]=fuzz.trapmf(x_D_range,[1.8,2.2,10,10])
    x_D["N"]=fuzz.trimf(x_D_range,[0,0,2.2])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P_1["S"] & x_D['N'] & x_H['N'])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=((x_P_1["M"] & x_D['N'] & x_H['N'])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_P_1["L"] & x_D['N'] & x_H['N'])),consequent=y_E["E"],label="3")
    rule4=ctrl.Rule(antecedent=((x_P_1["VL"] & x_D['N'] & x_H['N'])),consequent=y_E["F"],label="4")
    rule6=ctrl.Rule(antecedent=((x_P_2["S"] & (x_D['Y'] | x_H['Y']))),consequent=y_E["F"],label="5")
    rule5=ctrl.Rule(antecedent=((x_P_2["M"] & (x_D['Y'] | x_H['Y']))),consequent=y_E["F"],label="6")
    rule7=ctrl.Rule(antecedent=((x_P_2["L"] & (x_D['Y'] | x_H['Y']))),consequent=y_E["F"],label="7")
    
    rule=[rule1,rule2,rule3,rule4,rule5,rule6,rule7]    
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["pSO4_1"]=ps
    sim.input["pSO4_2"]=ps
    sim.input["height"]=h
    sim.input["dry"]=d
    sim.compute()
    env=sim.output["env"]
    return round(env)
  
def Env6_3_cal(ph:float)->int:
    x_P_range = np.arange(0, 14, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P = ctrl.Antecedent(x_P_range, 'pH')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P["S"]=fuzz.trimf(x_P_range, [5.4, 7, 14])
    x_P["M"]=fuzz.trimf(x_P_range, [4.3 ,5, 5.8])
    x_P["L"]=fuzz.trimf(x_P_range, [0 ,0,4.7])
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
    sim.input["pH"]=ph
    sim.compute()
    env=sim.output["env"]
    return round(env)

def Env6_cal(type:float,ps:float,pm:float,ph:float,pc:float,h:float,d:float)->int:
    if(type=="Water"): return Env6_1_cal(ps,pm,ph,pc,h,d)
    elif(type=='Solid'): return Env6_2_cal(ps,h,d)
    elif(type=="Air"): return Env6_3_cal(ph)
    else: return 0