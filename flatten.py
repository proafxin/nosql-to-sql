from pandas import (
    json_normalize,
    merge,
    concat,
    DataFrame,
)
from numpy import (
    nan,
)
from copy import (
    deepcopy,
)
from timeit import (
    default_timer,
)

HAS_SUBFIELD_LIST = 1
HAS_SUBFIELD_DICT = 2
HAS_NO_SUBFIELD = 3
HAS_NO_SUBFIELD_BUT_ITERABLE = 4
need_flattening = [
    HAS_SUBFIELD_DICT,
    HAS_SUBFIELD_LIST,
]

def flatten_json(dictionary):
    result = {}
    for key, value in dictionary.items():
        if isinstance(value, list) or isinstance(value, dict):
            result[key] = DataFrame(json_normalize(value))
            result[key].columns = [key+'.'+col for col in result[key].columns.tolist()]
        else:
            result[key] = DataFrame([value], columns=[key])
        result[key] = result[key].replace(nan, '', regex=True)
    # parsed_result = []
    df = DataFrame()
    for key in result:
        #print(key)
        #print(result[key].to_numpy())
        if df.shape[0] < 1:
            # parsed_result = result[key].to_numpy()
            df = result[key]
        else:
            # result_left = parsed_result
            
            # result_right = result[key].to_numpy()
            # res = []
            #print(result_left, result_right)
            # for left_row in result_left:
            #     for right_row in result_right:
            #         tmp = list(left_row)
            #         tmp.extend(list(right_row))
            #         res.append(tmp)
            # parsed_result = res
            cols = set(df.columns.tolist())
            cols = cols.intersection(result[key].columns.tolist())
            cols = list(cols)
            if len(cols) > 0:
                df = merge(
                    left=df,
                    right=result[key],
                    left_on=cols,
                    right_on=cols,
                )
            else:
                df['common'] = 1
                result[key]['common'] = 1
                df = merge(
                    left=df,
                    right=result[key],
                    left_on=['common'],
                    right_on=['common'],
                )
                df = df.drop('common', axis=1)
        #print(parsed_result)
        #print('')
    # columns = []
    # for key in result:
        # columns.extend(result[key].columns.tolist())
    # df2 = DataFrame(parsed_result,)
    return df

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

def flatten_dataframe(df):
    rows = df.to_numpy().tolist()
    columns = df.columns.tolist()
    columns_dict = {}
    for column in columns:
        columns_dict[column] = set()
    flattened_rows = []
    start = default_timer()
    types = get_types(df)
    for row in rows:
        for i, X in enumerate(row):
            if types[columns[i]] == HAS_SUBFIELD:
                data_flattened = json_normalize(X)
                columns_flattened = [
                    columns[i]+'.'+column for column in data_flattened.columns.tolist()
                ]
                data_flattened.columns = columns_flattened
                columns_dict[columns[i]].update(columns_flattened)
            else:
                columns_dict[columns[i]].add(columns[i])
    for column in columns_dict:
        columns_dict[column] = list(columns_dict[column])
    end = default_timer()
    flattened_table = []
    print(end-start)
    start = default_timer()
    for row in rows:
        data_flattened_cur = []
        for i, X in enumerate(row):
            rows_flattened = []
            if types[columns[i]] == HAS_SUBFIELD:
                data_flattened = json_normalize(X)
                records = data_flattened.to_dict('records')
                #print(records)
                for record in records:
                    row = record
                    for column in columns_dict[columns[i]]:
                        if column not in row:
                            row[column] = {}
                    rows_flattened.append(row)
                if data_flattened.shape[0] < 1:
                    row = {}
                    for column in columns_dict[columns[i]]:
                        row[column] = {}
                    rows_flattened.append(row)
            # elif types[columns[i]] == HAS_NO_SUBFIELD_BUT_ITERABLE:
            #     for x in X:
            #         row = {}
            #         row[columns_dict[columns[i]][0]] = x
            #         rows_flattened.append(row)
            else:
                row = {}
                row[columns_dict[columns[i]][0]] = X
                rows_flattened.append(row)
            #print(rows_flattened)
            if len(data_flattened_cur) < 1:
                data_flattened_cur = rows_flattened
            else:
                left_data = data_flattened_cur
                right_data = rows_flattened
                res_cur = []
                for dict_left in left_data:
                    dict_cur = dict_left
                    if not isinstance(dict_cur, dict):
                        #print(X, dict_cur)
                        raise ValueError('Not dictionary')
                    for dict_right in right_data:
                        for key, value in dict_right.items():
                            dict_cur[key] = value
                        res_cur.append(dict_cur)
                data_flattened_cur = res_cur
        #print(len(data_flattened_cur), type(data_flattened_cur[0]))
        for record in data_flattened_cur:
            record_copy = deepcopy(record)
            #print(type(record_copy), type(data_flattened))
            flattened_table.append(record_copy)
    end = default_timer()
    print(end-start)
    return DataFrame(flattened_table)

def get_columns(df):
    types = get_types(df)
    columns_dict = []
    columns_other = []
    #print(types)
    for column in types:
        if types[column] == HAS_SUBFIELD:
            columns_dict.append(column)
        else:
            columns_other.append(column)
    columns = {
        'flat': columns_other,
        'nested': columns_dict,
    }
    return columns

def handle(row):
    if isinstance(row, dict):
        return row
    if isinstance(row, list):
        return row
    if row != row:
        return []
    return [row]
            

def flatten_improved(df):
    columns = get_columns(df)
    columns_other = columns['flat']
    columns_dict = columns['nested']
    df['row_id'] = [i+1 for i in range(df.shape[0])]
    #print(columns_dict)
    columns_other.append('row_id')
    df_left = df[columns_other]
    #print(df_left.head())
    #print(columns_dict)
    for col in columns_dict:
        #print(col)
        rows = df[col].to_numpy()
        print(col, rows[:5])
        df_right = DataFrame()
        #print(df_left.head())
        #print(col)
        for i, row in enumerate(rows):
            #print(i, row)
            df_cur = json_normalize(
                row,
                errors='ignore',
            )
            df_cur['row_id'] = i+1
            if df_right.shape[0] < 1:
                df_right = df_cur
            else:
                df_right = concat([df_right, df_cur])
            #print(df_cur)
            #print(df_right)
        df_right = df_right.reset_index(drop=True)
        #print(col)
        df_right.columns = [col+'.'+column for column in df_right.columns.tolist()]
        #print(df_right.head())
        df_left = merge(
            left=df_left,
            right=df_right,
            left_on=['row_id'],
            right_on=[col+'.row_id'],
        )
        df_left = df_left.drop(col+'.row_id', axis=1)
        #print(df_left.columns.tolist())
    df_left = df_left.drop('row_id', axis=1)
    return df_left

def get_subcolumns(df):
    rows = df.to_numpy()
    columns = set()
    for row in rows:
        #print(row)
        if not isinstance(row, list):
            continue
        if len(row) < 1:
            continue
        df_cur = json_normalize(row)
        columns.update(df_cur.columns.tolist())
    columns = list(columns)
    return columns

def get_flat_columns(df):
    types = get_types(df)
    columns = df.columns.tolist()
    columns_flat = []
    for column in columns:
        if types[column] in need_flattening:
            columns_cur = [column]
            columns_cur.extend(get_subcolumns(df[column]))
            columns_flat.append(columns_cur)
        else:
            columns_flat.append(column)
    return columns_flat

def get_all_columns(df):
    types = get_types(df)
    columns = df.columns.tolist()
    columns_flat = []
    for column in columns:
        if types[column] in need_flattening:
            columns_cur = get_subcolumns(df[column])
            for col in columns_cur:
                columns_flat.append(column+'.'+col)
        else:
            columns_flat.append(column)
    return columns_flat

def flatten_auto(df):
    if isinstance(df, dict):
        df = json_normalize(df)
    else:
        df = json_normalize(
            data=df.to_dict('records'),
            sep='_',
        )
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
                record_prefix=col+'.',
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
        return flatten_auto(df_flat)

def flatten_twice(df):
    df_flat = flatten_auto(df)
    #df_flat = flatten_auto(df_flat)
    return df_flat
