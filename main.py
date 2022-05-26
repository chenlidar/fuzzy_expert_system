from Env1_Normal import Env1_cal
from Env2_Freeze import Env2_cal
from Env3_Sea import Env3_cal
from Env4_Cl import Env4_cal
from Env5_Salt import Env5_cal

t="Water"
p=0.3
d=0.5
dw=11
y=Env5_cal(t,p,d,dw)
print(y)