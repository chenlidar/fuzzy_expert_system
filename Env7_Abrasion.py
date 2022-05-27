import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

def check_wind(wind:float):
    return wind>=7
def check_sand(sand:float):
    return sand>0.2
def wind_cal(wind:float):
    if(not check_wind(wind)):return 0
    x_W_range = np.arange(6.5, 17, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_W = ctrl.Antecedent(x_W_range, 'wind')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_W["S"]=fuzz.trimf(x_W_range, [6.5, 7.5, 9.5])
    x_W["M"]=fuzz.trimf(x_W_range, [9.5 ,10.5, 11.5])
    x_W["L"]=fuzz.trapmf(x_W_range, [10.5 ,12.5, 17,17])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_W["S"])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=((x_W["M"])),consequent=y_E["D"],label="2")
    rule3=ctrl.Rule(antecedent=((x_W["L"])),consequent=y_E["F"],label="3")
    rule=[rule1,rule2,rule3]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["wind"]=wind
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def sand_cal(sand:float):
    if(not check_sand(sand)):return 0
    x_P_range = np.arange(0.17, 10, 0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    x_P = ctrl.Antecedent(x_P_range, 'sand')
    y_E = ctrl.Consequent(y_E_range, 'env')
    x_P["S"]=fuzz.trimf(x_P_range, [0.17, 0.17, 0.63])
    x_P["M"]=fuzz.trimf(x_P_range, [0.57 ,0.8, 1.03])
    x_P["L"]=fuzz.trapmf(x_P_range, [0.97 ,1.03, 10,10])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P["S"])),consequent=y_E["D"],label="1")
    rule2=ctrl.Rule(antecedent=((x_P["M"])),consequent=y_E["E"],label="2")
    rule3=ctrl.Rule(antecedent=((x_P["L"])),consequent=y_E["F"],label="3")
    rule=[rule1,rule2,rule3]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["sand"]=sand
    sim.compute()
    env=sim.output["env"]
    return round(env)
    
def Env7_cal(wind:float,sand:float,ice:bool)->int:
    a=wind_cal(wind)
    b=sand_cal(sand)
    if(ice):c=5
    else: c=0
    return max(a,b,c)