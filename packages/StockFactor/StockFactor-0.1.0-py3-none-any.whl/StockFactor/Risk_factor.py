import pandas as pd
import numpy as np

def weighted_average(dataframe, value, weight):
    val = dataframe[value]
    wt = dataframe[weight]
    return (val * wt).sum() / wt.sum()

def calculate_risk_factors(risk_port, rf):
    risk_port['HmL1'] = risk_port['lag_BM_TEJy']
    risk_port['HmL2'] = risk_port['lag_BM-TEJ-y']
    risk_port['HmL3'] = risk_port['lag_BM-TSE-y']
    risk_port['SmB1'] = risk_port['lag_MEy']
    risk_port['SmB2'] = risk_port['lag_MV-y']
    risk_port['Inv'] = risk_port['AGy']

    name_temp1 = ['HmL1', 'HmL2', 'Inv', 'OPy']
    name_temp2 = ['SmB1', 'SmB2']

    for i in name_temp1:
        risk_port[i + '_rank'] = risk_port.groupby(['Year', 'Month'])[i].transform(lambda x: pd.qcut(x, 10, labels=list(range(1, 11))))

    for i in name_temp2:
        risk_port[i + '_rank'] = risk_port.groupby(['Year', 'Month'])[i].transform(lambda x: pd.qcut(x, 2, labels=list(range(1, 3))))

    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['HmL1_rank'] <= 3)
    risk_port.loc[mask, 'Port_SBM'] = 'SL'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['HmL1_rank'] > 3) & (risk_port['HmL1_rank'] <= 7)
    risk_port.loc[mask, 'Port_SBM'] = 'SbmN'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['HmL1_rank'] > 7)
    risk_port.loc[mask, 'Port_SBM'] = 'SH'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['HmL1_rank'] <= 3)
    risk_port.loc[mask, 'Port_SBM'] = 'BL'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['HmL1_rank'] > 3) & (risk_port['HmL1_rank'] <= 7)
    risk_port.loc[mask, 'Port_SBM'] = 'BbmN'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['HmL1_rank'] > 7)
    risk_port.loc[mask, 'Port_SBM'] = 'BH'

    risk_port_monthly = pd.DataFrame()
    risk_port = risk_port.sort_values(['Year', 'Month', 'Port_SBM'])

    name_temp = ['SL', 'SbmN', 'SH', 'BL', 'BbmN', 'BH']
    for i in name_temp:
        risk_port_monthly[i] = risk_port.loc[risk_port['Port_SBM'] == i, :].groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')

    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['OPy_rank'] <= 3)
    risk_port.loc[mask, 'Port_SOP'] = 'SW'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['OPy_rank'] > 3) & (risk_port['OPy_rank'] <= 7)
    risk_port.loc[mask, 'Port_SOP'] = 'SopN'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['OPy_rank'] > 7)
    risk_port.loc[mask, 'Port_SOP'] = 'SR'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['OPy_rank'] <= 3)
    risk_port.loc[mask, 'Port_SOP'] = 'BW'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['OPy_rank'] > 3) & (risk_port['OPy_rank'] <= 7)
    risk_port.loc[mask, 'Port_SOP'] = 'BopN'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['OPy_rank'] > 7)
    risk_port.loc[mask, 'Port_SOP'] = 'BR'

    risk_port = risk_port.sort_values(['Year', 'Month', 'Port_SOP'])

    name_temp = ['SW', 'SopN', 'SR', 'BW', 'BopN', 'BR']
    for i in name_temp:
        risk_port_monthly[i] = risk_port.loc[risk_port['Port_SOP'] == i, :].groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')

    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['Inv_rank'] <= 3)
    risk_port.loc[mask, 'Port_SInv'] = 'SC'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['Inv_rank'] > 3) & (risk_port['Inv_rank'] <= 7)
    risk_port.loc[mask, 'Port_SInv'] = 'SinvN'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['Inv_rank'] > 7)
    risk_port.loc[mask, 'Port_SInv'] = 'SA'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['Inv_rank'] <= 3)
    risk_port.loc[mask, 'Port_SInv'] = 'BC'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['Inv_rank'] > 3) & (risk_port['Inv_rank'] <= 7)
    risk_port.loc[mask, 'Port_SInv'] = 'BinvN'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['Inv_rank'] > 7)
    risk_port.loc[mask, 'Port_SInv'] = 'BA'

    risk_port = risk_port.sort_values(['Year', 'Month', 'Port_SInv'])

    name_temp = ['SC', 'SinvN', 'SA', 'BC', 'BinvN', 'BA']
    for i in name_temp:
        risk_port_monthly[i] = risk_port.loc[risk_port['Port_SInv'] == i, :].groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')

    risk_port_monthly['SmBbm'] = (1 / 3) * (risk_port_monthly['SH'] + risk_port_monthly['SbmN'] + risk_port_monthly['SL']) - \
                                 (1 / 3) * (risk_port_monthly['BH'] + risk_port_monthly['BbmN'] + risk_port_monthly['BL'])
    risk_port_monthly['SmBop'] = (1 / 3) * (risk_port_monthly['SR'] + risk_port_monthly['SopN'] + risk_port_monthly['SW']) - \
                                 (1 / 3) * (risk_port_monthly['BR'] + risk_port_monthly['BopN'] + risk_port_monthly['BW'])
    risk_port_monthly['SmBinv'] = (1 / 3) * (risk_port_monthly['SC'] + risk_port_monthly['SinvN'] + risk_port_monthly['SA']) - \
                                  (1 / 3) * (risk_port_monthly['BC'] + risk_port_monthly['BinvN'] + risk_port_monthly['BA'])
    risk_port_monthly['SmB'] = (1 / 3) * (risk_port_monthly['SmBbm'] + risk_port_monthly['SmBop'] + risk_port_monthly['SmBinv'])

    risk_port_monthly['Small'] = risk_port.loc[risk_port['SmB1_rank'] == 1, :].groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')
    risk_port_monthly['Big'] = risk_port.loc[risk_port['SmB1_rank'] == 2, :].groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')

    risk_port_monthly['HmLS'] = risk_port_monthly['SH'] - risk_port_monthly['SL']
    risk_port_monthly['HmLB'] = risk_port_monthly['BH'] - risk_port_monthly['BL']
    risk_port_monthly['HmL'] = (1 / 2) * (risk_port_monthly['HmLS'] + risk_port_monthly['HmLB'])

    risk_port_monthly['RmWS'] = risk_port_monthly['SR'] - risk_port_monthly['SW']
    risk_port_monthly['RmWB'] = risk_port_monthly['BR'] - risk_port_monthly['BW']
    risk_port_monthly['RmW'] = (1 / 2) * (risk_port_monthly['RmWS'] + risk_port_monthly['RmWB'])

    risk_port_monthly['CmAS'] = risk_port_monthly['SC'] - risk_port_monthly['SA']
    risk_port_monthly['CmAB'] = risk_port_monthly['BC'] - risk_port_monthly['BA']
    risk_port_monthly['CmA'] = (1 / 2) * (risk_port_monthly['CmAS'] + risk_port_monthly['CmAB'])

    risk_port_monthly['RM'] = risk_port.groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')

    risk_port['IA'] = risk_port['lag_AGy']
    risk_port['EwdIA'] = risk_port['lag_EwdIAy']

    risk_port['IA' + '_rank'] = risk_port.groupby(['Year', 'Month'])['IA'].transform(lambda x: pd.qcut(x, 10, labels=list(range(1, 11))))
    risk_port['ROEy' + '_rank'] = risk_port.groupby(['Year', 'Month'])['lag_ROEy'].transform(lambda x: pd.qcut(x, 10, labels=list(range(1, 11))))

    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] <= 3) & (risk_port['ROEy_rank'] <= 3)
    risk_port.loc[mask, 'Port_HXZ'] = 'SLIALROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] > 3) & (risk_port['IA_rank'] <= 7) & (risk_port['ROEy_rank'] <= 3)
    risk_port.loc[mask, 'Port_HXZ'] = 'SNIALROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] > 7) & (risk_port['ROEy_rank'] <= 3)
    risk_port.loc[mask, 'Port_HXZ'] = 'SHIALROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] <= 3) & (risk_port['ROEy_rank'] > 3) & (risk_port['ROEy_rank'] <= 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'SLIANROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] > 3) & (risk_port['IA_rank'] <= 7) & (risk_port['ROEy_rank'] > 3) & (risk_port['ROEy_rank'] <= 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'SNIANROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] > 7) & (risk_port['ROEy_rank'] > 3) & (risk_port['ROEy_rank'] <= 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'SHIANROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] <= 3) & (risk_port['ROEy_rank'] > 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'SLIAHROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] > 3) & (risk_port['IA_rank'] <= 7) & (risk_port['ROEy_rank'] > 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'SNIAHROE'
    mask = (risk_port['SmB1_rank'] == 1) & (risk_port['IA_rank'] > 7) & (risk_port['ROEy_rank'] > 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'SHIAHROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] <= 3) & (risk_port['ROEy_rank'] <= 3)
    risk_port.loc[mask, 'Port_HXZ'] = 'BLIALROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] > 3) & (risk_port['IA_rank'] <= 7) & (risk_port['ROEy_rank'] <= 3)
    risk_port.loc[mask, 'Port_HXZ'] = 'BNIALROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] > 7) & (risk_port['ROEy_rank'] <= 3)
    risk_port.loc[mask, 'Port_HXZ'] = 'BHIALROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] <= 3) & (risk_port['ROEy_rank'] > 3) & (risk_port['ROEy_rank'] <= 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'BLIANROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] > 3) & (risk_port['IA_rank'] <= 7) & (risk_port['ROEy_rank'] > 3) & (risk_port['ROEy_rank'] <= 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'BNIANROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] > 7) & (risk_port['ROEy_rank'] > 3) & (risk_port['ROEy_rank'] <= 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'BHIANROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] <= 3) & (risk_port['ROEy_rank'] > 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'BLIAHROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] > 3) & (risk_port['IA_rank'] <= 7) & (risk_port['ROEy_rank'] > 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'BNIAHROE'
    mask = (risk_port['SmB1_rank'] == 2) & (risk_port['IA_rank'] > 7) & (risk_port['ROEy_rank'] > 7)
    risk_port.loc[mask, 'Port_HXZ'] = 'BHIAHROE'

    name_temp = ['SLIALROE', 'SNIALROE', 'SHIALROE', 'SLIANROE', 'SNIANROE', 'SHIANROE', 'SLIAHROE', 'SNIAHROE', 'SHIAHROE',
                 'BLIALROE', 'BNIALROE', 'BHIALROE', 'BLIANROE', 'BNIANROE', 'BHIANROE', 'BLIAHROE', 'BNIAHROE', 'BHIAHROE']
    for i in name_temp:
        risk_port_monthly[i] = risk_port.loc[risk_port['Port_HXZ'] == i, :].groupby(['Year', 'Month']).apply(weighted_average, 'return', 'lag_MV')

    risk_port_monthly['qSmB'] = (1 / 9) * (risk_port_monthly['SLIALROE'] + risk_port_monthly['SNIALROE'] + risk_port_monthly['SHIALROE'] + risk_port_monthly['SLIANROE'] +
                                           risk_port_monthly['SNIANROE'] + risk_port_monthly['SHIANROE'] + risk_port_monthly['SLIAHROE'] + risk_port_monthly['SNIAHROE'] +
                                           risk_port_monthly['SHIAHROE']) - \
                                (1 / 9) * (risk_port_monthly['BLIALROE'] + risk_port_monthly['BNIALROE'] + risk_port_monthly['BHIALROE'] + risk_port_monthly['BLIANROE'] +
                                           risk_port_monthly['BNIANROE'] + risk_port_monthly['SHIANROE'] + risk_port_monthly['BLIAHROE'] + risk_port_monthly['BNIAHROE'] +
                                           risk_port_monthly['BHIAHROE'])
    risk_port_monthly['RIA']=(1/6)*(risk_port_monthly['SLIALROE']+risk_port_monthly['SLIANROE']+risk_port_monthly['SLIAHROE']+\
                               risk_port_monthly['BLIALROE']+risk_port_monthly['BLIANROE']+risk_port_monthly['BLIAHROE'])-\
    (1/6)*(risk_port_monthly['SHIALROE']+risk_port_monthly['SHIANROE']+risk_port_monthly['SHIAHROE']+\
                                   risk_port_monthly['BHIALROE']+risk_port_monthly['BHIANROE']+risk_port_monthly['BHIAHROE'])
    
    risk_port_monthly['RROE']=(1/6)*(risk_port_monthly['SLIAHROE']+risk_port_monthly['SNIAHROE']+risk_port_monthly['SHIAHROE']+\
                                   risk_port_monthly['BLIAHROE']+risk_port_monthly['BNIAHROE']+risk_port_monthly['BHIAHROE'])-\
        (1/6)*(risk_port_monthly['SLIALROE']+risk_port_monthly['SNIALROE']+risk_port_monthly['SHIALROE']+\
                                       risk_port_monthly['BLIALROE']+risk_port_monthly['BNIALROE']+risk_port_monthly['BHIALROE'])


    risk_port['MGMTy'+'_rank']=risk_port.groupby(['Year','Month'])['lag_MGMTy'].transform(lambda x: pd.qcut(x,10,labels=list(range(1,11))))
    risk_port['PERFy'+'_rank']=risk_port.groupby(['Year','Month'])['lag_PERFy'].transform(lambda x: pd.qcut(x,10,labels=list(range(1,11))))
    mask=(risk_port['SmB1_rank']==1) & (risk_port['MGMTy_rank']<=2)
    risk_port.loc[mask,'Port_MGMT']='SLMGMT'
    mask=(risk_port['SmB1_rank']==1) & (risk_port['MGMTy_rank']>2) & (risk_port['MGMTy_rank']<=8)
    risk_port.loc[mask,'Port_MGMT']='SNMGMT'
    mask=(risk_port['SmB1_rank']==1) & (risk_port['MGMTy_rank']>8)
    risk_port.loc[mask,'Port_MGMT']='SHMGMT'
    mask=(risk_port['SmB1_rank']==2) & (risk_port['MGMTy_rank']<=2)
    risk_port.loc[mask,'Port_MGMT']='BLMGMT'
    mask=(risk_port['SmB1_rank']==2) & (risk_port['MGMTy_rank']>2) & (risk_port['MGMTy_rank']<=8)
    risk_port.loc[mask,'Port_MGMT']='BNMGMT'
    mask=(risk_port['SmB1_rank']==2) & (risk_port['MGMTy_rank']>8)
    risk_port.loc[mask,'Port_MGMT']='BHMGMT'

    mask=(risk_port['SmB1_rank']==1) & (risk_port['PERFy_rank']<=2)
    risk_port.loc[mask,'Port_PERF']='SLPERF'
    mask=(risk_port['SmB1_rank']==1) & (risk_port['PERFy_rank']>2) & (risk_port['PERFy_rank']<=8)
    risk_port.loc[mask,'Port_PERF']='SNPERF'
    mask=(risk_port['SmB1_rank']==1) & (risk_port['PERFy_rank']>8)
    risk_port.loc[mask,'Port_PERF']='SHPERF'
    mask=(risk_port['SmB1_rank']==2) & (risk_port['PERFy_rank']<=2)
    risk_port.loc[mask,'Port_PERF']='BLPERF'
    mask=(risk_port['SmB1_rank']==2) & (risk_port['PERFy_rank']>2) & (risk_port['PERFy_rank']<=8)
    risk_port.loc[mask,'Port_PERF']='BNPERF'
    mask=(risk_port['SmB1_rank']==2) & (risk_port['PERFy_rank']>8)
    risk_port.loc[mask,'Port_PERF']='BHPERF'

    name_temp=['SLMGMT','SNMGMT','SHMGMT','BLMGMT','BNMGMT','BHMGMT']
    for i in name_temp:
        risk_port_monthly[i]=risk_port.loc[risk_port['Port_MGMT']==i,:].groupby(['Year','Month']).apply(weighted_average,'return', 'lag_MV')
    name_temp=['SLPERF','SNPERF','SHPERF','BLPERF','BNPERF','BHPERF']
    for i in name_temp:
        risk_port_monthly[i]=risk_port.loc[risk_port['Port_PERF']==i,:].groupby(['Year','Month']).apply(weighted_average,'return', 'lag_MV')

    risk_port_monthly['MGMTS']=risk_port_monthly['SLMGMT']-risk_port_monthly['SHMGMT']
    risk_port_monthly['MGMTB']=risk_port_monthly['BLMGMT']-risk_port_monthly['BHMGMT']
    risk_port_monthly['MGMT']=(1/2)*(risk_port_monthly['MGMTS']+risk_port_monthly['MGMTB'])
    risk_port_monthly['PERFS']=risk_port_monthly['SLPERF']-risk_port_monthly['SHPERF']
    risk_port_monthly['PERFB']=risk_port_monthly['BLPERF']-risk_port_monthly['BHPERF']
    risk_port_monthly['PERF']=(1/2)*(risk_port_monthly['PERFS']+risk_port_monthly['PERFB']) 
    risk_port_monthly['misS']=(1/2)*(risk_port_monthly['SNMGMT']+risk_port_monthly['SNPERF'])
    risk_port_monthly['misB']=(1/2)*(risk_port_monthly['BNMGMT']+risk_port_monthly['BNPERF'])
    risk_port_monthly['misSmB']=risk_port_monthly['misS']-risk_port_monthly['misB']


    risk_port_monthly=risk_port_monthly.merge(rf,on=['Year','Month'],how='left')
    risk_port_monthly['RM-rf']=risk_port_monthly['RM']-risk_port_monthly['rf']*(1/12)

    risk_port_monthly_stat=risk_port_monthly.describe().T
    risk_port_monthly_stat['tstat']=risk_port_monthly_stat['mean']/(risk_port_monthly_stat['std']/np.sqrt(risk_port_monthly_stat['count']))

    return risk_port_monthly, risk_port_monthly_stat