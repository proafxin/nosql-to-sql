from pandas import (
    json_normalize,
    merge,
    DataFrame,
)
from numpy import (
    nan,
)

def flatten(dictionary):
    result = {}
    for key, value in dictionary.items():
        if type(value) == list or type(value) == dict:
            result[key] = DataFrame(json_normalize(value))
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