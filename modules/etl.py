import numpy as np
import pandas as pd


def isolate_num_cols(df):
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    isolated_num_df = df[numeric_columns]
    return isolated_num_df

def normalize_num_vals(isolated_num_df , num_cols:list):
    normalized_df = isolated_num_df[[num_cols]] / isolated_num_df[[num_cols]].max()
    return normalized_df

