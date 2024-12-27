from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from lightgbm import early_stopping
from oklearn import utility

@utility.measure_execution_time
def lr_clf(x_data, y_data):  ## LogisticRegression
    lr_clf = LogisticRegression(max_iter=100)
    lr_clf.fit(x_data, y_data)
    return lr_clf

@utility.measure_execution_time
def dt_clf(x_data, y_data):  ## Decision Tree
    dt_clf = DecisionTreeClassifier(random_state=1)
    dt_clf.fit(x_data, y_data)
    return dt_clf

@utility.measure_execution_time
def rf_clf(x_data, y_data):  ## Random Forest
    rf_clf = RandomForestClassifier(random_state=1)
    rf_clf.fit(x_data, y_data)
    return rf_clf

@utility.measure_execution_time
def xgb_wrapper(x_data, y_data):  ## XGBoost
    xgb_wrapper = XGBClassifier(random_state=1)
    xgb_wrapper.fit(x_data, y_data)
    return xgb_wrapper

@utility.measure_execution_time
def lgbm_wrapper(x_data, y_data):  ## LightGBM
    lgbm_wrapper = LGBMClassifier(random_state=1)
    lgbm_wrapper.fit(x_data, y_data)
    return lgbm_wrapper

@utility.measure_execution_time
def get_best_estimator(estimator, params, x_data, y_data):
    grid_cv = GridSearchCV(estimator, params, scoring=make_scorer(f1_score, average='macro'), 
                           n_jobs=-1, cv=3)
    grid_cv.fit(x_data, y_data)

    print('best parameters:', grid_cv.best_params_)
    print('best scores:', grid_cv.best_score_)
    
    return grid_cv.best_estimator_  # 학습된 모델

@utility.measure_execution_time
def get_best_lgbm_estimator(estimator, params, x_data, y_data, evals, stopping_rounds):
    grid_cv = GridSearchCV(estimator, params, scoring=make_scorer(f1_score, average='macro'), 
                           n_jobs=-1, cv=3)
    # grid_cv.fit(x_train_norm, y_train_over, early_stopping_rounds=100, eval_metric='auc_mu', eval_set=evals, 
    #             verbose=True)
    grid_cv.fit(x_data, y_data, callbacks=[early_stopping(stopping_rounds=stopping_rounds)], 
                eval_metric='auc_mu', eval_set=evals)

    print('best parameters:', grid_cv.best_params_)
    print('best scores:', grid_cv.best_score_)
    
    return grid_cv.best_estimator_  # 학습된 모델
