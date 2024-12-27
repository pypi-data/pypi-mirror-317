''' Returns CSI value for each variable to measure data drift in validation data wrt modeling data '''

import pandas as pd
import numpy as np

def CSI_calc(data1, data2, dec_sm, model_cols_input):
    
    count_sm = 0
    csi_mod_vs_oot = pd.DataFrame()
    var_issues=[]
    for var in model_cols_input:
        #print(var)
        try:
            count_sm = count_sm+1
            temp = data1[[var]]
            temp_oot = data2[[var]]
            
            if len(temp[temp[var] == 0]) > 0:
              temp_0 = temp[temp[var] == 0]
              #print(len(temp_0))
              temp_non0 = temp[temp[var] != 0]

              temp_non0['decile'] = pd.qcut(temp[var],dec_sm,duplicates='drop')
              temp_0['decile'] = '[0]'

              temp = temp_0.append(temp_non0)
  
            else:
              temp['decile'] = pd.qcut(temp[var],dec_sm,duplicates='drop')

            if len(temp['decile'].drop_duplicates()) < 2:
                temp['decile'] = temp[var].apply(lambda x: 'value_'+str(x))

          #### Get the bins created in the training data and define the same in the whole modeling data

            bins_training = temp.groupby('decile', as_index=False).agg({var:'min'})
            bins_training = bins_training.sort_values(by=[var])
            bins_training = bins_training.reset_index(drop=True)
            #print(bins_training)
            if bins_training[var].loc[0] > 0:
              bins_training[var].loc[0] = 0



            temp_oot['decile'] = np.nan
            for i in range(0,len(bins_training)):
                key = bins_training['decile'].loc[i]
                value = bins_training[var].loc[i]
                if(key=='[0]'):
                   temp_oot['decile'][temp_oot[var] == value] = key
                else:
                  temp_oot['decile'][temp_oot[var] >= value] = key


            if len(temp['decile'][temp[var].isnull()== True]) > 0:
                temp['decile'] = temp['decile'].astype("category")
                temp['decile'] = temp['decile'].cat.add_categories('Unknown')
                temp['decile'] = temp['decile'].fillna("Unknown")

            if temp_oot[var].isna().sum()>0 and temp[var].isna().sum()==0:
                temp['decile'] = temp['decile'].astype("category")
                temp['decile'] = temp['decile'].cat.add_categories('Unknown')
                temp['decile'] = temp['decile'].fillna("Unknown")
    #                 print (var)
    #                 print (len(temp['decile'][temp['decile'].isnull() == True]))
    #                 print ('---------')

            temp_oot['decile'] = temp_oot['decile'].fillna("Unknown")



            t1 = pd.DataFrame(temp['decile'].value_counts())
            t1 = t1.reset_index()
            t1 = t1.rename(columns={'index':'bins',
                             'decile':'count_oot1'})

            t1_oot = pd.DataFrame(temp_oot['decile'].value_counts())
            t1_oot = t1_oot.reset_index()
            t1_oot = t1_oot.rename(columns={'index':'bins',
                             'decile':'count_oot2'})

            t1_all = t1.merge(t1_oot, on='bins', how='outer', indicator=True)
    #             if((t1_all['_merge'].value_counts()['left_only']!=0) or (t1_all['_merge'].value_counts()['right_only']!=0)):
    #               print (t1_all['_merge'].value_counts())

            t1_all['pct_oot1'] = np.nan
            t1_all['pct_oot2'] = np.nan
            t1_all['diff'] = np.nan
            t1_all['log'] = np.nan
            t1_all['csi_decile'] = np.nan

            for j,row in t1_all.iterrows():
                if(row['_merge']=='left_only'):
                    t1_all.at[j, 'count_oot2'] = 0
                elif(row['_merge']=='right_only'):
                    t1_all.at[j, 'count_oot1'] = 0

            t1_all['pct_oot1'] = t1_all['count_oot1'].apply(lambda x: float(x) / t1_all['count_oot1'].sum())
            t1_all['pct_oot2'] = t1_all['count_oot2'].apply(lambda x: float(x) / t1_all['count_oot2'].sum())

            t1_all['diff'] = t1_all['pct_oot1'] - t1_all['pct_oot2']
            t1_all['log'] = np.nan
            t1_all['log'][t1_all['_merge'] == 'both'] = t1_all[t1_all['_merge'] == 'both'].apply(lambda x: np.log(x.pct_oot1/x.pct_oot2), axis=1)
            t1_all['log'][t1_all['_merge'] == 'left_only'] = t1_all[t1_all['_merge'] == 'left_only'].apply(lambda x: 1, axis=1)

            t1_all['csi_decile'] = t1_all['diff'] * t1_all['log']

            t1_all['variable_name'] = var

            csi_mod_vs_oot = csi_mod_vs_oot.append(t1_all)

        except:
            var_issues.append(var)

    return (csi_mod_vs_oot, var_issues)

# psi_calc, issues = CSI_calc(df1, df2, 10, col_for_model)
# csi = psi_calc.groupby('variable_name', as_index=False).agg({'csi_decile':'sum'})
# issues_df = pd.DataFrame(issues, columns=['issues_vars'])