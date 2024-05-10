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

    """
    This function standardizes the input table into a format that is compatible
    with the remaining processing steps for facility matching. This function
    inputs a data frame of the input table as well as column names specified in
    the GUI. It renames the columns to the names specified in col_rename_dict.
    It then sets the data type of each column of the data frame. Finally it
    removes any decimals places that may have accedentally been added to the
    FSIC and FNAICS columns.
    """

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

    """
    This function loads the parcel dataset in to a data frame before getting
    converted into a GeoPandas data frame referenced to EPSG:4269.
    """

    parcel_prq = pq.read_table(pqt_folder_path)
    parcel_df = parcel_prq.to_pandas()
    #parcel_df = parcel_df.drop_duplicates()
    #parcel_df["Parcel_UID"] = parcel_df.index
    parcel_gdf = gpd.GeoDataFrame(
        parcel_df,
        geometry=gpd.GeoSeries.from_wkt(parcel_df['Shape@WKT']),
        crs='EPSG:4269'
    )
    
    return parcel_gdf

def run_spatial_join(df, parcel_gdf):

    """
    This function inputs a facilities data frame as well as parcel GeoPandas
    data frame. The facilities data frame is converted into a GeoPandas data
    frame and spatial joined with the parcel GeoPandas data frame. Because
    overlapping parcels have been found during beta testing, only the largest
    parcel per facility is extracted. Ties go to the parcel with the lowest
    Parcel_UID. Unneeded columns are droped from the joined data frame. This
    function is used for both the input facilities table and Golden Master
    table.
    """

    geometry = [Point(xy) for xy in zip(df['LON_NAD83'], df['LAT_NAD83'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4269')

    df = gpd.sjoin(gdf, parcel_gdf, how="left", predicate="within")\
        .drop(columns=["geometry", "index_right", "Shape@WKT"])

    df = df.sort_values(by=['Parcel_UID', 'AREA_M2'], ascending=[True, False])\
        .groupby('UID')\
        .head(1)

    df = df.drop(['OBJECTID', 'Shape_Length', 'Shape_Area'], axis=1)

    return df

def standardize(col, standardization_dict, special_characters_list):

    """
    This function inputs a data frame column, dictionary of whole words to
    convert, and a list of special characters. The code performs string
    replacements on the data frame column for '-', '@', '%' as these are special
    characters that have word replacements. The code then removes spacial
    characters in the data frame column. It converts the column to UPPERCASE. It
    then removes excess spaces between words as well as add a leading and trailing
    space to the entire string. This is to distinguish whole words for word
    replacement. It then performs the word replacement before removing leading
    and trailing spaces.
    """

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

    """
    This function input the location of the database containing the Golden
    Master table as well as values from the config.ini file specifying the field
    names used within the database. The code uses SQLITE3 to connect to the
    database. Pandas is then used to read in the entire table from the database
    in a data frame. The columns are then renamed to be compatible with the
    rest of the code. It then sets the data type of each column of the data frame. Finally it
    removes any decimals places that may have accedentally been added to the
    FSIC and FNAICS columns.
    """

    conn = sqlite3.connect(db_loc)
    df_master = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()

    col_rename_dict = {
        ARBID_name: "ARBID",
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

    df_master.rename(columns=col_rename_dict, inplace=True)
    df_master = df_master[["ARBID", "CO", "AB", "DIS", "FACID", "FNAME", "FSTREET", "FCITY", "FZIP", "FSIC", "FNAICS", "LAT_NAD83", "LON_NAD83"]]

    dtype_mapping = {
        "ARBID": int,
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

    df_master = df_master.astype(dtype_mapping)
    df_master["FSIC"] = df_master["FSIC"].replace(r'\.0$', '', regex=True)
    df_master["FNAICS"] = df_master["FNAICS"].replace(r'\.0$', '', regex=True)

    return df_master

def drop_y_cols(df):

    """
    This function is used within algorithm() to drop columns in the tabular join
    that end with "_y".
    """
    
    columns_to_drop = [col for col in df.columns if col.endswith("_y")]
    df = df.drop(columns=columns_to_drop, axis=1)
    
    return df

def rename_x_cols(df):

    """
    This function is used within algorithm() to remove "_x" within columns after
    the tabular join.
    """
    
    df.columns = [col[:-2] if col.endswith("_x") else col for col in df.columns]
    
    return df

def algorithm(df, matching_df, match_score, match_cols):

    """
    This function matches the input facility table to the Golden Master table on
    columns associated with the match score. It adds values to the Match_ARBID
    and Match_Score columns of the input facility table if a match occurs. It is
    included within execure_match_algorithm.
    """

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

    for match_col in match_cols:
        if df[match_col].dtype == "float64":
            df.loc[(df["Match_Score"] == match_score) & (df[match_col].isna()), "Match_ARBID"] = np.nan
            df.loc[(df["Match_Score"] == match_score) & (df[match_col].isna()), "Match_Score"] = np.nan
        elif df[match_col].dtype == "object":
            df.loc[(df["Match_Score"] == match_score) & (df[match_col].isin(["", "nan"])), "Match_ARBID"] = np.nan
            df.loc[(df["Match_Score"] == match_score) & (df[match_col].isin(["", "nan"])), "Match_Score"] = np.nan

    return df

def execute_matching_algorithm(df, df_master, match_scores_fields_path):
    """
    This function creates the Match_ARBID and Match_Score columns within the
    input facilities table. It also loops through the match scores within
    logic.json and performs the match within algorithm() on the columns
    specified within the JSON.
    """

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

        df_matched = df

    return df_matched

def create_final_table(df, df_standardized, df_matched, df_scores_criteria, df_master):

    """
    This function creates the final table.
    """

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
    df_master.drop(columns=["UID"], inplace=True)

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
