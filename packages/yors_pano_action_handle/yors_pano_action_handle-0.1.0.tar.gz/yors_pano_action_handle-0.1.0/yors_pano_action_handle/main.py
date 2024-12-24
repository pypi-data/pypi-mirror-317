# action util module
# feat(core): def action_call_aliass
action_call_aliass=[]

# feat(core): def action_skip_aliass
action_skip_aliass=[]

# feat(core): def func to std action alias
def action_alias_std(alias:list[str]):
    """
    action_call_aliass=action_alias_std(action_call_aliass)
    """
    # return [x.upper() for x in alias]
    return [ action_value_camlize(x) for x in alias]

# feat(core): def func to std action value
def action_value_std(flag,first=""):
    """
    action_value_std(flag,"skip")

    input = action_value_std(flag,first)

    """
    input=""
    try:
        stri=""
        if isinstance(flag,str):
            stri=flag
        else:
            stri=str(flag)
        input=stri
    except:
        input=first
    # input=input.upper()
    input=action_value_camlize(input)

    return input

# feat(core): def func to camelize action value
def action_value_camlize(input:str):
    if len(input)>=1:
        u= input.upper()
        s= input.lower()
        u=u[0:1]
        s=s[1:]
        return f"{u}{s}"
    return input.lower()

# feat(core): def func to read action value from types

def action_values_from_types(types:list[str]):
    values=[]
    for x in types:
        values.extend(x.split(":"))
    return values

# feat(core): def func to enable action value from types
def action_enable_values_from_types(types:list[str],reverse=False):
    values=[]
    for x in types:
        e,n=x.split(":")
        if reverse:
            e=n
        values.append(e)
    return values

# feat(core): def func to check if action is skip
def action_skip_check(flag,first="skip"):
    global action_skip_aliass
    input = action_value_std(flag,first)
    if input in action_skip_aliass:
        return True
    return False

# feat(core): def func to check if action is call
def action_call_check(flag,first="call"):
    global action_call_aliass
    input = action_value_std(flag,first)
    if input in action_call_aliass:
        return True
    return False

# feat(core): def func to check if action is one of some actions
def action_is_one_of_them(flag,actions):
    """
    action_is_one_of_them("0",action_true_values)
    """
    input = action_value_std(flag)
    if input in actions:
        return True
    return False

# feat(core): def func to check if action is enable
def action_is_enable(flag,actions=None):
    """
    action_is_enable("0")

    action_is_enable("1")

    action_is_enable("enable")

    action_is_enable("disable")
    """
    global action_call_aliass
    them=action_call_aliass
    if actions is not None:
        them=actions
    
    input = action_value_std(flag)
    if input in them:
        return True
    return False

# feat(core): def func to reverse action value
def action_value_reverse(flag:str,action_true_values=None,action_false_values=None):
    """
    action_value_reverse("enable",action_true_values,action_false_values)
    """
    global action_call_aliass
    themt=action_call_aliass
    global action_skip_aliass
    themf=action_skip_aliass

    if action_true_values is not None:
        themt=action_true_values
    if action_false_values is not None:
        themf=action_false_values

    input = action_value_get(flag)
    # print(flag,input,themt,themf)
    # input=flag
    if input in themt:
       return themf.__getitem__(themt.index(input))
    
    if input in themf:
       return themt.__getitem__(themf.index(input))

    # r = [s for s in themt if input in s]
    # if len(r)>0:
    #    return r[0]
    # r = [s for s in themf if input in s]
    # if len(r)>0:
    #    return r[0]

# feat(core): def func to read action value
def action_value_get(flag:str,action_true_values=None,action_false_values=None):
    """
    action_value_get("enable",action_true_values,action_false_values)
    """
    global action_call_aliass
    themt=action_call_aliass
    global action_skip_aliass
    themf=action_skip_aliass

    if action_true_values is not None:
        themt=action_true_values
    if action_false_values is not None:
        themf=action_false_values

    input = action_value_std(flag)
    # input=flag

    r = [s for s in themt if input in s]
    if len(r)>0:
       return r[0]
    r = [s for s in themf if input in s]
    if len(r)>0:
       return r[0]
    return themt[0]

# type ACTION_KV = list[float]
# from typing import Literal
# type ActionKv = Literal["enable:disable", "On:Off", "true:false","call:skip","0:1"]
# SyntaxError: invalid syntax

# feat(core): def var action types
action_types=["enable:disable", "On:Off", "true:false","call:skip","0:1"]
# feat(core): def var action values
action_values= action_values_from_types(action_types)

# feat(core): def var action ture values
action_true_values=action_enable_values_from_types(action_types)
# feat(core): def var action false values
action_false_values=action_enable_values_from_types(action_types,True)
# feat(core): ini var action call alias from true values
action_call_aliass = action_alias_std(action_true_values)
# feat(core): ini var action skip alias from false values
action_skip_aliass = action_alias_std(action_false_values)
# feat(core): def var action code type
action_code_type=(action_types, {"default": "true:false"})
# feat(core): def var node action values
node_action_values=(action_values, {"default": action_values[0]})
