import copy
import numpy as np
import pandas as pd
import global_land_mask
import datetime
from pyproj import Transformer
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# PRIVATE GLOBAL VARIABLES

# List of month full names.
__months_full = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

# List of month short names.
__months_short = [ 
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
]

# Mapping of month short names to month numbers.
__month_nums = { 
    "jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, 
    "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12
}

# List of season names.
__seasons = ["summer", "autumn", "winter", "spring", 'fall']

# Columns in data sets fetched from TRY that contain important context
# information.
context_cols = ["DataName", "OriglName", "OrigUnitStr", "Comment"]

# PRIVATE FUNCTIONS

def __replace_month(date_str, is_form):
    '''
    Replaces the month in the given string.
    @parameter date_str: The string containing the month.
    @parameter is_form: Whether the replacement is being made in
                        a value_form. Else, this means the replacement
                        is being made in a value. So, if false, this function
                        will replace full month names with their short forms.
                        If true, month names (full/short) are replaced by "m".
    @return: String with the month replaced with "m" / month short name.
    '''
    if date_str == date_str and type(date_str) == str:
        for m in __months_full:
            replace_with = "m" if is_form else m[:3]
            date_str = date_str.replace(m, replace_with)
        if is_form:
            for m in __months_short: 
                date_str = date_str.replace(m, "m")
    return date_str

def __replace_season(date_str):
    '''
    Replaces the season name in the given string with "s".
    @parameter date_str: The string containing the month.
    @return: String with the season name replaced by "s".
    '''
    date_str = str.lower(date_str)
    for s in __seasons:  date_str = date_str.replace(s, "s")
    return date_str

def __convert_to_decimal_degrees(row):
    '''
    Given a latitude or longitude value, and its
    form, this function converts it into decimal degrees
    if it is not already in this format.
    Many forms like [@ @' @" n, @°@'@.@''n, @ @' n, @d @m n, 
    @°@'@.@''e, @ @' @" w, @ @´w, @ @' e, @.@° n, @.@° s, 
    @.@° e, @°@'n, @°@'s, @°@' e, @°@'e, @d  @m w]
    have at least degree and direction information with optional 
    minutes and seconds information. However, they are expressed 
    in various notations and so, should be parsed differently
    to extract degree, minutes, and seconds information
    from them and convert them into decimal degrees. Thus function
    handles this conversion of latitude longitude values into 
    decimal degrees with form specific parsing.
    @parameter row: Lat Lon data frame row.
    '''
    value = row.OrigValueStr
    if value == value: # Not NaN
        value = str(value)

        # UTM values will be processed later by the 
        # value_transformation_latlon(...) function.
        # So for now, return UTM related values, as is.
        if "utm" in value: 
            return value 

        form = row.value_form

        # Standard formats.
        if form in ["@", "-@", "@.@", "-@.@"]: 
            return float(value)
    
        # Non Standard formats.

        # Process form.
        form = form.replace("n", "D")
        form = form.replace("e", "D")
        form = form.replace("w", "D")
        form = form.replace("deg", "d ")
        form = form.replace('sec', "s ")
        form = form.replace("s", "D")
        form = form.replace("°", "d ")
        form = form.replace("''", "s ")
        form = form.replace("'", "m ")
        form = form.replace("´", "m ")
        form = form.replace('"', "s ")

        # Process value.
        value = value.replace("deg", "d")
        value = value.replace('sec', "s ")
        value = value.replace("°", "d ")
        value = value.replace("''", "s ")
        value = value.replace("'", "m ")
        value = value.replace("´", "m ")
        value = value.replace('"', "s ")

        # Proceed only if cardinal direction is available.
        if "D" in form:
            # Extract hemisphere, degrees, minutes, seconds.
            hemisphere = 1 # ["N", "E"]
            degrees = 0
            minutes = 0
            seconds = 0
            if str.upper(value[-1]) in ["S", "W"]: 
                hemisphere = -1
            value_split = [
                v.strip() for v in value.split(" ") 
                if v != " " and len(v.strip()) > 0
            ]
            for i in range(len(value_split)):
                v = value_split[i]
                if i == 0: # First value should always be degree.
                    v = v.replace("d", "")
                    if is_float(v):
                        degrees = float(v)
                    else: return np.nan
                else:
                    if "m" in v: # Value is minutes
                        v = v.replace("m", "")
                        if is_float(v):
                            minutes = float(v)
                    elif "s" in v:
                        v = v.replace("s", "")
                        if is_float(v):
                            minutes = float(v)
            decimal_degrees = hemisphere*(degrees+(minutes/60)+(seconds/3600))
            return decimal_degrees

    return np.nan

def __latlon_utm_to_decimal_degrees(data_latlon):
    '''
    Converts UTM values in "non_std" latitude and longitude
    data into decimal degrees wherever possible.
    @parameter data_latlon: Dictionary containing dataframes with
                            latitude and longitude data in the format
                            output by the get_data_latlon(...) function.
    NOTE: Values in the OrigUnitStr column should contain the unit in the standard
          form: "utm zone_[integer] hemisphere_[n/s]" wherever values are in the UTM
          format. Thus, ensure unit standardization was applied beforehand.
    @return: data_latlon with UTM "StdValue"s expressed in decimal degrees.
    '''
    # Extract and merge utm lat lon data into a single data frame.
    l = "latitude"
    utm_data = data_latlon["latitude"]["data"]["non_std"][
        data_latlon[
            "latitude"
        ]["data"][
            "non_std"
        ].OrigUnitStr.astype(str).str.lower().str.contains("utm")
    ][["ObservationID", "ObsDataID", "StdValue", "OrigUnitStr"]].merge(
        data_latlon["longitude"]["data"]["non_std"][
            data_latlon[
                "longitude"
            ]["data"][
                "non_std"
            ].OrigUnitStr.astype(str).str.lower().str.contains("utm")
        ][["ObservationID", "ObsDataID", "StdValue", "OrigUnitStr"]],
        how="inner", on=["ObservationID", "OrigUnitStr"], 
        suffixes=["_lat", "_lon"]
    ).drop_duplicates()

    # Extract utm zone and hemisphere information from standardized units.
    utm_data = utm_data.assign(
        zone = utm_data.OrigUnitStr.apply(
            lambda n: int(n.split()[1].replace("zone_", ""))
        ),
        hemisphere = utm_data.OrigUnitStr.apply(
            lambda n: n.split()[1].replace("hemisphere_", "")
        )
    )

    # Compute decimal degrees
    decdeg_latlon = utm_data.apply(
        lambda r: wgs84_m_utm_to_decimal_degrees(
            r.StdValue_lon, r.StdValue_lat, r.zone, r.hemisphere
        ), axis=1
    )
    utm_data = utm_data.assign(
        decdeg_lat = decdeg_latlon.iloc[:, 0],
        decdeg_lon = decdeg_latlon.iloc[:, 1]
    )
    utm_data = utm_data.dropna(subset=["decdeg_lat", "decdeg_lon"])

    # Add newly converted latitude and longitude
    # values to data_latlon in a new column "utm2dd".
    for l in ["latitude", "longitude"]:
        data_latlon[l]["data"]["non_std"] = data_latlon[l][
            "data"
        ]["non_std"].merge(
            utm_data[[
                f"ObsDataID_{l[:3]}",
                f"decdeg_{l[:3]}"
            ]].rename(columns = {
                f"ObsDataID_{l[:3]}": "ObsDataID",
                f"decdeg_{l[:3]}": "utm2dd"
            }), on = "ObsDataID", how = "left"
        )

        # Update main data frame values with UTM values
        # that have just been transformed into decimal degrees.
        data_latlon[l]["data"]["non_std"] = data_latlon[l][
            "data"
        ]["non_std"].assign(
            StdValue = data_latlon[l]["data"]["non_std"].apply(lambda r:
                r.utm2dd if r.utm2dd == r.utm2dd else r.StdValue
            , axis = 1),
            OrigUnitStr = data_latlon[l]["data"]["non_std"].apply(lambda r:
                "decimal degrees" if r.utm2dd == r.utm2dd else r.OrigUnitStr
            , axis = 1)
        )

        # Replace all remaining UTM values with NaN.
        data_temp = data_latlon[l]["data"]["non_std"]
        data_latlon[l]["data"]["non_std"] = data_temp.assign(
            StdValue = data_temp.apply(lambda r:
                np.nan if "utm" in str(r.OrigUnitStr).lower() else r.StdValue
            , axis = 1)
        )

    return data_latlon

def __latlon_nztm_to_decimal_degrees(data_latlon):
    '''
    Converts New Zealand Transverse Mercator (NZTM) values in 
    "non_std" latitude and longitude data into decimal degrees.
    @parameter data_latlon: Dictionary containing dataframes with
                            latitude and longitude data in the format
                            output by the get_data_latlon(...) function.
    NOTE: Values in the OrigUnitStr column should contain the unit in the standard
          form: "nztm" wherever values are in the NZTM format. 
          Thus, ensure unit standardization was applied beforehand.
    @return: data_latlon with NZTM "StdValue"s expressed in decimal degrees.
    '''
    # Extract and merge utm lat lon data into a single data frame.
    l = "latitude"
    nztm_data = data_latlon["latitude"]["data"]["non_std"][
        data_latlon[
            "latitude"
        ]["data"][
            "non_std"
        ].OrigUnitStr.astype(str).str.lower() == "nztm"
    ][["ObservationID", "ObsDataID", "StdValue", "OrigUnitStr"]].merge(
        data_latlon["longitude"]["data"]["non_std"][
            data_latlon[
                "longitude"
            ]["data"][
                "non_std"
            ].OrigUnitStr.astype(str).str.lower() == "nztm"
        ][["ObservationID", "ObsDataID", "StdValue", "OrigUnitStr"]],
        how="inner", on=["ObservationID", "OrigUnitStr"], 
        suffixes=["_lat", "_lon"]
    ).drop_duplicates()

    # Compute decimal degrees
    decdeg_latlon = nztm_data.apply(
        lambda r: nztm_to_decimal_degrees(r.StdValue_lon, r.StdValue_lat), axis=1
    )
    nztm_data = nztm_data.assign(
        decdeg_lat = decdeg_latlon.iloc[:, 0],
        decdeg_lon = decdeg_latlon.iloc[:, 1]
    )
    nztm_data = nztm_data.dropna(subset=["decdeg_lat", "decdeg_lon"])

    # Add newly converted latitude and longitude
    # values to data_latlon in a new column "utm2dd".
    for l in ["latitude", "longitude"]:
        data_latlon[l]["data"]["non_std"] = data_latlon[l][
            "data"
        ]["non_std"].merge(
            nztm_data[[
                f"ObsDataID_{l[:3]}",
                f"decdeg_{l[:3]}"
            ]].rename(columns = {
                f"ObsDataID_{l[:3]}": "ObsDataID",
                f"decdeg_{l[:3]}": "nztm2dd"
            }), on = "ObsDataID", how = "left"
        )

        # Update main data frame values with UTM values
        # that have just been transformed into decimal degrees.
        data_latlon[l]["data"]["non_std"] = data_latlon[l][
            "data"
        ]["non_std"].assign(
            StdValue = data_latlon[l]["data"]["non_std"].apply(lambda r:
                r.nztm2dd if r.nztm2dd == r.nztm2dd else r.StdValue
            , axis = 1),
            OrigUnitStr = data_latlon[l]["data"]["non_std"].apply(lambda r:
                "decimal degrees" if r.nztm2dd == r.nztm2dd else r.OrigUnitStr
            , axis = 1)
        )

        # Replace all remaining UTM values with NaN.
        data_temp = data_latlon[l]["data"]["non_std"]
        data_latlon[l]["data"]["non_std"] = data_temp.assign(
            StdValue = data_temp.apply(lambda r:
                np.nan if "nztm" in str(r.OrigUnitStr).lower() else r.StdValue
            , axis = 1)
        )

    return data_latlon

# PUBLIC FUNCTIONS

def agg_mean_mode(group):
    '''
    Aggregates trait values such that the "StdValue" with 
    greatest "priority" is selected if there is more than 
    one "StdValue" associated with each group. Also, if there is 
    more than one "StdValue" with the same "priority", mean shall
    be computed as long as all strings in the "StdValue" column 
    are numeric. If they are categorical instead, the mode 
    shall be computed.
    @parameter group: The group with possibly multiple StdValue values.
    @return: A single StdValue.
    '''
    # Get the rows with the greatest "priority".
    max_priority = group["priority"].max()
    max_priority_rows = group[group["priority"] == max_priority]
    try: # mean if numeric, and
        return max_priority_rows["StdValue"].astype(float).mean()
    except: # mode otherwise.
        return max_priority_rows["StdValue"].mode().iloc[0]

def agg_concat_str(group):
    '''
    Custom aggregation function that returns a single
    "StdValue" value when a group has more than one
    rows with "StdValue" values. The aggregation involves
    simply concatenating all strings such that all words 
    in the string are unique and each word is separated by 
    a " " in the resulting string that is returned.
    @parameter group: Group data frame with columns "StdValue"
                      and "priority".
    ''' 
    value = " ".join(set((" ".join([
        v.strip() for v in group.StdValue.astype(str).unique().tolist()
        if v != 'nan'
    ])).split()))
    return value if len(value) > 0 else np.nan

def avg_first_last_year(data_year):
    '''
    Computes average value of DataIDs corresponding to first and
    last years (4688, 4691).
    @parameter data_year: Dictionary with date date data frames.
    @return: Same dictionary but with first and last year data averaged.
    '''
    data_first_last_avg = data_year["data"][
        data_year["data"].DataID == 4688
    ][["ObservationID", "ObsDataID", "StdValue"]].rename(
        columns = {"StdValue": "first"}
    ).merge(
        data_year["data"][
            data_year["data"].DataID == 4691
        ][["ObservationID", "ObsDataID", "StdValue"]].rename(
            columns = {"StdValue": "last"}
        ), on = ["ObservationID"], how = "inner", 
        suffixes=["_first", "_last"]
    )
    data_first_last_avg = data_first_last_avg.assign(
        avg = data_first_last_avg[
            ["first", "last"]
        ].astype(float).mean(axis=1).astype(int).astype(str)
    )

    data_subset = data_year["data"][
        data_year["data"].DataID.isin([4688, 4691])
    ][["ObservationID", "ObsDataID", "StdValue"]].merge(
        data_first_last_avg[["ObservationID", "avg"]], 
        on="ObservationID", how="left"
    )

    data_year["data"].loc[
        data_year["data"].ObsDataID.isin(data_subset.ObsDataID)
        , "StdValue"
    ] = data_subset.avg.to_list()

    return data_year

def load_trait_table(path):
    '''
    Loads the trait table downloaded from TRY 
    and saved as a TSV file.
    @parameter path: Path to the trait table .tsv file.
    '''
    return pd.read_csv(path, sep="\t").drop(['Unnamed: 5'], axis=1)

def search_trait_table(trait_table_df, search_str_list, print_matches=True):
    ''' 
    Returns rows of the trait table containing
    the given search string. The search has the 
    following characteristics.
    - AND search w.r.t words in each search string.
    - OR search w.r.t search strings.
    For example, search_str_list = ["specific leaf area", "sla"]
    means that all traits containing either the entire substring
    "specific leaf area" comprised of 3 words (AND operation between
    words within quotes) or the word "sla" in its name, shall be
    returned as matches.
    @parameter trait_table_df: Trait table as pandas data frame.
    @parameter search_str_list: List of search strings.
    @parameter print_matches: Whether or not matches should be
                              printed.
    @return: Subsection of DF that matches search.
    '''
    trait_desc_list = [
        str.lower(trait) 
        for trait in trait_table_df.Trait
    ]
    trait_idx_list = set([])
    for i in range(len(trait_desc_list)):
        for search_str in search_str_list:
            all_words_present = True
            for word in search_str.split():
                all_words_present &= word in trait_desc_list[i]
            if all_words_present: trait_idx_list.add(i)
    trait_idx_list = list(trait_idx_list)
    trait_table_df_subset = trait_table_df.iloc[trait_idx_list, 0:2]
    if print_matches:
        for trait_id, trait_name in trait_table_df_subset.values:
            print(f"({trait_id}) - {trait_name}")
    return trait_table_df_subset

def is_float(s):
    '''
    Returns if this string is that of a float or not.
    @parameter s: String value.
    @return: Whether this is a float string.
    '''
    try: float(s)
    except: return False
    return True

def is_lat_lon_valid_terrestrial(lat, lon, antarctica_valid=False):
    '''
    Returns true if the given latitude and longitude
    values are both not NaN and are are valid floating
    point numbers on land.
    @parameter lat: Latitude in decimal degrees.
    @parameter lon: Longitude in decimal degrees.
    @parameter antarctica_valid: Whether or not to consider 
                                 points in antarctica valid.
    @return: True if all aforementioned conditions are met.
             False otherwise.
    '''
    # Invalid if NaN.
    if lat != lat or lon != lon: return False
    
    # Invalid if not a valid floating point number.
    if not (is_float(lat) and is_float(lon)): return False
    
    # Latitude must be in the range of -90 to 90 decimal degrees.
    # Longitude must be in the range of -180 to 180 decimal degrees.
    if lat < -90 or lat > 90 or lon < -180 or lon > 180: return False

    # Locations in Antarctica are invalid. 
    # There are no plants on Antarctica.
    # Antarctica is typically defined as the region south of 60°S latitude,
    # so any latitude less than -60 is considered Antarctic.
    if not antarctica_valid:
        if lat < -60: return False

    # Only other locations on land are considered valid.
    return global_land_mask.is_land(lat = lat, lon = lon)
     
def search_covariates(df, search_str_list, print_matches=True):
    ''' 
    Returns DataIDs of co-variates whose names are matched
    with the given search string. Search characteristics here
    are same as in the search_trait_table(...) function.
    @parameter df: Pandas data frame with data from TRY containing 
                   columns "DataID" and "DataName".
    @parameter search_str_list: List of search strings.
    @parameter print_matches: Whether or not matches are to be 
                              printed out (default = False).
    @return: List of DataIDs.
    '''
    df_subset = df[["DataID", "DataName"]].dropna().drop_duplicates()
    ids = set([])
    for data_id, data_name in df_subset.values:
        name = str.lower(data_name)
        for search_str in search_str_list:
            all_words_present = True
            for word in search_str.split():
                all_words_present &= word in name
            if all_words_present: ids.add(data_id)
    if print_matches:
        for data_id, data_name in df_subset[df_subset.DataID.isin(ids)].values:
            print(f"({data_id}) {data_name}")
    return list(ids)

def get_chunk_count(path, chunk_size):
    '''
    Returns no. of chunks that the data will be divided
    into if, chunk size for data loading is a certain value.
    @parameter path: Path to the data file.
    @parameter chunk_size: Chunk size (integer).
    @return: The no. of chunks.
    '''
    # Load downloaded data from TRY.
    num_chunks = 0
    for chunk in pd.read_csv(
        path, 
        delimiter = "\t", 
        encoding = "ISO-8859-1", 
        chunksize = chunk_size,
        low_memory = False
    ): num_chunks += 1
    return num_chunks

def load_big_data(
    path, drop_cols=[], 
    chunk_size=10000, chunk_idx = (-2, -1),
    clean=True, verbose=True
):
    '''
    Loads a large data file. This function sees to it that NaN
    values in the StdValue column are filled with values from the
    StdValueStr column so that all standardized values, if available,
    may be found in a single column "StdValue" instead of sometimes
    being present under column "StdValueStr" instead of "StdValue".
    @parameter path: Path to the large datafile.
    @parameter drop_cols: Columns to drop. Important columns for 
                          data exploration ["TraitID", "DataID", 
                          "DatasetID", "ObsDataID", "ObservationID", 
                          "AccSpeciesID", "StdValue", "StdValueStr", 
                          "UnitName", "OrigValueStr", "OrigUnitStr",
                          "OriglName", "Comment"] will not be dropped
                          on request.
    @parameter rename: If true (default), renames columns to 
                       more comprehensive and intuitive names.
    @parameter chunk_size: Data shall be loaded one chunk at a time to
                           minimize memory errors and kernel crashes. This
                           parameter defines the size of each data chunk.
    @parameter chunk_idx: A 2 element tuple wherein the first element is the
                          the index of the first data chunk to load and the
                          second element is the index of the last data chunk 
                          that is to be loaded. This parameter serves to allow
                          loading of only a portion of all data chunks when
                          the raw dataset is so large that it causes kernel
                          crashed even when loaded in chunks, if attempting
                          to load all the data in a single processing session.
                          By default, this parameter value is (1, 1). 
                          This indicates that all chunks are to be loaded. 
    @parameter clean: If true (default), performs the following 
                      two cleaning steps.
                      1. Drop duplicates.
                      2. Remove high risk error values. 
    @parameter verbose: Whether or not to print status comments.
    @return data: Data in given file as a pandas data frame.
    @return trait_id_list: List of all trait ids found in the 
                           loaded data set.
    '''
    # Load downloaded data from TRY.
    chunk_list = []

    i_start = chunk_idx[0]
    i_end = chunk_idx[1]
    step = 0 if i_start == -2 and i_end == -1 else 1
    i = -2 if step == 0 else 0
    for chunk in pd.read_csv(
        path, delimiter = "\t",
        encoding = "ISO-8859-1", 
        chunksize = chunk_size,
        low_memory = False
    ): 
        # Stop if ending chunk index is reached.
        if i == i_end: break
        # Consider only those chunks with the same index
        # as the start index or the index after the defined 
        # starting chunk index.
        if i >= i_start: chunk_list.append(chunk)
        i += step
    data = pd.concat(chunk_list, axis=0)

    # Optionally clean dataset.
    if clean:
        # Drop duplicates.
        # The TRY 6.0 data release notes states that if a row contains 
        # an integer for the OrigObsDataID column, then this integer 
        # refers to the original obs_id of the observation that this
        # row is a duplicate of. Such duplicate records exist because
        # multiple studies can upload same data. Thus, keeping only those
        # records for which obs_id_of_original is NaN is equivalent to
        # dropping all duplicate observations in the dataset.
        data = data[data.OrigObsDataID.isna()]
        data.drop(["OrigObsDataID"], axis=1, inplace=True)

        # Risk minimization.
        # Also in TRY 6.0 data release notes, it is suggested that 
        # all records with Error Risk > 4 be dropped. 
        # Thus, this is done here as well.
        data.drop(data[data.ErrorRisk > 4].index, inplace=True)
        data.drop(["ErrorRisk"], axis=1, inplace=True)

    # Drop less useful columns.
    drop_cols += [col for col in drop_cols if not col in 
        [ # Ensure key columns are still retained.
            "TraitID", "DataID", "DatasetID", "ObsDataID",
            "ObservationID", "AccSpeciesID",
            "StdValue", "StdValueStr", "UnitName",
            "OrigValueStr", "OrigUnitStr",
            "OriglName", "Comment"
        ]
    ] + ["Unnamed: 28"]
    data.drop(drop_cols, axis=1, inplace=True)

    # Fillna in StdValue column with value in StdValueStr column.
    data = data.assign(StdValue = data.StdValue.fillna(
        data.StdValueStr
    ))

    # Extract all unique trait ids in the the dataset.
    trait_id_list = data.TraitID.dropna().unique().astype(int).tolist()

    # Optionally print information about loaded data.
    if verbose:
        print(f"Loaded {len(data)} data points from '{path}'.")
        print("\nTraits Found:")
        for trait_id, trait_name in data[
            ["TraitID", "TraitName"]
        ].drop_duplicates().dropna().values:
            print(f"({int(trait_id)}) {trait_name}")

    return data, trait_id_list

def get_form(
    val, num_placeholder="@", rep_month=True, 
    rep_season=True, make_lower=True
):
    '''
    Replaces all number quantities in a mixed string 
    with a symbol while retaining non-numeric parts so 
    that the general form of the alphanumeric string is returned.
    @parameter val: Value, the form of which, is to be returned.
    @parameter num_placeholder: The symbol that will replace 
                                numbers (default = @).
    @parameter lower: Whether or not to make lowercase.
    @parameter rep_month: Whether or not to replace month names.
    @parameter rep_season: Whether or not to replace season names.
    @parameter make_lower: Whether or not to transform the form to be
                           in lowercase only.
    @return: General form of the given value.
    '''
    if val != val: return val # If value is NaN, return NaN.
    val_str = str(val) if type(val) != str else val
    val_form = ""
    is_num = False
    num_points = 0
    for i in range(len(val_str)):
        c = val_str[i]
        if c.isnumeric(): # character is a number
            if not is_num: # previous character was not a number
                is_num = True
                val_form += num_placeholder
        else: # character is not a number
            if (c == "."): # character is a point
                num_points += 1
            if not(
                c == 1 and # this is the first point encountered
                is_num and # since the previous character was a number
                i + 1 < len(val_str) and # there is a next character
                val_str[i+1].isnumeric() # such that is is also a number
            ):  # the above is not the case
                is_num = False
                num_points = 0
                val_form += c
    if rep_month: val_form = __replace_month(val_form, is_form=True)
    if rep_season: val_form = __replace_season(val_form)
    val_form = val_form.strip()
    if make_lower: val_form = val_form.lower()
    return val_form
    
def standardize_data(
    data, preprocessing_steps, 
    unit_std, value_form_std, value_trans
):
    '''
    Standardizes data column values in the given pandas data frame.
    @parameter data: Data dictionary containing one or more
                     pandas data frames in the format as output by
                     functions like "get_data_trait(...)", 
                     "get_data_latlon(...)", or "get_data_year(...)".
    @parameter preprocessing_steps: List of functions to apply to the
                                    data to preprocess it before applying
                                    other functions. All these functions should
                                    receive input and produce output in the same 
                                    format as parameter "data" here. If no
                                    preprocessing is to be performed, this
                                    parameter may be set to [].
    @parameter unit_std: Function that performs unit standardization.
                         The aim of unit standardization is to replace
                         invalid and ambiguous unit values with more 
                         appropriate values. This function should
                         receive input and produce output in the same 
                         format as parameter "data" here. This parameter 
                         may be set to None no unit standardization is to
                         be performed.
    @parameter value_form_std: Function that performs value form standardization.
                               The aim of value standardization is to replace 
                               values associated with invalid or ambiguous 
                               value forms, with better alternatives. This function
                               should receive input and produce output in the same 
                               format as parameter "data" here. This parameter 
                               may be set to None no value form standardization
                               is to be performed.
    @parameter value_trans: Function that performs value conversion and 
                            transforms the trait value expressed in the 
                            original unit, into its equivalent value in a
                            standard unit. The aim of this function is to 
                            ensure that all values are expressed in the same unit.
                            This function should receive input and produce 
                            output in the same format as parameter "data" here. 
                            This parameter may be set to None no value 
                            transformation is to be performed.
    @return: Data dictionary in the same format as received but with 
             units (OrigUnitStr or UnitName column values) or
             trait values (StdValue column) in component data frames,
             standardized.
    '''
    # Preprocess data frame.
    for prep_fun in preprocessing_steps:
        # Deep copying to prevent 
        # overwriting original data frame.
        data_copy = copy.deepcopy(data) 
        data = prep_fun(data_copy)

    # Unit form standardization.
    if type(unit_std) != type(None):
        data_copy = copy.deepcopy(data)
        data = unit_std(data_copy)

    # Value form standardization.
    if type(value_form_std) != type(None):
        data_copy = copy.deepcopy(data)
        data = value_form_std(data_copy)

    # Value conversion.
    if type(value_trans) != type(None):
        data_copy = copy.deepcopy(data)
        data = value_trans(data_copy)

    return data

def get_data_trait(
    data_raw, priority, verbose=True, 
    rep_month_trait=False,  rep_season_trait=False,
    rep_month_covariate=True, rep_season_covariate=True
):
    '''
    This function extracts rows associated with prioritized
    TraitIDs from the given data frame containing raw data
    from TRY. Extracted data is separated based on whether 
    the data corresponds to pre-standardized values in TRY 
    or not. This function also adds a new column to corresponding
    data frames called "value_form" containing strings representing
    the general form of trait values.
    @parameter data_raw: Pandas data frame with raw data from try.
    @parameter priority: List of priorities associated with each Trait ID.
                         with 1 = highest priority and higher numbers 
                         representing progressively lower priorities.
                         This value will be added to the table as a new
                         column called "priority". This value is so that it
                         may be used to settle conflicts when there is more 
                         than one value associated with each observation.
                         NOTE: Only those records corresponding to data ids 
                               for which priorities are defined, will be present 
                               in the final dataset.
    @parameter verbose: Whether or not to print possibly helpful
                        information about processed data.
    @parameter rep_month_trait: Whether to replace months in 
                                trait values with an "m".
    @parameter rep_month_covariate: Whether to replace months in the 
                                    covariate values with "m".
    @parameter rep_season_trait: Whether to replace seasons in 
                                 trait values with an "s".
    @parameter rep_season_covariate: Whether to replace seasons in the 
                                     covariate values with "s".
    @return data_trait: A dictionary with trait information
                        in the following form wherein all rows 
                        with no information, are excluded.
                        {
                            "std": A pandas data frame containing 
                                   pre-standardized trait values.,
                            "non_std": A pandas data frame containing 
                                       non-standardized trait values.
                        }
    @return data_covariate: A dictionary with covariate information
                            in the following form wherein all rows 
                            with no information, are excluded.
                            {
                                "std": A pandas data frame containing 
                                       pre-standardized covariate values,
                                "non_std": A pandas data frame containing 
                                           non-standardized covariate values.
                            }
    '''
    # No information => StdValueStr == NaN AND
    #                   StdValue == NaN AND
    #                   OrigValueStr == NaN.
    num_no_info = len(data_raw[np.logical_and(
        data_raw.StdValue.isna(), # Includes StdValueStr.isna() since NaN filled.
        data_raw.OrigValueStr.isna()
    )])

    # Separate trait data from covariate data.
    data_trait = data_raw[data_raw.TraitID.notna()] # Have TraitIDs and DataIDs.
    data_covariate = data_raw[data_raw.TraitID.isna()] # Have only DataIDs.

    # Only keep those traits that have a priority attached to it
    # and add a priority column.
    data_trait = data_trait[
        data_trait.TraitID.isin(priority.keys())
    ].merge(pd.DataFrame(
        priority.items(), columns=["TraitID", "priority"]
    ), on="TraitID", how="left")
    num_data_trait = len(data_trait)
    loaded_trait_ids = data_trait.TraitID.dropna().unique().tolist()
    
    # Only keep those covariate data rows
    # that are associated with selected 
    # trait related observations.
    data_covariate = data_covariate[
        data_covariate.ObservationID.isin(
            data_trait.ObservationID.dropna().unique().tolist()
        )
    ]
    num_data_covariate = len(data_covariate)

    # Separate trait and covarite data into standardized
    # and non-standardized data.
    # Standardized data => StdValue != NaN OR StdValueStr != NaN.
    # Non standardized data => StdValue == StdValueStr == NaN
    #                          AND OrigValueStr != NaN.
    data_trait = {
        "std": data_trait[data_trait.StdValue.notna()], 
        "non_std": data_trait[np.logical_and(
            data_trait.OrigValueStr.notna(),
            data_trait.StdValue.isna()
        )]
    }
    data_covariate = { 
        "std": data_covariate[data_covariate.StdValue.notna()],
        "non_std": data_covariate[np.logical_and(
            data_covariate.OrigValueStr.notna(),
            data_covariate.StdValue.isna()
        )]
    }
    
    # Add a value form column.
    data_trait["std"] = data_trait["std"].assign(
        value_form = data_trait["std"].StdValue.apply(
            lambda v: get_form(
                v, 
                rep_month = rep_month_trait, 
                rep_season = rep_season_trait
            )
        )
    )
    data_covariate["std"] = data_covariate["std"].assign(
        value_form = data_covariate["std"].StdValue.apply(
            lambda v: get_form(
                v, 
                rep_month = rep_month_covariate, 
                rep_season = rep_season_covariate
            )
        )
    )
    data_trait["non_std"] = data_trait["non_std"].assign(
        value_form = data_trait[
            "non_std"
        ].OrigValueStr.apply(
            lambda v: get_form(
                v, 
                rep_month = rep_month_trait, 
                rep_season = rep_season_trait
            )
        )
    )
    data_covariate["non_std"] = data_covariate["non_std"].assign(
        value_form = data_covariate[
            "non_std"
        ].OrigValueStr.apply(
            lambda v: get_form(
                v, 
                rep_month = rep_month_covariate, 
                rep_season = rep_season_covariate
            )
        )
    )

    # Optionally print separated data details.
    if verbose:
        num_total = len(data_raw)
        print(
            f"\nTotal no. of raw data points = ",
            f"{num_total} \n",
            f"\nNo. of trait data points = ",
            f"{num_data_trait}\n",
            f"No. of standardized trait data points = ",
            f"{len(data_trait["std"])}\n",
            f"No. of non standardized trait data points = ",
            f"{len(data_trait["non_std"])}\n",
            f"\nNo. of covariate data points = ",
            f"{num_data_covariate}\n",
            f"No. of standardized covariate data points = ",
            f"{len(data_covariate["std"])}\n",
            f"No. of non standardized covariate data points = ",
            f"{len(data_covariate["non_std"])}\n",
            f"\nNo. of data points with no information = {num_no_info}\n",
            f"\nLoaded TraitIDs: {loaded_trait_ids}", 
            sep=""
        )

    return data_trait, data_covariate

def display_units_forms(data, data_type="trait"):
    '''
    Displays some key information about pre-standardized
    and non-standardized values like their units and value format.
    This function is expected to be useful during manual
    investigation of data.
    @parameter data: Data dictionary as in the format returned by
                     functions get_data_trait(...), get_data_latlon(...),
                     or get_data_year(...).
    @parameter data_type: The type of data from which units and
                          forms are to be extracted. This may be 
                          "trait" for data in the format as returned 
                          by the get_data_trait(...) function. It may also be
                          "latlon" for data in the format as returned
                          by the get_data_latlon(...) function or "date" 
                          for data in the format as retuned by the 
                          get_data_year(...) function.
    '''
    if data_type == "trait":
        # View units.
        trait_std_units = data[
            "std"
        ].UnitName.dropna().drop_duplicates().values
        trait_non_std_units = data[
            "non_std"
        ].OrigUnitStr.dropna().drop_duplicates().tolist()
        print("Trait Standardised Units:", trait_std_units)
        print("Trait Non-Standardised Units:", trait_non_std_units)
        
        # View value forms.
        print(
            "Trait Standardised Value Forms:", 
            data["std"].value_form.unique().tolist()
        )
        print(
            "Trait Non-Standardised Value Forms:", 
            data["non_std"].value_form.unique().tolist()
        )

    if data_type == "date":
        # View units.
        print("Date Units:", data["data"].UnitName.unique().tolist())
        print( # View value forms.
            "Date Value Forms:", 
            data["data"].value_form.unique().tolist()
        )

    if data_type == "latlon":
        for l in ["latitude", "longitude"]:
            # View units.
            print(
                f"{'L'+l[1:]} Standardised Units:", 
                data[l]["data"]["std"].UnitName.unique().tolist()
            )
            print(
                f"{'L'+l[1:]} Non-Standardised Value Forms:", 
                data[l]["data"]["non_std"].OrigUnitStr.unique().tolist()
            )
            print(
                f"{'L'+l[1:]} Standardised Value Forms:", 
                data[l]["data"]["std"].value_form.unique().tolist()
            )
            print(
                f"{'L'+l[1:]} Non-Standardised Value Forms:", 
                data[l]["data"]["non_std"].value_form.unique().tolist()
            )

def get_vals_with_form(
    data, match_forms,
    keep_cols=[],
    value_form_col="value_form"
):
    '''
    Given a data frame with value form information, and 
    a list of value forms to search for, this function returns
    a subset of that dataframe with just the rows associated with
    value forms in the given match list.
    @parameter data: Data frame with value form information.
    @parameter value_form_col: Name of the column with value
                               form information 
                               (default = "value_form").
    @parameter keep_cols: List of columns to return. If all 
                          columns are to be returned, simply
                          set this to [] or do not set a value
                          for this parameter.
    @parameter match_forms: A list of value forms to match.
    @return: Data frame subset containing rows with 
             matching value forms.
    '''
    if len(keep_cols) > 0:
        return data[
            data[value_form_col].isin(match_forms)
        ][keep_cols].drop_duplicates()
    else:
        return data[
            data[value_form_col].isin(match_forms)
        ].drop_duplicates()

def get_data_latlon_ids(data_covariate):
    '''
    Prints standardized and non-standardized
    ids associated with latitude and longitude data.
    These IDs are also returned.
    @parameter data_covariate: Pre-standardized and non-standarized
                               covariate data as a dictionary in the
                               form {"std": ..., "non_std": ...}.
    @return data_latlon: Dictionary of the following form.
                         data_latlon = {
                            "latitude": {
                                "data_ids": {
                                    "std": [...], 
                                    "non_std": [...]
                                },
                                "data": None
                            },
                            "longitude": {
                                "data_ids": {
                                    "std": [...], 
                                    "non_std": [...]
                                },
                                "data": None
                            }
                         }
    '''
    data_latlon = {
        "latitude": {
            "data_ids": {"std": [], "non_std": []},
            "data": {"std": None, "non_std": None}
        }, 
        "longitude": {
            "data_ids": {"std": [], "non_std": []},
            "data": {"std": None, "non_std": None}
        },
    }

    print("\nAll Available Data: Standardized Lat Lon")
    data_latlon["latitude"]["data_ids"]["std"] = search_covariates(
        df = data_covariate["std"], 
        search_str_list = ["latitude"]
    )
    data_latlon["longitude"]["data_ids"]["std"] = search_covariates(
        df = data_covariate["std"], 
        search_str_list = ["longitude"]
    )

    print("\nAll Available Data: Non Standardized Lat Lon")
    data_latlon["latitude"]["data_ids"]["non_std"] = search_covariates(
        df = data_covariate["non_std"], 
        search_str_list = ["latitude"]
    )
    data_latlon["longitude"]["data_ids"]["non_std"] = search_covariates(
        df = data_covariate["non_std"], 
        search_str_list = ["longitude"]
    )

    return data_latlon

def get_data_latlon(data_latlon, data_covariate, verbose=True):
    '''
    Extracts pre-standardized and non-standardized latitude and
    longitude data from covariate data and returns this.
    @parameter data_latlon: Output of the function 
                            get_data_ids_latlon(...)
                            containing DataIDs corresponding to 
                            pre-standardized and standardized
                            latitude and longitude data, and space
                            for latitude and longitude related 
                            data frames respectively.
    @parameter data_covariate: A dictionary with both 
                               pre-standardized and standardized
                               covariate data of the form
                               {"std": ..., "non_std": ...}.
    @parameter verbose: Whether or not to print status details.
    @return: data_latlon with added latitude and longitude
             related data frames.
    '''
    # Load separated data.
    data_latlon["latitude"]["data"]["std"] = data_covariate["std"][
        data_covariate["std"].DataID.isin(
            data_latlon["latitude"]["data_ids"]["std"]
        )
    ]
    data_latlon["longitude"]["data"]["std"] = data_covariate["std"][
        data_covariate["std"].DataID.isin(
            data_latlon["longitude"]["data_ids"]["std"]
        )
    ]
    data_latlon["latitude"]["data"]["non_std"] = data_covariate["non_std"][
        data_covariate["non_std"].DataID.isin(
            data_latlon["latitude"]["data_ids"]["non_std"]
        )
    ]
    data_latlon["longitude"]["data"]["non_std"] = data_covariate["non_std"][
        data_covariate["non_std"].DataID.isin(
            data_latlon["longitude"]["data_ids"]["non_std"]
        )
    ]

    if verbose:
        loaded_data_ids = []
        for l in ["latitude", "longitude"]:
            for s in ["std", "non_std"]:
                loaded_data_ids += data_latlon[l][
                    "data"
                ][s].DataID.dropna().unique().tolist()
        loaded_data_ids = list(set(loaded_data_ids))
        print("\nDataIDs Loaded =", loaded_data_ids)

    return data_latlon

def value_transformation_trait(data_trait, get_std_value):
    '''
    Transforms all non standardized values to be expressed in
    an appropriate standard form.
    @parameter data_trait: Dictionary with trait data in 
                           constituent data frames. Form of this
                           dictionary shall be as returned by the 
                           get_data_trait(...) function.
    @parameter get_std_value: A function that, given a row from the
                              data_trait["non_std"] data frame,
                              returns a either a standard value
                              that is equivalent to the OrigStrValue
                              or NaN.
    @return: Same dictionary, but with standard values only.
    '''
    data_trait["non_std"] = data_trait["non_std"].assign(
        StdValue = data_trait["non_std"].apply(get_std_value, axis=1)
    )
    return data_trait

def value_transformation_latlon(
    data_latlon, handle_utm = True, handle_nztm = True,
    handle_special_cases = {"pre":[], "post":[]},
):
    '''
    Transforms all latitude and longitude values into their standard format.
    NOTE: All value_form and value strings must have a direction character 
          (n, e, w, s) and all 'n'/'N', 'e'/'E', 'w'/'W', and 's'/'S' characters 
          in these strings should refer to cardinal directions only.
    @parameter data_datlon: Latitude longitude data of the following form.
                            {
                                "latitude": {
                                    "data": {"std": ..., "non_std": ...},
                                    "data_ids: {"std}: ..., "non_std": ...}
                                },
                                "longitude": {
                                    "data": {"std": ..., "non_std": ...},
                                    "data_ids: {"std}: ..., "non_std": ...}
                                }
                            }
                            NOTE: It is important that the OrigUnitStr
                                  variable in the data frames within
                                  the input dictionary, be updated to
                                  contain information that can allow
                                  for extraction of UTM zone and
                                  hemisphere information through the 
                                  __latlon_utm_to_decimal_degrees(...) 
                                  function later, if UTM values are present.
                                  Similarly, the OrigUnitStr values associated
                                  with NZTM values should also be updated to 
                                  cater towards the function,
                                  __latlon_nztm_to_decimal_degrees(...).
    @parameter handle_utm: If true, converts any UTM data with UnitStrValue in format
                           "utm zone_[zone number] hemisphere_[n/s]"
                           into decimal degrees. Default = True.
    @parameter handle_nztm: If true, converts any NZTM data with UnitStrValue in format
                            "nztm" into decimal degrees. Default = True.
    @parameter handle_special_cases: Dictionary of the following 
                                     format containing a list of functions
                                     that may be applied before and/or after
                                     primary processing invovling converting
                                     given latitude and longitude value expression
                                     into decimal degrees.
                                     handle_special_cases = {
                                        "pre": [fun1, fun2, ...]/None,
                                        "post": [fun1, fun2, ...]/None 
                                    }
                                    These functions must accept a dictionary,
                                    data_latlon, with the same format as 
                                    returned by the get_data_latlon(...) function 
                                    as input such that the output has the same
                                    format as well, except that the values in the
                                    constitudent data frames could have been modified.
    @return: data_latlon with StdValue column updated with
             newly standardized data based on OrigValueStr values,
             all in decimal degrees. UnitValue field shall be 
             updated with "decimal degrees".
    '''
    data_latlon = copy.deepcopy(data_latlon)

    # Handle special cases.
    for f in handle_special_cases["pre"]:
        data_latlon = f(data_latlon)

    # Convert all values other than those with unit = utm.
    for l in ["latitude", "longitude"]:
        # Only non-standardized values need conversion.
        transformed_values = data_latlon[l]["data"][
            "non_std"
        ].apply(__convert_to_decimal_degrees, axis=1)
        data_latlon[l]["data"]["non_std"].loc[:, "StdValue"] = transformed_values

    # Convert UTM values into decimal degrees.
    if handle_utm:
        data_latlon = __latlon_utm_to_decimal_degrees(data_latlon)

    # Convert NZTM values into decimal degrees.
    if handle_nztm: 
        data_latlon = __latlon_nztm_to_decimal_degrees(data_latlon)

    # Keep only rows that have location data.
    for l in ["latitude", "longitude"]:
        for s in ["std", "non_std"]:
            data_latlon[l]["data"][s].dropna(
                subset=["StdValue"], inplace=True
            )

    # Handle special cases.
    for f in handle_special_cases["post"]:
        data_latlon = f(data_latlon)

    return data_latlon

def value_transformation_year(
    data_year, handle_special_cases = {"pre":[], "post":[]}
):
    '''
    Extracts years from dates.
    @parameter data_year: Dictionary containing data frames with
                          date information.
    @parameter handle_special_cases: Functions to be applied
                                     before and/or after year extraction.
                                     handle_special_cases = {
                                        "pre": [pre-processing functions],
                                        "post": [post-processing functions]
                                     }.
                                     NOTE: Both pre and post processing functions
                                           should receive data_year (in the same
                                           format as returned by 
                                           get_data_year(...)) and return the same
                                           dictionary with modification as output.
    @return: Same dictionary with years instead of entire dates.
    '''
    for f in handle_special_cases["pre"]:
        data_year = f(data_year)
    data_year["data"] = data_year["data"].assign(
        StdValue = data_year["data"].apply(
            lambda row: extract_year(row)
        , axis=1)
    )
    for f in handle_special_cases["post"]:
        data_year = f(data_year)
    return data_year

def get_data_year_ids(data_covariate):
    '''
    Prints standardized and non-standardized
    ids associated with date-time data. These IDs are also returned.
    @parameter data_covariate: Pre-standardized and non-standarized
                               covariate data as a dictionary in the
                               form {"std": ..., "non_std": ...}.
    @return data_year: Dictionary of the following form.
                       data_year = {
                            "data_ids": {
                                "std": [...], 
                                "non_std": [...]
                            },
                            "data": DataFrame
                       }
    '''
    data_year = {
        "data_ids": {"std": [], "non_std": []},
        "data": {"std": None, "non_std": None}
    }

    print("\nAll Available Data: Standardized Dates")
    data_year["data_ids"]["std"] = search_covariates(
        df = data_covariate["std"], 
        search_str_list = ["date"]
    )
    print("\nAll Available Data: Non-Standardized Dates")
    data_year["data_ids"]["non_std"] = search_covariates(
        df = data_covariate["non_std"], 
        search_str_list = ["date"]
    )

    return data_year

def get_data_year(data_year, data_covariate, verbose=True):
    """
    Extracts date related data amidst pre-standardized
    and standardized date related covariate data and 
    returns it, combined in one data frame because in
    TRY, date values are not explicitly standardized to 
    one common format.
    @parameter data_year: Dictionary output by the 
                          get_data_ids_year(...) function
                          of the following form.
                          data_year = {
                            "data_ids": {
                                "std": [...], 
                                "non_std": [...]
                            }, "data": {
                                "std": DataFrame,
                                "non_std": DataFrame
                            }
                          }
    @parameter data_covariate: Dictionary containing pre-standardized
                               and standardized covariate data.
    @parameter verbose: Whether or not to print status details.
    @return: Date-time related covariate data.
    """    
    data_year = copy.deepcopy(data_year)

    # Load separated data.
    data_year["data"]["std"] = data_covariate["std"][
        data_covariate["std"].DataID.isin(
            data_year["data_ids"]["std"]
        )
    ]
    data_year["data"]["non_std"] = data_covariate["non_std"][
        data_covariate["non_std"].DataID.isin(
            data_year["data_ids"]["non_std"]
        )
    ]

    # Merge std and non_std data.
    data_year["data"] = pd.concat([
        data_year["data"]["std"],
        data_year["data"]["non_std"]
    ])

    # Handle StdValue column
    std_value = data_year["data"].StdValue.fillna(
        data_year["data"].OrigValueStr
    )
    std_value = std_value.apply(
        lambda v: v if not isinstance(v, str) else v.lower()
    )

    # Handle UnitName column
    unit_name = data_year["data"].UnitName.astype(str)
    unit_name = unit_name.fillna(
        data_year["data"].OrigUnitStr.astype(str)
    )

    # Reassign columns explicitly
    data_year["data"] = data_year["data"].assign(
        StdValue = std_value,
        UnitName = unit_name
    )

    # Drop redundant columns.
    data_year["data"].drop([
        "OrigValueStr", "OrigUnitStr", "StdValueStr"
    ], axis=1, inplace=True)

    # Print data ids present.
    if verbose:
        print(
            "\nDataIDs Loaded =", 
            data_year["data"].DataID.drop_duplicates().tolist()
        )

    return data_year

def view_context(df, return_subset = False):
    '''
    Displays unique DataName, OriglName, OrigUnitStr, Comment combinations.
    @parameter df: Data frame with all aforementioned columns.
    @parameter context_cols: Option to define alternative context columns.
    @parameter return_subset: Whether or not to return the viewed 
                              data frame subset.
    '''
    df_subset = df[context_cols].drop_duplicates()
    display(df_subset)
    if return_subset: return df_subset

def combine_data(
    data_trait, data_latlon, data_year, 
    feature_name, feature_std_unit,
    trait_value_agg=None, drop_water_antarctica=True
):
    '''
    Given processed trait, geo-location, and year data,
    this function combines them into one dataframe.
    Following are the keys that the data dictionaries
    are expected to have. All data frames should have
    the standardized value in the StdValue column.

    NOTE: It is expected that data_trait, data_latlon, and
          data_year data frames contain the following columns.
          * data_trait: [
                "StdValue", "ObservationID", 
                "AccSpeciesID", "priority"
            ]
          * data_latlon: [
                "StdValue", "ObservationID"
          ]
          * data_year: [
                "StdValue", "ObservationID"
          ]

    @parameter data_trait: {"std": Dataframe, "non_std": Dataframe}
    @parameter data_latlon: {
        "latitide": {"data": {"std": Dataframe, "non_std": Dataframe}}, 
        "longitude": {"data": {"std": Dataframe, "non_std": Dataframe}} 
    }
    @parameter data_year: {"data": {"std": Dataframe, "non_std": Dataframe}}
    @parameter feature_name: Name of the feature of interest.
    @parameter feature_std_unit: The standardized unit of the
                                 feature in standard notation.
    @parameter trait_value_agg: Custom trait value aggregation function
                                for when there is more than one different
                                StdValue per year, latitude, longitude, AccSpeciesID
                                combination. This function must accept a "group"
                                data frame with columns "priority", and "StdValue" 
                                as input and return a single "StdValue" that 
                                represents the single reduced "StdValue"
                                for the entire group which may have more than one 
                                row's worth of data.
    @parameter drop_water_antarctica: Drop latitudes and longitudes that
                                      correspond to non-terrestrial locations
                                      and/or antarctica if True. Default = True.
    @return: Single data frame with all standardized values.
    '''
    # Combine standardized and non standardized trait data.
    data = pd.concat([
        data_trait["std"],
        data_trait["non_std"]
    ])

    # Add location data.
    data_lat = pd.concat([
        data_latlon["latitude"]["data"]["std"],
        data_latlon["latitude"]["data"]["non_std"]
    ]).rename(columns={
        "StdValue": "latitude" 
    })[["ObservationID", "latitude"]]
    data_lon = pd.concat([
        data_latlon["longitude"]["data"]["std"],
        data_latlon["longitude"]["data"]["non_std"]
    ]).rename(columns={
        "StdValue": "longitude"
    })[["ObservationID", "longitude"]]
    data_latlon = data_lat.merge(data_lon, on="ObservationID", how="inner")
    if drop_water_antarctica:
        data_latlon = data_latlon[ # Keep terrestrial & not antarctica points only.
            data_latlon[["latitude", "longitude"]].apply(
                lambda r: is_lat_lon_valid_terrestrial(r.latitude, r.longitude)
            , axis=1)
        ]
    data = data.merge(data_latlon, on="ObservationID", how="left")

    # Add date information.
    data = data.merge(
        data_year["data"][[
            "ObservationID", "StdValue"
        ]].rename(columns = {
            "StdValue": "year"
        }), 
        on = "ObservationID", how = "left"
    )[[
        "year", "latitude", "longitude", 
        "AccSpeciesID", "StdValue", "priority"
    ]]
    data = data.drop_duplicates()

    if type(trait_value_agg) == type(None):
        data = data[[
            "year", "latitude", "longitude", "AccSpeciesID", "StdValue"
        ]]
    else:
        # Reduce data so that there is one unique
        # feature value for every unique combination
        # of year + latitude + longitude + species.
        data = data.groupby([
            "year", "latitude", "longitude", "AccSpeciesID"
        ], dropna=False).apply(lambda group: pd.Series({
            "StdValue": trait_value_agg(group)
        }), include_groups=False).reset_index()
    
    # Rename column to be feature name.
    feature_column_name = feature_name
    if len(feature_std_unit) > 0:
        feature_column_name += "_" + feature_std_unit

    data = data.rename(columns = {
        "AccSpeciesID": "species_id",
        "StdValue": feature_column_name
    })

    # Only return values where the feature column 
    # and latitude/longitude are not nan.
    data = data.dropna(subset=[feature_column_name])
    
    return data

def extract_year(data_year_row, handle_special_cases=None):
    ''' 
    Given a date, returns the year from it in standard format.
    @parameter data_year_row: A row from the data_year dataframe
                              containing date related information.
                              This data frame is expected to have
                              columns [StdValue, value_form].
    @parameter handle_special_cases: Optional function that accepts 
                                     date_str, date_split, years, and 
                                     the dataframe row as inputs and 
                                     handles special cases
                                     to return a single year value alongwith
                                     a boolean value that indicates whether
                                     or not the special condition was met.
                                     This function should look as follows.
                                     def handle_special_cases(
                                        data_year_row, data_split, years, 
                                     ): 
                                        is_special_condition_met = ...
                                        to_return = ...
                                        return is_special_condition_met, to_return
    @return: Year if the date form is a single date or 
             mean year if it is a date range date range.
    '''
    current_year = datetime.date.today().year

    date_str = data_year_row.StdValue
    if date_str == date_str: # No NaN.
        if type(date_str) != str: # Make string, if not already so.
            date_str = str(date_str)

        date_str = date_str.replace("(", "")
        date_str = date_str.replace(")", "")
        date_str = date_str.replace(",", "-")
        date_str = date_str.replace("/", "-")
        date_str = date_str.replace("&", "-")
        date_str = date_str.replace(".", "-")
        date_str = date_str.replace("t", "-")
        date_str = date_str.replace("?", "")
        date_str = date_str.replace(" ", "-")

        date_split = date_str.split("-")

        years = np.sort([
            y.strip() for y in date_split 
            if y.strip().isnumeric() and len(y.strip()) == 4
        ]).tolist()

        # Special cases.
        if type(handle_special_cases) != type(None) :
            is_special_condition_met, to_return = handle_special_cases(
                data_year_row, date_split, years
            )
            if is_special_condition_met: return to_return
        
        # General case.
        if len(years) > 0:
            # For all other valid cases,
            # a year_start and year_end
            # can be obtained.
            year_start = int(years[0])
            year_end = int(years[-1])
            if (year_start <= current_year and year_end <= current_year):
                year_final = str(int(np.ceil((year_start+year_end)/2)))
                return year_final
            
    # Any other situation is invalid. 
    return np.nan 

def save_data(data, dest_fold, feature_name, feature_unit, suffix=""):
    '''
    Saves the given data frame at the given path as a 
    csv file.
    @parameter data: Pandas dataframe to save.
    @parameter dest_fold: Destination folder in which to save data.
    @parameter feature_name: Name of the feature that this dataset 
                             records values of, and has a column named
                             after.
    @parameter feature_unit: The standard unit of this feature.
    @parameter suffix: Some suffix to add to the file name after a "_".
    '''
    filename = feature_name
    if len(feature_unit) > 0: filename += "_" + feature_unit
    if len(suffix) > 0: filename += "_" + suffix
    data.to_csv(f"{dest_fold}/{filename}.csv", index=False)
    print(f'Saved "{filename}" data at "{dest_fold}/{filename}.csv".')

def wgs84_m_utm_to_decimal_degrees(easting, northing, zone, hemisphere):
    '''
    Converts X and Y values expressed in meters with the 
    coordinate reference system being UTM and  
    WGS84 reference datum to latitude and longitude values
    expressed in decimal degrees.
    @parameter easting: Longitude equivalent.
    @parameter northing: Latitude equivalent.
    @parameter zone: UTM Zone.
    @parameter hemisphere: Vertical geographic hemisphere (N/S).
    @return: Tuple of (latitude, longitude) in decimal degrees.
    '''
    latitude = np.nan
    longitude = np.nan
    if(
        easting == easting and 
        northing == northing and 
        zone == zone and 
        hemisphere == hemisphere
    ):
        # Build the UTM CRS string
        utm_crs = f"EPSG:326{zone}" if hemisphere == 'n' else f"EPSG:327{zone}"
        # Define the transformer (UTM to WGS84)
        transformer = Transformer.from_crs(utm_crs, "EPSG:4326", always_xy=True) 
        # Convert to decimal degrees (longitude, latitude)
        longitude, latitude = transformer.transform(easting, northing)
    return pd.Series([latitude, longitude])

def nztm_to_decimal_degrees(easting, northing):
    '''
    Converts New Zealand Transverse Mercator (NZTM) 
    coordinates to decimal degrees.
    @parameter easting: Longitude equivalent.
    @parameter northing: Latitude equivalent.
    @return latitude, longitude: Decimal degrees.
    '''
    latitude = np.nan
    longitude = np.nan
    if(
        easting == easting and 
        northing == northing
    ):
        # EPSG:2193 is NZTM, EPSG:4326 is WGS84 (decimal degrees)
        transformer = Transformer.from_crs("EPSG:2193", "EPSG:4326", always_xy=True)
        longitude, latitude = transformer.transform(easting, northing)
    return pd.Series([latitude, longitude])

def avg_min_max_latlon(data_latlon):
    '''
    For ObservationIDs with both min and max latitude/longitude
    values, the average value, replaces these. This function is expected
    to be used as a pre-processing step.
    @parameter data_latlon: Dictionary with latitude and longitude data.
    @return: Same data_latlon dictionary, but with avg. lat/lon value
             replacing min and max values.
    '''
    for l, min_num, max_num in [
        ("latitude", 4708, 4709),
        ("longitude", 4710, 4711)
    ]:
        # Calculate average.
        data_temp = data_latlon[l]["data"]["non_std"]
        df_min_max = data_temp[
            data_temp.DataID == min_num
        ][["ObservationID", "OrigValueStr"]].rename(
            columns = {"OrigValueStr": "min"}
        ).drop_duplicates().merge(
            data_temp[
                data_temp.DataID == max_num
            ][["ObservationID", "OrigValueStr"]].rename(
                columns = {"OrigValueStr": "max"}
            )
        , on = "ObservationID", how = "inner")
        df_min_max = df_min_max.assign(
            avg = df_min_max[["min", "max"]].astype(float).mean(axis=1)
        )
        # Update main data frame.
        data_temp = data_latlon[l]["data"]["non_std"]
        update_idx = data_temp[
            np.logical_and(
                data_temp.ObservationID.isin(df_min_max.ObservationID),
    	        data_temp.DataID.isin([min_num, max_num])
            )
        ].index.tolist()
        data_latlon[l]["data"]["non_std"].loc[
            update_idx, "OrigValueStr"
        ] = data_temp.loc[update_idx][
            ["ObservationID"]
        ].merge(df_min_max, on="ObservationID", how="left").avg

    return data_latlon

def get_utm_data(data_latlon, include_wgs=True):
    '''
    Returns those non_std rows of data where latitude/longitude
    is expressed in the UTM format.
    @parameter data_latlon: Dictionary with latitude and longitude data.
    @parameter include_wgs: Whether or not to also match rows with WGS data.
    @return: Matched data subset.
    '''
    data_latlon = copy.deepcopy(data_latlon)

    # Join non_std latitude and longitude data.
    data_latlon_non_std = pd.concat([
        data_latlon["latitude"]["data"]["non_std"], 
        data_latlon["longitude"]["data"]["non_std"]
    ]).drop_duplicates()

    # Extract UTM data.
    data_utm = data_latlon_non_std[
        np.logical_or(
            data_latlon_non_std.DataName.astype(
                str
            ).str.lower().str.contains("utm"),
            np.logical_or(
                data_latlon_non_std.OriglName.astype(
                    str
                ).str.lower().str.contains("utm"),
                data_latlon_non_std.Comment.astype(
                    str
                ).str.lower().str.contains("utm"),
            )
        )
    ]
    
    # Optionally extract WGS data.
    if include_wgs:
        data_wgs = data_latlon_non_std[
            np.logical_or(
                data_latlon_non_std.DataName.astype(
                    str
                ).str.lower().str.contains("wgs"),
                np.logical_or(
                    data_latlon_non_std.OriglName.astype(
                        str
                    ).str.lower().str.contains("wgs"),
                    data_latlon_non_std.Comment.astype(
                        str
                    ).str.lower().str.contains("wgs"),
                )
            )
        ]
        data_utm = pd.concat([data_utm, data_wgs]).drop_duplicates()

    return data_utm

def map_plot(data, save_path="", fig_size=(10, 10), title=""):
    '''
    Plots latitude and longitude columns of the given
    pandas dataframe on a map.
    @parameter data: Pandas dataframe containing columns
                     "latitude" and "longitude" with values in
                     decimal degrees.
    @parameter save_path: Saves the generated map to the given
                          location as a png image. By default,
                          the map is not saved as save_path = "".
    @parameter title: Map title. Default = "".
    @parameter fig_size: Size of the figure. Default = (10, 10).
    ''' 
    # Drop NaN latitude and longitude values.
    data = data.dropna(subset=["latitude", "longitude"])
    
    # Define figure and axes.
    fig, ax = plt.subplots(
        figsize=fig_size, 
        subplot_kw={'projection': ccrs.Mercator()}
    )

    data.loc[:, "latitude"] = data.latitude.astype(float)
    data.loc[:, "longitude"] = data.longitude.astype(float)

    # Plot the data.
    ax.scatter(
        data['longitude'], 
        data['latitude'], 
        color='green', 
        s=10, 
        transform=ccrs.PlateCarree()
    )

    # Add gridlines and features.
    ax.gridlines(draw_labels=True)
    ax.coastlines()

    # Optinally add a title.
    plt.title(title, fontsize=14)

    # Optionally save as png.
    if save_path != "": plt.savefig("static_map.png", dpi=300)
    
    # Display map.
    plt.show()