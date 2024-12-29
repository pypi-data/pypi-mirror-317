import pandas as pd
import numpy as np
from feature_engine.outliers import Winsorizer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant



def Outlier_IQR(df,columns):
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (1.5 * IQR)
        LL = df[i].quantile(0.25) - (1.5 * IQR)

        df[i] = np.where(df[i] > UL, UL, np.where(df[i] < LL , LL, df[i]))
    return df



def Outlier_Winsorizer(df, column, capping_method='iqr'):
    winsor = Winsorizer(capping_method=capping_method,
                        tail='both',
                        fold=1.5,
                        variables=[column])
    
    df[column] = winsor.fit_transform(df[[column]])
    return df



def Outlier_Clip(df,columns):
    for column in columns:
        df[column] = df[column].clip(lower=df[column].quantile(0.05), upper=df[column].quantile(0.95))
    return df


def MissingVal_Repl(df, columns, type='mean'):
    for i in columns:
        if type == 'mean':
            value = df[i].mean()
        elif type == 'median':
            value = df[i].median()
        elif type == 'mode':
            value = df[i].mode()[0]  
        
        df[i] = df[i].replace(np.nan, value)
    return df


def MissingVal_Imputer(df,columns,strategy='mean'):
    if strategy == 'mode':
        strategy = 'most_frequent'

    imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
    for i in columns:
        df[i] = pd.DataFrame(imputer.fit_transform(df[[i]]))
    return df
    

def MissingVal_Fillna(df):
    num_cols = df.select_dtypes(include=['float', 'int']).columns
    for x in num_cols:
        df[x] = df[x].fillna(df[x].mean())

    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for y in cat_cols:
        df[y] = df[y].fillna(df[y].mode()[0])
    return df


## VERSION 1.3

def outlierColumns(df):
    outl_cols = []
    for i in df.columns:
        if pd.api.types.is_numeric_dtype(df[i]):
            IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
            LLi = df[i].quantile(0.25) - (1.5 * IQR)
            ULi = df[i].quantile(0.75) + (1.5 * IQR)
            
            if ((df[i] < LLi) | (df[i] > ULi)).sum() > 0:
                outl_cols.append(i)
    return outl_cols



def outlierCount(df, columns):
    plt.ioff()
    for i in columns:
        oc = len(plt.boxplot(df[i])['fliers'][0].get_ydata())
        print(f"{i} = {oc}")



def highFrequency(df, perc=0.5):
    high_freq_columns = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            value_counts = df[col].value_counts()
            max_count = value_counts.max()
            total_count = len(df)
            
            if max_count / total_count > perc:
                high_freq_columns.append(col)
    return high_freq_columns


## VERSION 1.4

def Encoding(df,method='label'):
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if method == 'label':
        label = LabelEncoder()
        for col in cat_cols:
            df[col] = label.fit_transform(df[col])
    elif method == 'onehot':
        df = pd.get_dummies(df, columns=cat_cols)
    return df


def Scaling(df, method='minmax'):
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'robust':
        scaler = RobustScaler()
        
    df = pd.DataFrame(scaler.fit_transform(df),columns=df.columns)
    return df
    


## VERSION 1.6
# Redundant Codes removed

## VERSION 1.9

def Outlier_MMM(df, columns, type='median'):
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        UL = df[i].quantile(0.75) + (1.5 * IQR)
        LL = df[i].quantile(0.25) - (1.5 * IQR)

        if type == 'mean':
            value = df[i].mean()
        elif type == 'median':
            value = df[i].median()
        elif type == 'mode':
            value = df[i].mode()[0]

        if df[i].dtype in ['int32', 'int64']:
            value = int(value)    
        
        df.loc[df[i] > UL, i] = value
        df.loc[df[i] < LL, i] = value

    return df


def LowVarianceCols(df):
    LowVar = []
    columns = df.describe(include = ['int','float']).columns
    for i in columns:
        IQR = df[i].quantile(0.75) - df[i].quantile(0.25)
        if IQR == 0:
            LowVar.append(i)
         
    return LowVar


## VERSION 2.0

def MissingVal_Interpolate(df,type='linear'):
    num_cols = df.select_dtypes(include=['float', 'int']).columns
    for i in num_cols:
        if type == 'linear':
            df[i] = df[i].interpolate(method='linear')
        elif type == 'polynomial':
            df[i] = df[i].interpolate(method='polynomial', order=2)
        elif type == 'spline':
            df[i] = df[i].interpolate(method='spline', order=3)
    return df


def Lineplot_Multi(df, inpCol, outCol, figsize=(15, 5)):

    n_plots = len(inpCol)
    n_rows = int(np.ceil(n_plots / 3))
    plt.figure(figsize=(figsize[0], figsize[1] * n_rows))
    
    for i, col in enumerate(inpCol, 1): 
        plt.subplot(n_rows, 3, i)  
        sns.lineplot(data=df, x=col, y=outCol)
        plt.title(col)  
        plt.xlabel(col)  
        plt.ylabel(outCol) 
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()



def Lineplot_Single(df, inpCol, outCol):
    plt.figure(figsize=(10,9))
    
    for col in inpCol:
        sns.lineplot(data=df, x=col, y=outCol, label=col)
    
    plt.title(f"{outCol} vs Input Columns")
    plt.xlabel("Input Columns")
    plt.ylabel(outCol)
    plt.legend(title="Input Columns")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

## VERSION 2.1

def RegressionPlot_Multiple(df, inpCol, outCol, figsize=(15, 5)):
   
    n_plots = len(inpCol)
    n_rows = int(np.ceil(n_plots / 3))
    plt.figure(figsize=(figsize[0], figsize[1] * n_rows))
    
    for i, col in enumerate(inpCol, 1):
        plt.subplot(n_rows, 3, i) 
        sns.regplot(data=df, x=col, y=outCol, ci=None,line_kws={'color':'red'})    
        plt.title(f'Regression: {col} vs {outCol}')
        plt.xlabel(col)  
        plt.ylabel(outCol)  
        plt.grid(True)
    
    plt.tight_layout()
    plt.show()



def VIF(X):
    X = add_constant(X)
    vif_df = pd.DataFrame()
    vif_df["Variable"] = X.columns[1:]

    vif_values = []
    for i in range(1,X.shape[1]):
        vif = variance_inflation_factor(X.values, i)
        vif_values.append(vif)

    vif_df["VIF"] = vif_values
    return vif_df    


## VERSION 2.1.1
# Redundant Codes removed