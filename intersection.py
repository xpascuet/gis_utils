import geopandas as gpd

file1 = r"D:\Documents\Gencat\SIGPAC\2022\comunals\fo_gene\forests_shp\Forests.shp"
file2 = r"D:\Documents\Gencat\SIGPAC\2021\comunals\comunals_21.shp"


def intersection(file1, file2, result_file, col_to_keep1='all', col_to_keep2='all'):
    """
    
    Parameters
    ----------
    file1 : string
        DESCRIPTION.
    file2 : string
        DESCRIPTION.
    result_file : TYPE
        DESCRIPTION.
    col_to_keep1 : list of strings, optional
        List of the columns(fields) wanted to keep from file 1. The default is 'all'.
    col_to_keep2 : list of strings, optional
        List of the columns(fields) wanted to keep from file 2. The default is 'all'.

    Returns
    -------
    None.

    """
    intersect = []
    file1_df = gpd.read_file(file1)
    file2_df = gpd.read_file(file2)
    # Set same crs for both dataframes
    if file1_df.crs != file2_df.crs:
        file2_df.to_crs(file1_df.crs)
    # Set columns to keep from dataframe1
    if col_to_keep1 == 'all':
        cols1 = file1_df.columns.drop('geometry')
    else:
        cols1 = col_to_keep1
    # Set columns to keep from dataframe2
    if col_to_keep2 == 'all':
        cols2o = file2_df.columns.drop('geometry')
    else:
        cols2o = col_to_keep2
    # Rename cols from df2 if exists in df1
    cols2 = []
    for col in cols2o:
        while col in cols1:
            col = col + "_2"
        cols2.append(col)
    #cols2 = [col if col not in cols1 else (col + "_2") for col in cols2o]
    # Intersection
    for i1, r1 in file1_df.iterrows():
        if r1["geometry"].is_valid:
            for i2, r2 in file2_df.iterrows():
                if r2["geometry"].is_valid and r1["geometry"].intersects(r2["geometry"]):
                    intersect.append({**{"geometry": r1["geometry"].intersection(r2["geometry"])},
                                      **{i: r1[i] for i in cols1}, **{i: r2[z] for i, z in zip(cols2, cols2o)},
                                      **{"area": r1["geometry"].intersection(r2["geometry"]).area}})

    intersect_df = gpd.GeoDataFrame(intersect)
    intersect_df.to_file(result_file, driver='GeoJSON')


intersection(file1, file2, "result.geojson")
