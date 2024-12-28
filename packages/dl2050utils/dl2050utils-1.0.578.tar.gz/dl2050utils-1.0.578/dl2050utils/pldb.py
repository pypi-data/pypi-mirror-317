#
# pldb.py
#

from dl2050utils.common import listify
from dl2050utils.dbutils import parse_filters

# ####################################################################################################
# df_filter
# ####################################################################################################

def df_filter(df, filters, sfilters=None):
    """
    Filters a Polars DataFrame based on a filters structure.
        - df: Polars DataFrame to filter.
        - filters: A list of filter dictionaries or a dictionary of filters.
    Return the filtered DataFrame.
    """
    # Check inputs
    if filters is None and sfilters is None: return df
    filters,sfilters = listify(filters),listify(sfilters)
    # Parse filters
    filters = parse_filters(filters)
    sfilters = parse_filters(sfilters)
    # If no valid filters, return the original DataFrame
    if not filters and not sfilters: return df
    # Build the filter expression
    filter_expressions = []
    for f in filters:
        col, val, op = f['col'], f['val'], f['op']
        # Handle operations
        if op == '=': filter_expressions.append(df[col] == val)
        elif op == '!=': filter_expressions.append(df[col] != val)
        elif op == '>': filter_expressions.append(df[col] > val)
        elif op == '>=': filter_expressions.append(df[col] >= val)
        elif op == '<': filter_expressions.append(df[col] < val)
        elif op == '<=': filter_expressions.append(df[col] <= val)
        elif op == 'IN': filter_expressions.append(df[col].is_in(val))
        elif op == 'NOT_IN': filter_expressions.append(~df[col].is_in(val))
        elif op == 'IS':
            if val == 'NOT NULL':
                filter_expressions.append(df[col].is_not_null())
            else:  # Assume `val == 'NULL'`
                filter_expressions.append(df[col].is_null())
    # Handle string containment filters
    if sfilters:
        for sf in sfilters:
            col, val = sf['col'], sf['val']
            if isinstance(val, str):
                words = val.split()
                # Create AND condition for all words
                word_expressions = [df[col].str.contains(word, literal=False) for word in words]
                word_filter = word_expressions[0]
                for expr in word_expressions[1:]:
                    word_filter &= expr
                filter_expressions.append(word_filter)
    # Combine all filter expressions
    if filter_expressions:
        combined_filter = filter_expressions[0]
        for expr in filter_expressions[1:]:
            combined_filter &= expr
        return df.filter(combined_filter)
    # Return the original DataFrame if no filters applied
    return df

# #########################################################################################################################
# df_filter
# #########################################################################################################################

def get_tbl(df, cols=None, filters=None, sfilters=None, sort=None, ascending=True, offset=None, limit=None, excel=False):
    """
    Processes a Polars DataFrame by applying filters, sorting, column selection, and pagination, 
    and prepares the result as a dictionary suitable for JSON serialization with orjson.
    Parameters:
    - df (pl.DataFrame): The DataFrame to process. Returns an empty result if None.
    - cols (list, optional): Subset of column names to include in the result. Defaults to all columns.
    - filters (list/dict, optional): Filters to apply (e.g., `=`, `!=`, `>`, `<`, `IN`).
    - sfilters (list/dict, optional): String filters matching all words in the specified columns.
    - sort (str, optional): Column name to sort the DataFrame by.
    - ascending (bool, default=True): Whether to sort in ascending order (False for descending).
    - offset (int, optional): Starting index for row slicing. Defaults to 0.
    - limit (int, default=64): Maximum number of rows to include in the result.
    - one (bool, optional): Unused, placeholder for returning single-row results.
    - excel (bool, optional): Used for exporting to Excel, returns the filtered dataframe for conversion.
    - join (str, optional): Unused, placeholder for joining tables.
    - lookups (dict, optional): Unused, placeholder for enriching data with lookups.
    Returns:
    dict: {
        'data': List of dictionaries (rows in the DataFrame),
        'nrows': Total rows in the filtered DataFrame before slicing,
        'cols': List of included column names.
    }
    """
    if df is None: return {'data':[]}
    df = df_filter(df, filters, sfilters)
    if df is None: return {'data':[]}
    if sort and sort in df.columns: df = df.sort(sort, descending=not ascending)
    cols = [e for e in cols if e in df.columns] if cols else df.columns
    df = df.select(cols)
    if excel: df
    nrows = len(df)
    offset,limit = 0 if offset is None else int(offset),64 if limit is None else int(limit)
    df = df[offset:offset+limit]
    rows = df.to_dicts()
    return {'data':rows, 'nrows':nrows, 'cols':cols}
