# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 00:13:08 2022

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt

def computeDamage(stats, dmgType):
    
    if dmgType == 'atk':
        damage = ((stats["atkBase"] * (1 + stats["atkPercent"])) + stats["atkFlat"]) * (1 + stats["critRate"]*stats["critDamage"]) * (1 + stats["dmgPercent"])
    elif dmgType == 'hp':
        damage = ((stats["hpBase"] * (1 + stats["hpPercent"])) + stats["hpFlat"]) * (1 + stats["critRate"]*stats["critDamage"]) * (1 + stats["dmgPercent"])
        
    return damage
    

def computeSubstatGains(stats, dmgType):
    
    roll_atkPercent = 4.96/100
    roll_critRate = 3.31/100
    roll_critDamage = 6.62/100
    roll_em = 19.82
    roll_hpPercent = 4.96/100
    
    damage_initial = computeDamage(stats, dmgType)
    
    stats_atkPercent = stats.copy()
    stats_atkPercent["atkPercent"] = stats_atkPercent["atkPercent"] + roll_atkPercent
    gain_atkPercent = computeDamage(stats_atkPercent, dmgType)/damage_initial

    stats_critDamage = stats.copy()
    stats_critDamage["critDamage"] = stats_critDamage["critDamage"] + roll_critDamage
    gain_critDamage = computeDamage(stats_critDamage, dmgType)/damage_initial
    
    stats_critRate = stats.copy()
    stats_critRate["critRate"] = stats_critRate["critRate"] + roll_critRate
    gain_critRate = computeDamage(stats_critRate, dmgType)/damage_initial

    stats_em = stats.copy()
    # stats_em["dmgPercent"] = stats_em["dmgPercent"] + roll_em*0.15/100 # Yae Miko only
    gain_em = computeDamage(stats_em, dmgType)/damage_initial
    
    stats_hpPercent = stats.copy()
    stats_hpPercent["hpPercent"] = stats_hpPercent["hpPercent"] + roll_hpPercent
    gain_hpPercent = computeDamage(stats_hpPercent, dmgType)/damage_initial
    
    return [gain_atkPercent, gain_critRate, gain_critDamage, gain_em, gain_hpPercent]
   
def simulateSubStatGain(stats, num_subs, dmgType):
    
    damage_initial = computeDamage(stats, dmgType)
    
    gains = []
    
    for x in range(0,num_subs):
        
        gain = computeSubstatGains(stats, dmgType)
        gains.append(gain)
        gain_maxIdx = gain.index(max(gain))
        
        if gain_maxIdx == 0:
            stats["atkPercent"] = stats["atkPercent"] + 4.96/100
        elif gain_maxIdx == 1: 
            stats["critRate"] = stats["critRate"] + 3.31/100
        elif gain_maxIdx == 2:
            stats["critDamage"] = stats["critDamage"] + 6.62/100
        elif gain_maxIdx == 3:
            stats["dmgPercent"] = stats["dmgPercent"] + 19.82*0.15/100
        elif gain_maxIdx == 4:
            stats["hpPercent"] = stats["hpPercent"] + 4.96/100 

    selected_stat_idx = np.argmax(gains, axis=1)
    gains = np.asarray(gains)
    selected_stat_gain = gains[np.arange(len(gains)), selected_stat_idx]
    gain_cumulative = np.cumprod(selected_stat_gain)
    damage_cumulative = damage_initial*gain_cumulative
        
    return gains, damage_cumulative
    
#%% 

num_subs = 50

# Yae Miko
stats_SA = {"atkBase": 340+674, "atkPercent": 0.466+0.331, "atkFlat": 311, "critRate": 0.05+0.192+0.311, "critDamage": 0.5, "dmgPercent": 0.466+0.12} # Skyward Atlas
stats_KV_E = {"atkBase": 340+608, "atkPercent": 0.466, "atkFlat": 311, "critRate": 0.05+0.192+0.311, "critDamage": 0.5+0.662, "dmgPercent": 0.466+0.48} # Kagura's Verity
stats_KV_Q = {"atkBase": 340+608, "atkPercent": 0.466, "atkFlat": 311, "critRate": 0.05+0.192+0.311, "critDamage": 0.5+0.662, "dmgPercent": 0.466+0.12} # Kagura's Verity

SA_gains, SA_damage_cumulative = simulateSubStatGain(stats_SA, num_subs, 'atk')
KV_E_gains, KV_E_damage_cumulative = simulateSubStatGain(stats_KV_E, num_subs, 'atk')
KV_Q_gains, KV_Q_damage_cumulative = simulateSubStatGain(stats_KV_Q, num_subs, 'atk')

# Plot total damage comparison
# Plot all 
fig = plt.figure
plt.plot(range(1,num_subs+1),SA_damage_cumulative, label='Skyward Atlas')
plt.plot(range(1,num_subs+1),KV_E_damage_cumulative, label='Kagura\'s Verity E')
plt.plot(range(1,num_subs+1),KV_Q_damage_cumulative, label='Kagura\'s Verity Q')
plt.title('Optimally distributed substats')
plt.xlabel('Substat Number')
plt.ylabel('Damage before talent multipliers')
plt.grid()
plt.legend()


# Plot individual gains
gains = SA_gains
fig = plt.figure()
plt.plot(range(1,num_subs+1),(gains[:,0]-1)*100, label='ATK%')
plt.plot(range(1,num_subs+1),(gains[:,1]-1)*100, label='CR')
plt.plot(range(1,num_subs+1),(gains[:,2]-1)*100, label='CD')
plt.plot(range(1,num_subs+1),(gains[:,3]-1)*100, label='EM')
plt.title('Substat Weights - Yae Miko, Skyward Atlas, ATK/ELE/CR')   
# plt.title('Substat Weights - Yae Miko, Kagura\'s Verity, ATK/ELE/CR')   
plt.xlabel('Substat Number')
plt.ylabel('Relative Damage Gain (%)')
plt.grid()
plt.legend()

#%% Yelan

num_subs = 50

stats_HP_HY_CR = {"atkBase": 0, "atkPercent": 0, "atkFlat": 0, "hpBase": 14450, "hpPercent": 0.466, "hpFlat": 4780, "critRate": 0.05+0.192+0.311, "critDamage": 0.5, "dmgPercent": 0.466} 

yelan_gains, yelan_damage_cumulative = simulateSubStatGain(stats_HP_HY_CR, num_subs, 'hp')

# Plot all 
fig = plt.figure
plt.plot(range(1,num_subs+1),yelan_damage_cumulative, label='HP/HYDRO/CRIT')
plt.title('Optimally distributed substats')
plt.xlabel('Substat Number')
plt.ylabel('Damage before talent multipliers')
plt.grid()
plt.legend()

# Plot individual gains
gains = yelan_gains
fig = plt.figure()
plt.plot(range(1,num_subs+1),(gains[:,0]-1)*100, label='ATK%')
plt.plot(range(1,num_subs+1),(gains[:,1]-1)*100, label='CR')
plt.plot(range(1,num_subs+1),(gains[:,2]-1)*100, label='CD')
plt.plot(range(1,num_subs+1),(gains[:,3]-1)*100, label='EM')
plt.plot(range(1,num_subs+1),(gains[:,4]-1)*100, label='HP%')
plt.title('Substat Weights - Yelan, Favonius Warbow, HP/HYDRO/CR')   
# plt.title('Substat Weights - Yae Miko, Kagura\'s Verity, ATK/ELE/CR')   
plt.xlabel('Substat Number')
plt.ylabel('Relative Damage Gain (%)')
plt.grid()
plt.legend()

## Which substats
best_subs = np.argmax(gains,1)
best_subs = best_subs[:20-6+6] # Filter to more reasonable number of substats, +6 = KQM fixed rolls, -6 = ER rolls required on distributed subs
subs_CD = sum(best_subs == 2)
subs_CR = sum(best_subs == 1)
subs_HP = sum(best_subs == 4)





