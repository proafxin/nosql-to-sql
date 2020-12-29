from pandas import (
    json_normalize,
    merge,
    DataFrame,
)

HAS_SUBFIELD_LIST = 1
HAS_SUBFIELD_DICT = 2
HAS_NO_SUBFIELD = 3
HAS_NO_SUBFIELD_BUT_ITERABLE = 4
need_flattening = [
    HAS_SUBFIELD_DICT,
    HAS_SUBFIELD_LIST,
]


def check_subfield(X):
    if isinstance(X, dict):
        return HAS_SUBFIELD_DICT
    if isinstance(X, list):
        if len(X) < 1:
            return HAS_NO_SUBFIELD
        if isinstance(X[0], dict):
            return HAS_SUBFIELD_LIST
        return HAS_NO_SUBFIELD_BUT_ITERABLE
    return HAS_NO_SUBFIELD

def has_subfield(X):
    status = check_subfield(X)
    return status in [HAS_SUBFIELD_LIST, HAS_SUBFIELD_DICT]

def get_types(df, check_rows=100):
    types = {}
    rows = df.to_numpy()
    columns = df.columns.tolist()
    for row in rows[:check_rows]:
        for i, X in enumerate(row):
            tmp = check_subfield(X)
            if columns[i] in types:
                types[columns[i]] = min(types[columns[i]], tmp)
            else:
                types[columns[i]] = tmp
    return types

def flatten_auto(df, depth=0, depth_cur=0, sep='.'):
    if isinstance(df, dict):
        df = json_normalize(df)
    elif isinstance(df, DataFrame):
        df = json_normalize(
            data=df.to_dict('records'),
            sep=sep,
        )
    else:
        raise ValueError('Either dictionary (JSON) or dataframe (array of JSON) objects are supported')
    if depth_cur != depth_cur:
        raise ValueError('Current depth has to be an integer')
    if depth != depth:
        raise ValueError('Max depth has to be an integer')
    if not isinstance(depth, int):
        raise ValueError('Max depth has to be an integer')
    if not isinstance(depth_cur, int):
        raise ValueError('Depth has to be an integer')
    if depth <= depth_cur:
        return df
    df['_ID_'] = [i+1 for i in range(df.shape[0])]
    types = get_types(df)
    columns = df.columns.tolist()
    df_flat = df
    num_flat = 0
    for col in columns:
        if types[col] in need_flattening:
            #print('Flattening', col)
            records = df_flat.to_dict('records')
            df_flat = df_flat.drop(col, axis=1)
            cur_flat = json_normalize(
                records,
                record_path=col,
                meta='_ID_',
                record_prefix=col+sep,
            )
            df_flat = merge(
                left=df_flat,
                right=cur_flat,
                left_on=[
                    '_ID_',
                ],
                right_on=[
                    '_ID_',
                ],
                how='outer',
            )
        else:
            num_flat += 1
    df_flat = df_flat.drop(
        '_ID_',
        axis=1,
    )
    #print(num_flat, df.shape[1])
    if num_flat == df.shape[1]:
        return df_flat
    else:
        return flatten_auto(df_flat, depth, depth_cur+1)