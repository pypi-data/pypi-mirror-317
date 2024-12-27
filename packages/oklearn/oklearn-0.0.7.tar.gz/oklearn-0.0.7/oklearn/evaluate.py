import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics

# measure_prediction_accuracy
def MAE(y_true, y_pred):  # Mean Absolute Error
    return np.mean(np.abs(y_true - y_pred)) # metrics.mean_absolute_error

def ME(y_true, y_pred):  # Mean Error
    return np.mean(y_true - y_pred)

def MPE(y_true, y_pred):  # Mean Percentage Error
    for y in y_true:
        if y == 0:
            print('zero division is not possible')
            return
    return np.mean((y_true - y_pred) / y_true) * 100

def MAPE(y_true, y_pred):  # Mean Absolute Percentage Error
    return np.mean(np.abs(y_true - y_pred) / y_true) * 100

def MAPER(y_true, y_pred):  # Mean Absolute Percentage Error Revised
    return np.mean((y_true - np.abs(y_pred - y_true)) / y_true * 100)

def MSE(y_true, y_pred):  # Mean Squared Error
    error = np.square(y_true - y_pred)  # (y_true - y_pred)**2
    # metrics.mean_squared_error
    return np.mean(error)

def RMSE(y_true, y_pred):  # Root Mean Squared Error
    error = np.square(y_true - y_pred)  # (y_true - y_pred)**2
    mse = np.mean(error)
    return np.sqrt(mse)

# log 값 변환 시 NaN등의 이슈로 log() 가 아닌 log1p() 를 이용하여 RMSLE 계산
def RMSLE(y, pred):
    log_y = np.log1p(y)
    log_pred = np.log1p(pred)
    squared_error = (log_y - log_pred) ** 2
    rmsle = np.sqrt(np.mean(squared_error))
    return rmsle

# model 평가
def evaluate_model(model, x_data, y_data, labels):
    y_pred = model.predict(x_data)
    score = metrics.f1_score(y_data, y_pred, average='macro', labels=labels)
    print('F1-score: {0:.2f} %'.format(score*100))
    return y_pred

# feature importance 시각화
def plot_feature_importance(model, columns):
    try:
        feature_importance = model.feature_importances_
    except:
        feature_importance = [abs(i) for i in model.coef_[0]]
    
    plt.figure(figsize=(8,6))
    plt.title('Feature importance')
    plt.barh(y = columns, width = feature_importance)
    plt.show()

def get_clf_eval(y_true, y_pred, labels, target_names):
    output_labels = []
    output = []    
    # print('Classfication report:\n', 
    #       metrics.classification_report(y_true, y_pred, labels=labels, 
    #                                    target_names=target_names))    
    cm = metrics.confusion_matrix(y_true, y_pred, labels=labels)
    # print('Confusion matrix:\n', cm)
    
    # np.trace(cm): confusion matrix의 대각 원소의 합 (정확히 예측된 경우)
    # np.sum(cm): confusion matrix의 모든 원소의 합
    accuracy = np.array( [round(np.trace(cm) / np.sum(cm), 3)] * len(labels) )
    precision = np.round(metrics.precision_score(y_true, y_pred, average=None, labels=labels), 3)
    recall = np.round(metrics.recall_score(y_true, y_pred, average=None, labels=labels), 3)
    f1_score = np.round(metrics.f1_score(y_true, y_pred, average=None, labels=labels), 3)
    # output.extend([accuracy.tolist(), precision.tolist(), recall.tolist(), f1_score.tolist()])
    output.extend([accuracy, precision, recall, f1_score])
    output_labels.extend(['accuracy', 'precision', 'recall', 'f1-score'])
    
    output_df = pd.DataFrame(output, columns=target_names)
    output_df['mean'] = output_df.mean(axis=1)
    print('Evaluation Metric:\n', output_df)

    # output_df = pd.DataFrame(output, columns=['mean'])
    output_df.index = output_labels
    return output_df

# 학습된 분류기들의 성능을 시각화 (recall)
def plot_evaluation(clfs, xlabel, start, stop, step, x_data, y_data, labels):
    x_plot = list()
    y_plot = list()

    for i in range(start, stop, step):
        x_plot.append(i)
        y_pred = clfs[i].predict(x_data)
        score = metrics.recall_score(y_data, y_pred, average='macro', labels=labels)
        y_plot.append(score)

    plt.figure(figsize=(8,6))
    plt.plot(x_plot, y_plot, 'g-')
    plt.title('Validation Recall')
    plt.xlabel(xlabel)
    plt.ylabel('Recall')
    plt.grid(alpha=0.3)
    plt.show()
    
    # best model 선택
    best_model = clfs[x_plot[np.argmax(y_plot)]]
    print(best_model)
    print('Recall: {0:.2f}'.format(y_plot[np.argmax(y_plot)]*100))
    return best_model
