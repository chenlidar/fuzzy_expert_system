%模糊控制器设计
env=newfis('env1_normal');

env=addvar(env,'input','W',[0,1]);                   
env=addvar(env,'input','H',[0,1]);
env=addvar(env,'output','Env',[1,3]);

env=addmf(env,'input',1,'NL','trimf',[0.00, 0.00, 0.35]); 
env=addmf(env,'input',1,'O','trimf',[0.35, 0.60, 0.90]); 
env=addmf(env,'input',1,'F','trimf',[0.85, 1.00, 1.00]); 

env=addmf(env,'input',2,'D','trimf', [0.00, 0.00, 0.25]); 
env=addmf(env,'input',2,'LD','trimf',[0.15, 0.30, 0.45]); 
env=addmf(env,'input',2,'LW','trimf',[0.35, 0.50, 0.65]); 
env=addmf(env,'input',2,'W','trimf', [0.55, 0.70, 0.85]); 
env=addmf(env,'input',2,'VW','trimf',[0.75, 1.00, 1.00]); 

env=addmf(env,'output',1,'A','trimf',[1, 1, 2]); 
env=addmf(env,'output',1,'B','trimf',[1, 2, 3]); 
env=addmf(env,'output',1,'C','trimf',[2, 3, 4]);

%规则库
rulelist=[1 1 1 1 1;
          1 2 2 1 1;
          1 3 2 1 1;
          1 4 1 1 1;
          1 5 1 1 1;
          2 1 1 1 1;
          2 2 3 1 1;
          2 3 3 1 1;
          2 4 3 1 1;
          2 5 1 1 1;
          3 1 1 1 1;
          3 2 1 1 1;
          3 3 1 1 1;
          3 4 1 1 1;
          3 5 1 1 1;];
           
env=addrule(env,rulelist);                %添加模糊规则函数
a1=setfis(env,'DefuzzMethod','centroid');                  %设置解模糊方法
writefis(a1,'env');                       %保存模糊系统
