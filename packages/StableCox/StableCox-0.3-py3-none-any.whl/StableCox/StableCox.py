from data.selection_bias import gen_selection_bias_data
from algorithm.SRDO import SRDO
from model.linear import get_algorithm_class
from metrics import get_metric_class
from utils import setup_seed, get_beta_s, get_expname, calc_var, pretty, get_cov_mask, BV_analysis
from Logger import Logger
from model.STG import STG
from sksurv.metrics import brier_score, cumulative_dynamic_auc
from sklearn.metrics import mean_squared_error
import numpy as np
import argparse
import os
import torch
from collections import defaultdict as dd
import pandas as pd
from sklearn.model_selection import train_test_split
from lifelines import CoxPHFitter
from sksurv.util import Surv
from lifelines.utils import concordance_index
def get_args():
    parser = argparse.ArgumentParser(description="Script to launch sample reweighting experiments", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # data generation
    parser.add_argument("--p", type=int, default=10, help="Input dim")
    parser.add_argument("--n", type=int, default=2000, help="Sample size")
    parser.add_argument("--V_ratio", type=float, default=0.5)
    parser.add_argument("--Vb_ratio", type=float, default=0.1)
    parser.add_argument("--true_func", choices=["linear",], default="linear")
    parser.add_argument("--mode", choices=["S_|_V", "S->V", "V->S", "collinearity"], default="collinearity")
    parser.add_argument("--misspe", choices=["poly", "exp", "None"], default="poly")
    parser.add_argument("--corr_s", type=float, default=0.9)
    parser.add_argument("--corr_v", type=float, default=0.1)
    parser.add_argument("--mms_strength", type=float, default=1.0, help="model misspecifction strength")
    parser.add_argument("--spurious", choices=["nonlinear", "linear"], default="nonlinear")
    parser.add_argument("--r_train", type=float, default=2.5, help="Input dim")
    parser.add_argument("--r_list", type=float, nargs="+", default=[-3, -2, -1.7, -1.5, -1.3, 1.3, 1.5, 1.7, 2, 3])
    parser.add_argument("--noise_variance", type=float, default=0.3)

    # frontend reweighting 
    parser.add_argument("--reweighting", choices=["None", "DWR", "SRDO"], default="DWR")
    parser.add_argument("--decorrelation_type", choices=["global", "group"], default="global")
    parser.add_argument("--order", type=int, default=1)
    parser.add_argument("--iters_balance", type=int, default=3000)

    parser.add_argument("--topN", type=int, default=10)
    # backend model 
    parser.add_argument("--backend", choices=["OLS", "Lasso", "Ridge", "Weighted_cox"], default="Weighted_cox")
    parser.add_argument("--paradigm", choices=["regr", "fs",], default="regr")
    parser.add_argument("--iters_train", type=int, default=5000)
    parser.add_argument("--lam_backend", type=float, default=0.01) # regularizer coefficient
    parser.add_argument("--fs_type", choices=["oracle", "None", "given", "STG"], default="STG")
    parser.add_argument("--mask_given", type=int, nargs="+", default=[1,1,1,1,1,0,0,0,0,0])
    parser.add_argument("--mask_threshold", type=float, default=0.2)
    parser.add_argument("--lam_STG", type=float, default=3)
    parser.add_argument("--sigma_STG", type=float, default=0.1)
    parser.add_argument("--metrics", nargs="+", default=["L1_beta_error", "L2_beta_error"])
    parser.add_argument("--bv_analysis", action="store_true")

    # others
    parser.add_argument("--seed", type=int, default=6)
    parser.add_argument("--times", type=int, default=1)
    parser.add_argument("--result_dir", default="results")

    return parser.parse_args()


args = get_args()    
setup_seed(args.seed)


class StableCox:
    def __init__(self, alpha=0.01, hidden_layer_sizes=(100, 5), W_clip=(0.1, 2)):
        """
        alpha: the regularization strength of l2 norm
        hidden_layer_sizes: the hidden dim of MLP of SRDO
        W_clip: the clip value for learned weights. It will reduce the variance.
        """
        self.alpha = alpha
        self.hidden_layer_sizes=hidden_layer_sizes
        self.W_clip = W_clip
    def fit(self, data, duration_col, event_col):
        """
        data:input data should be a dataframe, n*(d+2), n is the number of samples, d is the dimension of covariates (e.g., the number of genes)
        duration_col: the survival duration column name
        event_col: the survival event indicator column name
        """
        self.train = data
        self.duration_col = duration_col
        self.event_col = event_col
        covariate = np.array(data.drop([duration_col, event_col], axis=1))
        W = SRDO(covariate, hidden_layer_sizes = self.hidden_layer_sizes, decorrelation_type=args.decorrelation_type, max_iter=3000)
        
        mean_value = np.mean(W)
        W = W * (1/mean_value)

        W = np.clip(W, self.W_clip[0], self.W_clip[1])

        model_func = get_algorithm_class(args.backend)
        model = model_func(data, duration_col, event_col, W, self.alpha)
        self.model = model
        self.summary = model.summary
        return model

    def predict_with_topN(self, data, topN = 10):
        """
        data: has the same covariate of training data or only has the top N covariate
        topN: the number of biomarker selected
        """
        columns = data.columns
        test1_W = np.ones((data.shape[0], 1))
        X_test1_pd = np.concatenate((data, test1_W), axis=1)
        X_test1_pd = pd.DataFrame(X_test1_pd, columns=list(columns)+["Weights"])
        
        summary = self.model.summary
        sorted_indices = summary['p'].sort_values().head(topN).index
        print("top "+str(topN)+" biomarker:")
        print("\n".join([str(tmp) for tmp in list(sorted_indices)]))
        coef = summary.loc[list(sorted_indices)]["coef"]
        cols = [self.duration_col, self.event_col] + list(sorted_indices)
        selected_X_train = self.train[cols]
        cph2 = CoxPHFitter(penalizer=0.1)
        cph2.fit(selected_X_train, duration_col=self.duration_col, event_col=self.event_col)
        
        c_index_dict = []
        c_index = concordance_index(X_test1_pd[self.duration_col], -cph2.predict_partial_hazard(X_test1_pd), X_test1_pd[self.event_col])
        return c_index
        
    def predict(self, data):
        """
        data: has the same covariate of training data
        """
        columns = data.columns
        test1_W = np.ones((data.shape[0], 1))
        X_test1_pd = np.concatenate((data, test1_W), axis=1)
        X_test1_pd = pd.DataFrame(X_test1_pd, columns=list(columns)+["Weights"])
        c_index = concordance_index(X_test1_pd[self.duration_col], -self.model.predict_partial_hazard(X_test1_pd), X_test1_pd[self.event_col])
        return c_index
        

if __name__ == "__main__":

    """
    training_pd_data = pd.read_csv('./omics_data/HCC_cancer/train_median.csv', index_col=0)
    test1_pd_data = pd.read_csv('./omics_data/HCC_cancer/test1_median.csv', index_col=0)
    test2_pd_data = pd.read_csv('./omics_data/HCC_cancer/test2_median.csv', index_col=0)
    test3_pd_data = pd.read_csv('./omics_data/HCC_cancer/test3_median.csv', index_col=0)
    SC = StableCox(alpha=0.0005, hidden_layer_sizes = (98, 11), W_clip=(0.4, 4))
    duration_col = "Survival.months"
    event_col="Survival.status"
    SC.fit(training_pd_data, duration_col, event_col)
    cindex = SC.predict_with_topN(test1_pd_data, topN=10)
    print("cindex", cindex)
    """
    training_pd_data = pd.read_csv('./clinical_data/breast_cancer/breast_train_survival.csv', index_col=0)
    test1_pd_data = pd.read_csv('./clinical_data/breast_cancer/breast_test1_survival.csv', index_col=0)
    

    training_pd_data = training_pd_data.drop(['Recurr.months', 'Recurr.status', 'Cohort'], axis=1)
    test1_pd_data = test1_pd_data.drop(['Recurr.months', 'Recurr.status', 'Cohort'], axis=1)
     
    SC = StableCox(alpha=0.002, hidden_layer_sizes = (69, 15), W_clip=(0.02, 2))
    duration_col = "Survival.months"
    event_col="Survival.status"
    SC.fit(training_pd_data, duration_col, event_col)
    cindex = SC.predict(test1_pd_data)
   
    print(cindex)
 
