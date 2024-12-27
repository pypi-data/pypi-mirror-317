import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_outlier(df=None, column=None, weight=1.5):
    # 1/4 분위와 3/4 분위 지점을 np.percentile로 구함
    quantile_25 = np.quantile(df[column].values, .25)
    quantile_75 = np.quantile(df[column].values, .75)
    # quantile_25 = np.quantile(df[column].values, .25)
    # quantile_75 = np.quantile(df[column].values, .75)    
    # print('quantile_25:', quantile_25, 'quantile_75:', quantile_75)
    
    # IQR을 구하고, IQR에 1.5를 곱하여 최대값과 최소값 지점 구함
    iqr = quantile_75 - quantile_25
    
    iqr_weight = iqr * weight
    lowest_val = quantile_25 - iqr_weight  # 최소값: Q1 – 1.5 * IQR
    highest_val = quantile_75 + iqr_weight  # 최대값: Q3 + 1.5 * IQR    
    print(f'[{column}] iqr: {round(iqr, 1)}, lowest_val: {round(lowest_val, 1)}, highest_val: {round(highest_val, 1)}')
    
    threshold = {}
    threshold['lowest_val'] = lowest_val
    threshold['highest_val'] = highest_val
    
    # 최대값 보다 크거나, 최소값 보다 작은 값을 아웃라이어로 설정하고 DataFrame index 반환 
    # outlier_index = df[column][(df[column] < lowest_val) | (df[column] > highest_val)].index
    return threshold

def oversampling(x_train, y_train):
    print('before oversampling')
    print(x_train.shape, y_train.shape)
    print(y_train.value_counts().sort_index())
    print(round(y_train.value_counts().sort_index()/y_train.count()*100, 1))

    # !pip install imbalanced-learn
    from imblearn.over_sampling import SMOTE

    smote = SMOTE(random_state=1, k_neighbors=5)
    x_train_over, y_train_over = smote.fit_resample(x_train, y_train)  # train data only

    print('after oversampling')
    print(x_train_over.shape, y_train_over.shape)
    print(y_train_over.value_counts().sort_index())
    print(y_train_over.value_counts().sort_index()/y_train_over.count()*100)    

    # 데이터 증가율 = (new - origin) / origin x 100
    print(round((y_train_over.count() - y_train.count()) / y_train.count() * 100), '%')

    return x_train_over, y_train_over

def check_data_period(dataframes, labels):
    # dataframes = [failures, maintenance, errors, measures]
    # labels = ['failures', 'maintenance', 'errors', 'measures']
    # colors = ['red', 'green', 'blue', 'orange']

    plt.figure(figsize=(10, 6))

    for i, df in enumerate(dataframes):
        start_date = df['datetime'].min()
        end_date = df['datetime'].max()
        
        plt.barh(y=labels[i], width=(end_date - start_date).days, left=start_date, color='dodgerblue')

    plt.yticks(ticks=range(len(dataframes)), labels=labels)  # y축에 데이터 프레임 레이블 추가

    import matplotlib.dates as mdates
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # 월 단위로 주요 눈금 설정

    plt.title('Data period')
    # plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.xticks(rotation=70)
    plt.show()

# 데이터 건수 및 비율 확인
def check_data_ratio(column_name, count, raw_count):
    print(f'{column_name} 데이터 개수: {count}건, 비율: {round((count / raw_count * 100), 1)}%')

if __name__ == "__main__":
    df_contbr = pd.read_csv('../../../datasets/contrib/contrib.csv')
    outlier_index = get_outlier(df_contbr, 'contb_receipt_amt')
    print(outlier_index)
