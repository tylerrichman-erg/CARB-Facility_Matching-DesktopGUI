import geopandas as gpd
import json
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from shapely.geometry import Point
import sqlite3

def standardize_table(
    df,
    CO_name,
    AB_name,
    DIS_name,
    FACID_name,
    FNAME_name,
    FSTREET_name,
    FCITY_name,
    FZIP_name,
    FSIC_name,
    FNAICS_name,
    LAT_name,
    LON_name
    ):

    df = df[["UID", CO_name, AB_name, DIS_name, FACID_name, FNAME_name, FSTREET_name, FCITY_name, FZIP_name, FSIC_name, FNAICS_name, LAT_name, LON_name]]

    col_rename_dict = {
        "UID" : "UID",
        CO_name: "CO",
        AB_name: "AB",
        DIS_name: "DIS",
        FACID_name: "FACID",
        FNAME_name: "FNAME",
        FSTREET_name: "FSTREET",
        FCITY_name: "FCITY",
        FZIP_name: "FZIP",
        FSIC_name: "FSIC",
        FNAICS_name: "FNAICS",
        LAT_name: "LAT_NAD83",
        LON_name: "LON_NAD83"
        }

    df = df.rename(columns=col_rename_dict)
    #df.rename(columns=col_rename_dict, inplace=True)

    dtype_mapping = {
        "UID": int,
        "CO": str, 
        "AB": str, 
        "DIS": str,
        "FACID": str,
        "FNAME": str, 
        "FSTREET": str, 
        "FCITY": str,
        "FZIP": str,
        "FSIC": str, 
        "FNAICS": str,
        "LAT_NAD83": float,
        "LON_NAD83": float
    }

    df = df.astype(dtype_mapping)
    df["FSIC"] = df["FSIC"].replace(r'\.0$', '', regex=True)
    df["FNAICS"] = df["FNAICS"].replace(r'\.0$', '', regex=True)

    return df

def load_parcel_dataset(pqt_folder_path):

    parcel_prq = pq.read_table(pqt_folder_path)
    parcel_df = parcel_prq.to_pandas()
    parcel_df = parcel_df.drop_duplicates()
    parcel_df["Parcel_UID"] = parcel_df.index
    parcel_gdf = gpd.GeoDataFrame(
        parcel_df,
        geometry=gpd.GeoSeries.from_wkt(parcel_df['Shape@WKT']),
        crs='EPSG:4269'
    )
    
    return parcel_gdf

def run_spatial_join(df, parcel_gdf):

    geometry = [Point(xy) for xy in zip(df['LON_NAD83'], df['LAT_NAD83'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4269')

    df = gpd.sjoin(gdf, parcel_gdf, how="left", predicate="within")\
        .drop(columns=["geometry", "index_right", "Shape@WKT"])

    df = df.sort_values(by=['Parcel_UID', 'AREA_M2'], ascending=[True, False])\
        .groupby('UID')\
        .head(1)

    df = df.drop(['OBJECTID', 'PARCEL_APN', 'Shape_Length', 'Shape_Area'], axis=1)

    return df

def standardize(col, standardization_dict, special_characters_list):

    ## Replace "-", "@", and "%" ##
    col = col.str.replace('-', ' ')
    col = col.str.replace('@', ' AT ')
    col = col.str.replace('%', ' PERCENT ')

    ## Remove special characters ##
    for special_character in special_characters_list:
        col = col.str.replace(special_character, '')

    ## Convert characters to UPPER ##
    col = col.str.upper()

    ## Remove excess spaces between words ##
    col = col.str.replace(r'\s+', ' ', regex=True)

    ## Add one leading and trailing space ##
    col = ' ' + col + ' '

    ## Perform word replacement ##
    for str_val in standardization_dict.keys():
        col = col.str.replace(str_val, standardization_dict[str_val])

    ## Remove leading and trailing spaces ##
    col = col.str.strip()

    return col

def standardize_text_fields(df, logic_path):
    standardization_df = pd.read_csv(logic_path)\
        .fillna("")\
        .set_index('input', inplace=False)

    special_characters_list = ['!', '"', '#', '$', '&', "'", '(', ')', 
                           '*', '+', ',', '.', '/', ':', ';', '<', 
                           '=', '>', '?', '[', '\\', ']', '^', '_', 
                           '`', '{', '|', '}', '~'] # '-', '@', '%'

    standardization_dict = standardization_df.to_dict(orient='dict')['standardized']
    standardization_dict = {f' {key} ': f' {value} ' for key, value in standardization_dict.items()}

    df["FNAME_STANDARDIZED"] = standardize(df["FNAME"], standardization_dict, special_characters_list)
    df["FSTREET_STANDARDIZED"] = standardize(df["FSTREET"], standardization_dict, special_characters_list)

    return df

def read_in_master_table(
        db_loc,
        table_name,
        ARBID_name,
        CO_name,
        AB_name,
        DIS_name,
        FACID_name,
        FNAME_name,
        FSTREET_name,
        FCITY_name,
        FZIP_name,
        FSIC_name,
        FNAICS_name,
        LAT_name,
        LON_name,
        PARCEL_name
        ):

    conn = sqlite3.connect(db_loc)

    df_master = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    conn.close()

    col_rename_dict = {
        ARBID_name: "ARBID",
        CO_name: "CO",
        AB_name: "AB",
        DIS_name: "DIS",
        FACID_name: "FACID",
        FNAME_name: "FNAME_STANDARDIZED",
        FSTREET_name: "FSTREET_STANDARDIZED",
        FCITY_name: "FCITY",
        FZIP_name: "FZIP",
        FSIC_name: "FSIC",
        FNAICS_name: "FNAICS",
        LAT_name: "LATITUDE_ROUND_5",
        LON_name: "LONGITUDE_ROUND_5",
        PARCEL_name: "Parcel_UID"
        }

    df_master.rename(columns=col_rename_dict, inplace=True)
    df_master = df_master[["ARBID", "CO", "AB", "DIS", "FACID", "FNAME_STANDARDIZED", "FSTREET_STANDARDIZED", "FCITY", "FZIP", "FSIC", "FNAICS", "LATITUDE_ROUND_5", "LONGITUDE_ROUND_5", "Parcel_UID"]]

    dtype_mapping = {
        "ARBID": int,
        "CO": str, 
        "AB": str, 
        "DIS": str,
        "FACID": str,
        "FNAME_STANDARDIZED": str, 
        "FSTREET_STANDARDIZED": str, 
        "FCITY": str,
        "FZIP": str,
        "FSIC": str, 
        "FNAICS": str,
        "LATITUDE_ROUND_5": float,
        "LONGITUDE_ROUND_5": float,
        "Parcel_UID": float
    }

    df_master = df_master.astype(dtype_mapping)
    df_master["FSIC"] = df_master["FSIC"].replace(r'\.0$', '', regex=True)
    df_master["FNAICS"] = df_master["FNAICS"].replace(r'\.0$', '', regex=True)

    return df_master

def drop_y_cols(df):
    
    columns_to_drop = [col for col in df.columns if col.endswith("_y")]
    df = df.drop(columns=columns_to_drop, axis=1)
    
    return df

def rename_x_cols(df):
    
    df.columns = [col[:-2] if col.endswith("_x") else col for col in df.columns]
    
    return df

def algorithm(df, matching_df, match_score, match_cols):

    matching_df["Score_To_Assign"] = match_score
    df = pd.merge(
        df,
        matching_df,
        on=match_cols,
        how='left'
    )

    df.loc[df["ARBID"].notna() & df["Match_ARBID"].isna(), "Match_ARBID"] = df["ARBID"]

    df.loc[df["Score_To_Assign"].notna() & df["Match_Score"].isna(), "Match_Score"] = df["Score_To_Assign"]
    df = drop_y_cols(df)
    df = df.drop('Score_To_Assign', axis = 1)
    df = rename_x_cols(df)

    df = df.drop(["ARBID"], axis=1)

    df = df.drop_duplicates()

    return df

def execute_matching_algorithm(df, df_master, match_scores_fields_path):

    with open(match_scores_fields_path, 'r') as json_file:
        match_fields_dict = json.load(json_file)

    first_run = True

    df["Match_ARBID"] = np.nan
    df["Match_Score"] = np.nan

    for match_score in match_fields_dict.keys():

        df = algorithm(
                df = df, 
                matching_df = df_master, 
                match_score = int(match_score), 
                match_cols = match_fields_dict[match_score]
            )
        
        """
        for match_cols in match_fields_dict[match_score]:
            df = algorithm(
                df = df, 
                matching_df = df_master, 
                match_score = match_score, 
                match_cols = match_cols
            )
        """
        """
        if first_run is True:
            df_matched = df_new_match
            first_run = False

        else:
            df_matched = pd.concat([df_matched, df_new_match], ignore_index=True)
        """

        df_matched = df

    return df_matched

def create_final_table(df, df_standardized, df_matched, df_scores_criteria, df_master):

    #print(df.columns)
    #print(df_standardized.columns)

    df_standardized.drop(columns=["Match_ARBID", "Match_Score"], inplace=True)

    for column in df_standardized.columns:
        if column != 'UID':
            df_standardized.rename(columns={column: column + '_standardizedCol'}, inplace=True)

    df_final = pd.merge(
        df,
        df_standardized,
        on='UID',
        how='left'
    )

    df_final = pd.merge(
        df_final,
        df_matched[["UID", "Match_ARBID", "Match_Score"]],
        on='UID',
        how='outer'
    )

    for column in df_scores_criteria.columns:
        if column not in ["UID", "Match_Score", "Match_ARBID"]:
            df_scores_criteria.rename(columns={column: column + '_matchCriteria'}, inplace=True)

    df_final = pd.merge(
        df_final,
        df_scores_criteria,
        on='Match_Score',
        how='left'
    )

    df_master.drop(columns=["Score_To_Assign"], inplace=True)
    df_master.rename(columns={"ARBID": "Match_ARBID"}, inplace=True)

    for column in df_master.columns:
        if column not in ["Match_ARBID"]:
            df_master.rename(columns={column: column + '_matchRecord'}, inplace=True)

    df_final = pd.merge(
        df_final,
        df_master,
        on='Match_ARBID',
        how='left'
    )

    return df_final
