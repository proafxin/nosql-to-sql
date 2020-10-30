from pandas import (
    json_normalize,
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
    parsed_result = []
    for key in result:
        #print(key)
        #print(result[key].to_numpy())
        if len(parsed_result) < 1:
            parsed_result = result[key].to_numpy()
        else:
            result_left = parsed_result
            
            result_right = result[key].to_numpy()
            res = []
            #print(result_left, result_right)
            for left_row in result_left:
                for right_row in result_right:
                    tmp = list(left_row)
                    tmp.extend(list(right_row))
                    res.append(tmp)
            parsed_result = res
        #print(parsed_result)
        #print('')
    columns = []
    for key in result:
        columns.extend(result[key].columns.tolist())
    df = DataFrame(parsed_result, columns=columns)
    return df