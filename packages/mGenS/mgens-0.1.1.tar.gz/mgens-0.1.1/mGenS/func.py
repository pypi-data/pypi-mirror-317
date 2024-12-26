"""
FUNCTIONS POOL
"""
import pandas as pd
import re

from dateutil.relativedelta import relativedelta

# Define parameters
#####################################################################################
ADMIN_LIST = ['ADMIN', 'APAC', 'BD', 'CDCO', 'Channel', 'ComEx', 'Compliance',
              'Demand Planning','FIN', 'Finance', 'GA', 'GAMA', 'GM',
              'Global', 'HR', 'IT', 'MA', 'MKT', 'MPA', 'MPA ', 'New Channel',
              'ORS', 'People', 'QA', 'RA', 'RQA', 'SUCH']
NDS_LIST = ['National Sales Manager','National Sales Director','Sales Administrator']
ASM_LIST = ['Area Sales Manager','Local Marketing Partner','Regional Sales Manager','Head of HK and Macao']
DSM_LIST = ['Territory Sales Manager','District Sales Manager','Sales Manager, non-public','Territory Manager WC',
            'Local Marketing Manager','Regional Product Manager, Taiwan']
REP_LIST = ['Key Account Manager','Senior Product Specialist','Product Specialist']
FP_400_LIST = ['400 PIM', '400 BURNS', '400 SCAR', '400 INC', '400 INC_AGV2',
               '400 INC_V1V2', '400 INC_V2', '400 OTHERS']
euRate = 7.9449
hkRate =  0.929294962 


# Self-defined functions
#####################################################################################
# manipulation functions for quarterly territories
def manipulator(initDF, Q):
    tempDF = initDF[['代表岗位号','医院编码']].copy()
    tempDF['区域版本'] = Q

    return tempDF

# merge multiple lists into one
def merge_lists(*lists):
    merged_set = set()
    for lst in lists:
        merged_set.update(lst)
    return list(merged_set)

# search through product lists to find matching columns
def save_matching_value(row):
    col_name = row['Product List']
    if col_name in FP_400_LIST:
        return row[col_name]
    return None

# find last non zero value within the group
def last_non_zero(series):
    non_zero_series = series[series!=0]
    if not non_zero_series.empty:
        return non_zero_series.iloc[-1]
    else:
        return 0

# only keep the last non zero value within the group
def keep_last_non_zero(group):
    last_non_zero_idx = group[group != 0].index[-1] if (group != 0).any() else None
    if last_non_zero_idx is not None:
        mask = group.index != last_non_zero_idx
        group.loc[mask] = 0
    return group

# remove the last number in account id
def remove_last_number(s):
    # Find all numbers in the string
    numbers = re.findall(r'\d+', s)
    if numbers:
        # Remove the last number found
        s = re.sub(r'(\d+)(?!.*\d)', '', s)
    return s

def fill_missing(df):
    df = df.reset_index(drop=True)
    df['representativeID'] = df.groupby('KEY')['representativeID'].transform(lambda x:x.ffill().bfill())
    
    return df

def fill_na(row):
    # Convert row to a list to work with indices
    row_list = row.tolist()
    
    # Find the first and last non-NA indices
    try:
        first_non_na = next(i for i, val in enumerate(row_list) if pd.notna(val))
    except StopIteration:
        first_non_na = None
    
    try:
        last_non_na = len(row_list) - next(i for i, val in enumerate(reversed(row_list)) if pd.notna(val)) - 1
    except StopIteration:
        last_non_na = None
    
    # Fill NA values before the first non-NA value with "非目标医院"
    if first_non_na is not None:
        for i in range(first_non_na):
            if pd.isna(row_list[i]):
                row_list[i] = "非目标医院"
    
    # Fill NA values after the last non-NA value with "目标医院"
    if last_non_na is not None:
        for i in range(last_non_na + 1, len(row_list)):
            if pd.isna(row_list[i]):
                row_list[i] = "目标医院"
    
    # Convert back to pandas Series
    return pd.Series(row_list, index=row.index)

# Functions for SIP calculation
#####################################################################################
# general payout rate calculation
def payoutCalculator(achievement_rate):
    if achievement_rate < 0.9:
        return 0
    elif achievement_rate > 1.0:
        return 1
    else:
        return max(0,min(1, 0.5+(achievement_rate-0.9)*5))
    
# general focus products payout rate calculation
def payoutCalculatorFP(achievement_rate):
    if achievement_rate < 0.9:
        return 0
    elif achievement_rate >= 1.25:
        return 2.5
    elif (achievement_rate > 0.9) & (achievement_rate < 1.0):
        return max(0,min(1, 0.5+(achievement_rate-0.9)*5))
    elif (achievement_rate >= 1.0) & (achievement_rate < 2.5):
        return max(1,min(2.5, 1+(achievement_rate-1)*6))

def bonusPool(df):
    # Step 1: Create columns for adjusted sales and achievement percentage
    df['Adj IMS'] = df['IMS']
    df['Adj 单季度'] = df['单季度']

    # Step 2: Group data by representative
    reps = df[df.columns[0]]

    # Step 3: Adjust performance for each representative
    for rep in reps:
        rep_data = df[df[df.columns[0]]==rep]
        
        # Sort quarters to ensure we adjust from earliest to latest
        rep_data = rep_data.sort_values('区域版本')

        # Lists to store indices of underachieved and overachieved quarters
        underachieved_indices = []
        overachieved_indices = []

        # Identify underachieved and overachieved quarters
        for index, row in rep_data.iterrows():
            if row['单季度'] < 1:
                underachieved_indices.append(index)
            elif row['单季度'] > 1:
                overachieved_indices.append(index)

        # Step 4: Redistribute overachieved sales to underachieved quarters
        for over_idx in overachieved_indices:
            surplus_sales = df.loc[over_idx, 'IMS'] - df.loc[over_idx, 'Total_TGT']
            
            # Adjust each underachieved quarter with the surplus
            for under_idx in underachieved_indices:
                if surplus_sales > 0:
                    needed_sales = df.loc[under_idx, 'Total_TGT'] - df.loc[under_idx, 'IMS']
                    
                    if surplus_sales >= needed_sales:
                        # Fully compensate the underachieved quarter
                        df.loc[under_idx, 'Adj IMS'] += needed_sales
                        df.loc[under_idx, 'Adj 单季度'] = (df.loc[under_idx, 'Adj IMS'] / df.loc[under_idx, 'Total_TGT'])
                        surplus_sales -= needed_sales
                    else:
                        # Partially compensate the underachieved quarter
                        df.loc[under_idx, 'Adj IMS'] += surplus_sales
                        df.loc[under_idx, 'Adj 单季度'] = (df.loc[under_idx, 'Adj IMS'] / df.loc[under_idx, 'Total_TGT'])
                        surplus_sales = 0

            # Update the overachieved quarter's adjusted sales and 单季度
            df.loc[over_idx, 'Adj IMS'] = df.loc[over_idx, 'Total_TGT'] + surplus_sales
            df.loc[over_idx, 'Adj 单季度'] = (df.loc[over_idx, 'Adj IMS'] / df.loc[over_idx, 'Total_TGT'])

    return df


# Functions for PM&I Master
#####################################################################################
# Calculate 2024 IMS records based on 400 product groups
def PD400calculator(dfIMSRaw, list_400, TA):
    df = dfIMSRaw[(dfIMSRaw['Year']==2024)&(dfIMSRaw['Customer ID'].isin(list_400))&
                  (dfIMSRaw['Product ID'].isin(TA))].groupby('Customer ID')['IMS'].sum().reset_index()
    
    return df

def PD400Evaluator(dfIMSRaw, list_400, TA):
    df = pd.DataFrame(columns=['Customer ID','sum','count'])
    for i in list_400:
        result = dfIMSRaw[(dfIMSRaw['Year']==2024)&(dfIMSRaw['Customer ID']==i)&(dfIMSRaw['Product ID'].isin(TA))]
        if len(result) == 0:
            pass
        else:
            begin_window = result['Date'].iloc[0]
            end_window = begin_window + relativedelta(months=+6)
            
            temp = dfIMSRaw[(dfIMSRaw['Date']>=begin_window)&(dfIMSRaw['Date']<=end_window)&(dfIMSRaw['Customer ID']==i)&
                        (dfIMSRaw['Product ID'].isin(TA))].groupby('Customer ID')['IMS'].agg(['sum','count']).reset_index()
            df = pd.concat([df, temp], ignore_index=True)
        
    return df

# FP Master Generator Module
def focusproductGenerator(territory, FP, Q):
    """
    因为代表维度指标 != 经理维度指标 != 大区总指标, 所以需要生成以下DUMMY ID来补齐缺口

    Parameters
    ----------
    param Q: Current quarter


    Returns
    -------
    Quarterly FP territory at hospital level
    """
    speical_rep = ['内蒙古CNA_NMG1','新疆CNA_XJ1','西藏CNA_SC1','青海CNA_QH1','甘肃CNA_GS1']
    speical_province = ['西藏','内蒙古','青海']
    speical_area = ['吉林','山西']
    
    ## Merge hospital targets with FPs targets
    Q1FP = territory[(territory['区域版本']==Q)&
                     (~territory['医院编码'].isna())].merge(FP[['医院代码', 'FP', 'PIM_Act','BURNS_Act', 'Incision_Act', 'SCAR_Act']].drop_duplicates(), how='left',
                                                           left_on='医院编码', right_on='医院代码')\
                                                    .rename({'PIM_Act': 'PIM', 'BURNS_Act': 'BURNS', 'Incision_Act':'INCISION', 'SCAR_Act':'SCAR'}, axis=1)\
                                                    .drop('医院代码', axis=1)
    
    ## Summarize representative targets
    repFPQ1 = Q1FP.groupby(['省份','代表岗位号'])[['PIM','BURNS', 'INCISION', 'SCAR']].sum().reset_index()\
                  .merge(FP[['Province', 'PIM.1', 'BURNS.1','Incision Care.1', 'SCAR.1']].drop_duplicates(), how='left',left_on='省份', right_on='Province')
    repFPQ1['key'] = repFPQ1['省份']+repFPQ1['代表岗位号']

    ## Setting FPs target = 0 for 1代1省份
    
    repFPQ1.loc[repFPQ1['key'].isin(speical_rep),['PIM','BURNS', 'INCISION', 'SCAR']] = 0
    # 指标不满6w升级到6w
    # 设置6w指标，给予代表获奖资格，但该6w不计入经理指标
    repFPQ1.loc[(~repFPQ1['key'].isin(speical_rep))&(repFPQ1['PIM.1']==1)&(repFPQ1['PIM']<60000),'PIM'] = 60000
    repFPQ1.loc[(~repFPQ1['key'].isin(speical_rep))&(repFPQ1['BURNS.1']==1)&(repFPQ1['BURNS']<60000),'BURNS'] = 60000
    repFPQ1.loc[(~repFPQ1['key'].isin(speical_rep))&(repFPQ1['Incision Care.1']==1)&(repFPQ1['INCISION']<60000),'INCISION'] = 60000
    repFPQ1.loc[(~repFPQ1['key'].isin(speical_rep))&(repFPQ1['SCAR.1']==1)&(repFPQ1['SCAR']<60000),'SCAR'] = 60000

    # Sum FPs targets at representative level
    repFPQ1['FP'] = repFPQ1[['PIM','BURNS', 'INCISION', 'SCAR']].sum(axis=1)
    repFPQ1 = repFPQ1[['省份','代表岗位号','PIM','BURNS', 'INCISION', 'SCAR']].rename({'PIM': 'PIM_Act', 'BURNS': 'BURNS_Act', 
                                                                                'INCISION':'Incision_Act', 'SCAR':'SCAR_Act'}, axis=1)
    ## Calculate gaps between two versions
    repGap = repFPQ1.merge(Q1FP.groupby(['省份','代表岗位号'])[['PIM','BURNS', 'INCISION', 'SCAR']].sum().reset_index()\
                               .rename({'PIM': 'PIM_Prop', 'BURNS': 'BURNS_Prop', 'INCISION':'Incision_Prop', 'SCAR':'SCAR_Prop'}, axis=1), 
                           how='left', on=['省份','代表岗位号'])
    repGap['PIM'] = repGap['PIM_Act']-repGap['PIM_Prop']
    repGap['BURNS'] = repGap['BURNS_Act']-repGap['BURNS_Prop']
    repGap['INCISION'] = repGap['Incision_Act']-repGap['Incision_Prop']
    repGap['SCAR'] = repGap['SCAR_Act']-repGap['SCAR_Prop']
    repGap['FP'] = repGap[['PIM','BURNS', 'INCISION', 'SCAR']].sum(axis=1)
    repGap = repGap[repGap['FP']!=0]

    # Create dummy hospital KPIs
    repGap = repGap[['省份','代表岗位号','FP','PIM','BURNS', 'INCISION', 'SCAR']].merge(Q1FP[['代表姓名','代表岗位号']].drop_duplicates(), how='left', on='代表岗位号')
    # create dummy customer ID
    repGap['医院编码'] = 'MNK'+repGap['代表岗位号'].str.split('_' ,expand=True)[1]
    repGap['医院编码'] = repGap['医院编码'].apply(lambda x: x.ljust(10, '0'))
    # create other attributes
    repGap['区域'] = 'Greater China'
    repGap[['大区','省份','城市','地区经理']] = '其他'
    repGap['地区经理岗位号'] = 'DSM_DUMMY'
    repGap['医院名称'] = 'DUMMY'
    repGap['医院级别'] = 'O'
    repGap['医院指标(KCNY)'] = 0
    repGap['区域版本'] = Q
    
    ## Combine FPs targets
    # Q1FP = pd.concat([Q1FP, repGap[Q1FP.columns]], ignore_index=True, sort=False)
    
    ## Summarize district manager targets
    dsmFPQ1 = Q1FP.groupby(['省份','地区经理岗位号'])[['PIM','BURNS', 'INCISION', 'SCAR']].sum().reset_index()\
                  .merge(FP[['Province', 'PIM.1', 'BURNS.1','Incision Care.1', 'SCAR.1']].drop_duplicates(), how='left',left_on='省份', right_on='Province')
    dsmFPQ1 = dsmFPQ1[dsmFPQ1['省份']!='其他']

    ## Setting FPs target = 0 for 1代1省份
    dsmFPQ1.loc[dsmFPQ1['省份'].isin(speical_province),['PIM','BURNS', 'INCISION', 'SCAR']] = 0
    # Mark province with promoted district KPIs that not included in area KPI
    speicalDSM = dsmFPQ1[~(dsmFPQ1['省份'].isin(speical_province))&
                         ((dsmFPQ1['PIM']==0)&(dsmFPQ1['PIM.1']==1)|
                          (dsmFPQ1['BURNS']==0)&(dsmFPQ1['BURNS.1']==1)|
                          (dsmFPQ1['INCISION']==0)&(dsmFPQ1['Incision Care.1']==1)|
                          (dsmFPQ1['SCAR']==0)&(dsmFPQ1['SCAR.1']==1))]

    # 指标不满6w升级到6w
    # 设置6w指标，给予代表获奖资格，但该6w不计入经理指标
    dsmFPQ1.loc[(~dsmFPQ1['省份'].isin(speical_province))&(dsmFPQ1['PIM.1']==1)&(dsmFPQ1['PIM']<100000),'PIM'] = 100000
    dsmFPQ1.loc[(~dsmFPQ1['省份'].isin(speical_province))&(dsmFPQ1['BURNS.1']==1)&(dsmFPQ1['BURNS']<100000),'BURNS'] = 100000
    dsmFPQ1.loc[(~dsmFPQ1['省份'].isin(speical_province))&(dsmFPQ1['Incision Care.1']==1)&(dsmFPQ1['INCISION']<100000),'INCISION'] = 100000
    dsmFPQ1.loc[(~dsmFPQ1['省份'].isin(speical_province))&(dsmFPQ1['SCAR.1']==1)&(dsmFPQ1['SCAR']<100000),'SCAR'] = 100000

    dsmFPQ1['FP'] = dsmFPQ1[['PIM','BURNS', 'INCISION', 'SCAR']].sum(axis=1)
    dsmFPQ1 = dsmFPQ1[['省份','地区经理岗位号','PIM','BURNS', 'INCISION', 'SCAR']].rename({'PIM': 'PIM_Act', 'BURNS': 'BURNS_Act', 'INCISION':'Incision_Act', 'SCAR':'SCAR_Act'}, axis=1)

    ## Calculate gaps between two versions
    dsmGap = dsmFPQ1.merge(Q1FP[Q1FP['省份']!='其他'].groupby(['省份','地区经理岗位号'])[['PIM','BURNS', 'INCISION', 'SCAR']].sum().reset_index()\
                               .rename({'PIM': 'PIM_Prop', 'BURNS': 'BURNS_Prop', 'INCISION':'Incision_Prop', 'SCAR':'SCAR_Prop'}, axis=1), 
                           how='left', on=['省份','地区经理岗位号'])
    dsmGap['PIM'] = dsmGap['PIM_Act']-dsmGap['PIM_Prop']
    dsmGap['BURNS'] = dsmGap['BURNS_Act']-dsmGap['BURNS_Prop']
    dsmGap['INCISION'] = dsmGap['Incision_Act']-dsmGap['Incision_Prop']
    dsmGap['SCAR'] = dsmGap['SCAR_Act']-dsmGap['SCAR_Prop']
    dsmGap['FP'] = dsmGap[['PIM','BURNS', 'INCISION', 'SCAR']].sum(axis=1)
    dsmGap = dsmGap[dsmGap['FP']!=0]
    
    # print(dsmGap)
    
    dsmGap.loc[dsmGap['省份']=='吉林','SCAR'] = 0
    dsmGap.loc[dsmGap['省份']=='山西','BURNS'] = 0

    # Create dummy hospital KPIs
    dsmGap = dsmGap[['省份','地区经理岗位号','FP','PIM','BURNS', 'INCISION', 'SCAR']].merge(Q1FP[['地区经理','地区经理岗位号','大区']].drop_duplicates(), how='left', on='地区经理岗位号')
    # create dummy customer ID
    dsmGap['医院编码'] = 'MNK'+dsmGap['地区经理岗位号'].str.split('_' ,expand=True)[1]
    dsmGap['医院编码'] = dsmGap['医院编码'].apply(lambda x: x.ljust(10, '0'))
    # create other attributes
    dsmGap['区域'] = 'Greater China'
    dsmGap[['城市','代表姓名']] = '其他'
    dsmGap['代表岗位号'] = 'CNA_DUMMY'
    dsmGap['医院名称'] = 'DUMMY'
    dsmGap['医院级别'] = 'O'
    dsmGap['医院指标(KCNY)'] = 0
    dsmGap['区域版本'] = Q

    ## Combine FPs targets
    # Q1FP = pd.concat([Q1FP, dsmGap[Q1FP.columns]], ignore_index=True, sort=False)
    
    ## Summarize area manager targets
    asmFPQ1 = Q1FP.groupby(['大区'])[['PIM','BURNS', 'INCISION', 'SCAR']].sum().reset_index().rename({'PIM': 'PIM_Act', 'BURNS': 'BURNS_Act', 'INCISION':'Incision_Act', 'SCAR':'SCAR_Act'}, axis=1)

    ## Calculate gaps between two versions
    asmGap = asmFPQ1.merge(Q1FP[Q1FP['省份']!='其他'].groupby(['大区'])[['PIM','BURNS', 'INCISION', 'SCAR']].sum().reset_index()\
                               .rename({'PIM': 'PIM_Prop', 'BURNS': 'BURNS_Prop', 'INCISION':'Incision_Prop', 'SCAR':'SCAR_Prop'}, axis=1), 
                           how='left', on=['大区'])
    asmGap['PIM'] = asmGap['PIM_Act']-asmGap['PIM_Prop']
    asmGap['BURNS'] = asmGap['BURNS_Act']-asmGap['BURNS_Prop']
    asmGap['INCISION'] = asmGap['Incision_Act']-asmGap['Incision_Prop']
    asmGap['SCAR'] = asmGap['SCAR_Act']-asmGap['SCAR_Prop']
    
    # asmGap.loc[asmGap['大区']=='Central','BURNS'] = asmGap[asmGap['大区']=='Central']['BURNS']-100000
    # asmGap.loc[asmGap['大区']=='North','SCAR'] = asmGap[asmGap['大区']=='North']['SCAR']-100000
    # asmGap.loc[asmGap['大区']=='South','BURNS'] = asmGap[asmGap['大区']=='South']['BURNS']-100000
    
    asmGap['FP'] = asmGap[['PIM','BURNS', 'INCISION', 'SCAR']].sum(axis=1)
    asmGap = asmGap[asmGap['FP']!=0]

    # Create dummy hospital KPIs
    asmGap = asmGap[['大区','FP','PIM','BURNS', 'INCISION', 'SCAR']]
    # create dummy customer ID
    asmGap['医院编码'] = 'MNK'+asmGap['大区']
    asmGap['医院编码'] = asmGap['医院编码'].apply(lambda x: x.ljust(10, '0'))
    # create other attributes
    asmGap['区域'] = 'Greater China'
    asmGap[['省份','城市','地区经理','代表姓名']] = '其他'
    asmGap['代表岗位号'] = 'CNA_DUMMY'
    asmGap['地区经理岗位号'] = 'DSM_DUMMY'
    asmGap['医院名称'] = 'DUMMY'
    asmGap['医院级别'] = 'O'
    asmGap['医院指标(KCNY)'] = 0
    asmGap['区域版本'] = Q

    ## Combine FPs targets
    Q1FP = pd.concat([Q1FP, repGap[Q1FP.columns], dsmGap[Q1FP.columns],asmGap[Q1FP.columns]], ignore_index=True, sort=False)

    return Q1FP

