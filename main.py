from Env1_Normal import Env1_cal
from Env2_Freeze import Env2_cal
from Env3_Sea import Env3_cal
from Env4_Cl import Env4_cal
from Env5_Salt import Env5_cal
from Env6_Chemical import Env6_1_cal,Env6_2_cal,Env6_3_cal
from Env7_Abrasion import Env7_cal


def Env_cal():
    arr=input("""选择要评估混凝土工程所在环境：
(1)一般环境
(2)冻融环境
(3)近海或海洋氯化物环境
(4)除冰盐等其他氯化物环境
(5)盐结晶环境
(6)化学腐蚀环境
(7)磨蚀环境
""")
    env=[int(n) for n in arr.split()]
    tocal=[0,0,0,0,0,0,0,0]
    for an in env:
        if 1 <= an <= 7:
            tocal[an]=1
    ans=0
    env_focal=["无效结果","A 轻微","B 轻度","C 中度","D 严重","E 非常严重","F 极端严重"]
    if(tocal[1]):
        print("(1)一般环境")
        tmp=Env1_cal(float(input("与水接触程度(0-1):")),float(input("年平均相对湿度(0-1):")))
        print(env_focal[tmp])
        ans=max(ans,tmp)
        
    if(tocal[2]):
        print("(2)冻融环境")
        tmp=Env2_cal(float(input("混凝土相对饱水度(0-1):")),float(input("最冷月平均气温(摄氏度):")),float(input("平均日温差(摄氏度):")))
        print(env_focal[tmp])
        ans=max(ans,tmp)
    if(tocal[3]):
        print("(3)近海或海洋氯化物环境")
        tmp=Env3_cal(float(input("海岸线距离(km):")),float(input("年平均温度(摄氏度):")),float(input("高水位(m):")),float(input("低水位(m):")),float(input("水位位置(m):")))
        print(env_focal[tmp])
        ans=max(ans,tmp)
    if(tocal[4]):
        print("(4)除冰盐等其他氯化物环境")
        tmp=Env4_cal(input("土体/水体(Solid/Water):"),float(input("氯离子浓度(g/kg,g/L):")))
        print(env_focal[tmp])
        ans=max(ans,tmp)
    if(tocal[5]):
        print("(5)盐结晶环境")
        tmp=Env5_cal(input("土体/水体(Solid/Water):"),float(input("硫酸根离子浓度(g/kg,g/L):")),float(input("平均日温差(摄氏度):")),float(input("干湿交替程度(0-1):")))
        print(env_focal[tmp])
        ans=max(ans,tmp)
    if(tocal[6]):
        print("(6)化学腐蚀环境")
        type=input("土体/水体/大气(Solid/Water/Air):")
        if type=="Water":
            tmp=Env6_1_cal(float(input("硫酸根离子浓度(g/L):")),
                                      float(input("镁离子浓度(g/L):")),
                                      float(input("pH值:")),
                                      float(input("CO2浓度(g/l):")),
                                      float(input("海拔(km):")),
                                      float(input("干燥度系数:")))
        elif type=="Solid":
            tmp=Env6_2_cal(float(input("硫酸根离子浓度(g/kg):")),
                                      float(input("海拔(km):")),
                                      float(input("干燥度系数:")))
        elif type=="Air":
            tmp=Env6_3_cal(float(input("pH值:")))
        print(env_focal[tmp])
        ans=max(ans,tmp)
    if(tocal[7]):
        print("(7)磨蚀环境")
        tmp=Env7_cal(float(input("风力等级:")),float(input("汛期含沙量(1000kg/m3):")),bool("是否有流冰(0/1):"))
        print(env_focal[tmp])
        ans=max(ans,tmp)
    print("综合作用："+str(env_focal[ans]))
    
if __name__ == '__main__':
    Env_cal()