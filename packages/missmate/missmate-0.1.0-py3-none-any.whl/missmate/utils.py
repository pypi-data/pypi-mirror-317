def unpack_2d_list(list2d):
    '''Unpack a 2d list into a 1d list'''
    return [item for sublist in list2d for item in sublist]

def concat_all_dict_values_into_list(dict_of_lists):
    '''Concat all values in dict into a single list'''
    return [item for sublist in dict_of_lists.values() for item in sublist.values()]
