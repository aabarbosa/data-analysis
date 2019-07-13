#!/usr/bin/env python
# coding: utf-8

# ### Algorithm to extract JSON objects recursively 
# 
# 

# Simple notebook for support other data manipulation, consider to use 'import json' and json.dump as it transforms the nested in a Python object, as following.
# 
# - [x] Extract keys of nested JSON, recursively
# - [ ] Summarize the structure of a nested JSON (2)
# 
# [image](./img/object.gif "segment")

# In[1]:


def extract(obj, key):
    """
    Read JSON obj recursively to find the key and 
    return its values for all occurences of key in `obj`.
    
    Warning: It can be a sub_obj if key:<dict> type
    or ignored if key is a index, thus `obj` as a dict 
    prevents the bypass of `s_obj` @seeline 9, 1: r=[].
    """
    r=[]
    def extract(obj, key, r):
        if isinstance(obj,(dict)):
            for k,v in obj.items():
                if k == key:
                    return r.append(v)
                else:
                    extract(v,key,r)
        elif isinstance(obj,(list)):
            for v in obj:
                extract(v, key, r)
    extract(obj,key,r)
    return r
    


# In[2]:


person = {1: {'name': 'John', 'age': '28', 'sex': 'Male'}, 2: {'name': 'Marie', 'age': '22', 'sex': 'Female'}}

extract(person,"name")


# ### Making nested structures futhermore 
# - [ ] Give proper substructure to the following algoritm by (2) 
# Note: For found values, the search continues for other keys within both list or dict.
# In[3]:


def extract_values(iobj, key, default=''):
    """
    Extract all values of `key` from `iobj`.
    
    iobj   : Independent object, entity or profile, 
            probably within JSON.
    key    : set of key,
            probably from a dict.
    default: Default indicator for missing values. 
    """
    return [unbox(extract(u_obj, k),default) for k in key]
def extract_pairs(u_obj, keys):
    """
    Extract all pairs `(key, values)` from `keys` indicator.
    
    u_obj: to be re-structured within @extract_nested()
    keys : subset of @keys() in u_obj
    """
    pairs = []
    for k in keys:
        pairs.append((k, unbox(extract(u_obj, k),'')))
    return pairs


# In[4]:


def extract_nested_values(obj, location, fields):
    """
    Extract specific values from extracted independent object,
    and add it to a list.

    obj     : a parsed JSON Python object or objects
    location: <list> keys to start this extraction,
    fields  : <list> keys to extact its values in `obj`,
    
    return  : [(key, values), ...]
    """
    ss_objs=[] # sub_sub_objects
    for loc in location:
        s_obj=extract(obj, loc)
        ss_objs.append(extract_values(s_obj, fields))
    return ss_objs
# [ ] How to detect (2) as this should be replaced by a parser/profile

def extract_nested_pairs(obj, location, fields):
    """
    Extract specific fields, and add it to a tuple of pairs 
    i.e, apply extract_pairs for located JSON objects.

    obj     : a parsed JSON Python object or objects
    location: <list> keys to start this extraction,
    fields  : <list> keys to extact its values in `obj`,
    
    return  : [(key, values), ...]
    """
    ss_objs=[] # sub_sub_objects
    for loc in location:
        s_obj=extract(obj, loc)
        ss_objs.append(extract_pairs(s_obj, fields))
    return ss_objs


# In[5]:


extract_nested(person, [1,2], ['name','sex'])


# ### Conclusions
# 
#     If used correctly, the algoritms works in nested JSON with bilions of entries (without effecting its processing speed). As demonstrated in extract pairs and nested functions, the problem would be broken applying the step in the extract algorithm (recursively).
# 
# Sub-notes: I choose tuples for simplicity with matplotlib in the posterior work, althugh dict or even list could also be used effectively. You have to edit the code.

# In[6]:


# Parameters already atributed to values are shifted to the end of the function parameter's. 
def extract_df(obj, keys, loc = None):
    """
    Add dataframe on the top of extract nested.
    
    Action: Parse [(key, values), ...] to a pandas dataframe.
    see @extract_nested 
    
    if not specified `loc`, it considers
    its locator as list (the range of index in `obj`).
    """
    import pandas as pd
    
    loc = range(len(obj)) if loc == None else loc
    
    new_obj=extract_nested_values(obj, loc, keys)
    df = pd.DataFrame.from_records(new_obj, columns = keys)
    
    return df

