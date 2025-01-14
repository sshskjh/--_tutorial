#보류
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats
import os
import sys
import pandas as pd
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "20201008 계측 Data")
save_path = os.path.dirname(__file__)
sys.path.append(data_path)
plt.rcParams["font.family"] = "Times New Roman"

data = pd.read_csv(data_path+"\\1Mohm4단자_10kOhm을ground멀리연결_vv.csv", skiprows=4, usecols=np.r_[0:2])
V_DUT = data.loc[:,'Channel 1 (V)'].to_list()
V_tot = data.loc[:,'Channel 2 (V)'].to_list()

# choose what to use as x and y
V_tot = np.array(list(V_tot))
V_DUT = np.array(list(V_DUT))
#x = I, y = V_RL'
y = V_DUT
x = (V_tot-V_DUT)/1e6

#cut Data for 1 period[:N] 
N = int(930.908 * 5)
start = 862+54
x = x[start:N+start]
y = y[start:N+start]

# 무엇을 x와 y의 값에 얼마를 곱할 것인지 선택하라.(ex choose mV in x axis --> x_mul = 1e3) 
# 그래프에서 단위를 표기하는 것에 주의하라.
x_mul = 1e6
y_mul = 1
x_rlim = max(x)
x_llim = min(x)

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print('y = (%f) + (%f) * x' % (intercept, slope))
print('r^2 = %f' % r_value**2)
print('R_DUT = ', slope)
x_reggression = np.linspace(x_llim, x_rlim, 10)
y_reggression = intercept + slope * x_reggression

#average the results
x_avg = []
y_avg = []
avg_N = 100
for i in range(len(x)//avg_N):
    x_a = 0
    y_a = 0
    for j in range(avg_N):
        x_a += x[i*avg_N+j]
        y_a += y[i*avg_N+j]
    x_avg.append(x_a/avg_N)
    y_avg.append(y_a/avg_N)
x = x_avg
y = y_avg

#resize for plotting
x = [x_mul*e for e in x]
y = [y_mul*e for e in y]
x_reggression = [x_mul*e for e in x_reggression]
y_reggression = [y_mul*e for e in y_reggression]

x_rlim = max(x)
x_llim = min(x)
y_ulim = max(y)
y_dlim = min(y)


plt.title('Correlation between $\mathrm{I_{DUT}}$ and $\mathrm{V_{{R\'}_L}}$')
plt.xlabel('$\mathrm{I_{DUT}}$[$\mathrm{\mu}A$]')
plt.ylabel('$\mathrm{V_{{R\'}_L}}$[V]')
plt.xlim(x_llim, x_rlim)
plt.ylim(y_dlim, y_ulim)
plt.plot(x_reggression, y_reggression, label='fitted', color = 'blue', linewidth = 2)
plt.plot(x, y, '.', label='experiment', markersize = 7, color = 'black')
plt.legend(loc=0)
#plt.show() 하면 pdf출력이 안됨. 왜그런지는 모르겠음
plt.savefig(os.path.join(save_path,'0_IV_curve_10kOhm_far_ground.pdf'))
plt.show()