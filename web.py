from flask import Flask,render_template,request
from sqlalchemy import true
from Env1_Normal import Env1_cal
from Env2_Freeze import Env2_cal
from Env3_Sea import Env3_cal
from Env4_Cl import Env4_cal
from Env5_Salt import Env5_cal
from Env6_Chemical import Env6_1_cal,Env6_2_cal,Env6_3_cal
from Env7_Abrasion import Env7_cal

app = Flask(__name__)
@app.route('/',methods=["get"])
def index():
    return render_template('try.html')

@app.route('/env_assess',methods=["get"])
def assess():
    return render_template('assess.html')
@app.route('/result',methods=["post"])
def result():
    ans=0
    env_focal=["无效结果","A 轻微","B 轻度","C 中度","D 严重","E 非常严重","F 极端严重"]
    data=request.form.to_dict()
    tocal=[0,0,0,0,0,0,0,0]
    res=[0,0,0,0,0,0,0,0]
    if 'env1' in data:
        tmp=Env1_cal(float(data['env1_W']),float(data['env1_T']))
        tocal[1]=1
        res[1]=tmp
        ans=max(ans,tmp)
        
    if 'env2' in data:
        tmp=Env2_cal(float(data['env2_W']),float(data['env2_T']),float(data['env2_DT']))
        tocal[2]=1
        res[2]=tmp
        ans=max(ans,tmp)
    if 'env3' in data:
        tmp=Env3_cal(float(data['env3_D']),float(data['env3_T']),float(data['env3_HL']),float(data['env3_LL']),float(data['env3_W']))
        tocal[3]=1
        res[3]=tmp
        ans=max(ans,tmp)
    if 'env4' in data and 'env4_1' in data:
        ty=''
        ss=''
        if data['env4_1']=='env4_s':
            ty='Solid'
            ss='env4_s_CL'
        else:
            ty='Water'
            ss='env4_w_CL'
        tmp=Env4_cal(ty,float(data[ss]))
        tocal[4]=1
        res[4]=tmp
        ans=max(ans,tmp)
    if 'env5' in data and 'env5_1' in data:
        ty=''
        env5_S=0.0
        env5_T=0.0
        env5_D=0.0
        if data['env5_1']=='env5_s':
            ty='Solid'
            env5_S=float(data['env5_s_S'])
            env5_T=float(data['env5_s_T'])
            env5_D=float(data['env5_s_D'])
        else:
            ty='Water'
            env5_S=float(data['env5_w_S'])
            env5_T=float(data['env5_w_T'])
            env5_D=float(data['env5_w_D'])
        tmp=Env5_cal(ty,env5_S,env5_T,env5_D)
        tocal[5]=1
        res[5]=tmp
        print(env_focal[tmp])
        ans=max(ans,tmp)
    if 'env6' in data and 'env6_1' in data:
        if data['env6_1']=='env6_w':
            tmp=Env6_1_cal(float(data['env6_w_S']),
                            float(data['env6_w_M']),
                            float(data['env6_w_PH']),
                            float(data['env6_w_C']),
                            float(data['env6_w_H']),
                            float(data['env6_w_D']))
        elif data['env6_1']=='env6_s':
            tmp=Env6_2_cal(float(data['env6_s_S']),
                            float(data['env6_s_H']),
                            float(data['env6_s_D']))
        elif data['env6_1']=='env6_a':
            tmp=Env6_3_cal(float(data['env6_a_PH']))
        tocal[6]=1
        res[6]=tmp
        ans=max(ans,tmp)
    if 'env7' in data:
        a=0
        if 'env7_I' in data: a=1
        tmp=Env7_cal(float(data['env7_W']),float(data['env7_S']),bool(a))
        tocal[7]=1
        res[7]=tmp
        ans=max(ans,tmp)
    print("综合作用："+str(env_focal[ans]))
    for i in range(1,8):
        if tocal[i]==1:
            res[i]=env_focal[res[i]]
    return render_template('result.html',ans=env_focal[ans],tocal=tocal,res=res)