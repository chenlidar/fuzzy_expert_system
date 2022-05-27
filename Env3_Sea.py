import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
    
def check(dis:float)->bool:
    return dis<=1.2
def Env3_cal(dis:float,tempo:float,highw:float,loww:float,pos:float)->int:
    if(not check(dis)): return 0
    a=loww-1
    b=highw-1
    c=highw+1.5
    x_T_range = np.arange(-60, 60, 0.01,np.float32)
    x_D_range = np.arange(0, 1.2, 0.001,np.float32)
    x_P_range = np.arange(-1000,1000,0.01,np.float32)
    y_E_range = np.arange(1, 6, 0.1,np.float32)
    # 定义模糊控制变量
    x_T = ctrl.Antecedent(x_T_range, 'tempo')
    x_D = ctrl.Antecedent(x_D_range, 'distance')
    x_P = ctrl.Antecedent(x_P_range, 'position')
    y_E = ctrl.Consequent(y_E_range, 'env')
    # 隶属度函数
    x_T["N"]=fuzz.trapmf(x_T_range, [-60,-60, 10, 22])
    x_T["H"]=fuzz.trapmf(x_T_range, [18 ,25, 60, 60])
    x_D["S"]=fuzz.trimf(x_D_range, [0.28, 1.2, 1.2])
    x_D["M"]=fuzz.trimf(x_D_range, [0.08, 0.20, 0.32])
    x_D["L"]=fuzz.trimf(x_D_range, [0, 0, 0.12])
    x_P["U"]=fuzz.trapmf(x_P_range, [-1000 ,-1000, a-1, a+0.3])
    x_P["S"]=fuzz.trimf(x_P_range, [a-0.3 ,(a+b)/2.0, b+0.3])
    x_P["T"]=fuzz.trimf(x_P_range, [b-0.3 ,(b+c)/2.0, c+0.3])
    x_P["A"]=fuzz.trapmf(x_P_range, [c-0.3 ,c+1, 1000,1000])
    y_E["C"] =fuzz.trimf(y_E_range, [2, 3, 4])
    y_E["D"] =fuzz.trimf(y_E_range, [3, 4, 5])
    y_E["E"] =fuzz.trimf(y_E_range, [4, 5, 6])
    y_E["F"] =fuzz.trimf(y_E_range, [5, 6, 6])
    y_E.defuzzify_method="centroid"
    # 规则
    rule1=ctrl.Rule(antecedent=((x_P["U"])),consequent=y_E["C"],label="1")
    rule2=ctrl.Rule(antecedent=(((x_P["S"] | x_P["T"]) & x_T["N"])),consequent=y_E["E"],label="2")
    rule3=ctrl.Rule(antecedent=(((x_P["S"] | x_P["T"]) & x_T["H"])),consequent=y_E["F"],label="3")
    rule4=ctrl.Rule(antecedent=((x_P["A"] & x_D["S"])),consequent=y_E["C"],label="4")
    rule5=ctrl.Rule(antecedent=((x_P["A"] & x_D["M"])),consequent=y_E["D"],label="5")
    rule6=ctrl.Rule(antecedent=((x_P["A"] & x_D["L"])),consequent=y_E["E"],label="6")
    rule=[rule1,rule2,rule3,rule4,rule5,rule6]
    # 系统和运行环境初始化
    system = ctrl.ControlSystem(rule)
    sim = ctrl.ControlSystemSimulation(system)
    # 计算
    sim.input["distance"]=dis
    sim.input["tempo"]=tempo
    sim.input["position"]=pos
    sim.compute()
    env=sim.output["env"]
    return round(env)