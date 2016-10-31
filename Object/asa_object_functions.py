def determine_obj_key(obj):
    '''
    The ASA API has different 'values' used to refer to the kind of object being referenced:
    This function takes the object being created, and returns the appropriate 'value'.

    Args:
        obj: The object being created. The type of 'value' is determined by the object.
        Values are:
            0.0.0.0/0 = AnyIPAddress
            x.x.x.x = IPv4Address
            x.x.x.x/(0 < y < 32) = IPv4Network
            x.x.x.x-y.y.y.y = IPv4Range
            object network = objectRef#NetworkObj
            object-group network = objectRef#NetworkObjGroup

    Returns:
        The appropriate dictionary 'value' based on the kind of object.

    '''
    if obj == 'any4':
        return "AnyIPAddress"
    elif '/' in obj:
        return "IPv4Network"
    elif '-' in obj:
        return "Ipv4Range"
    elif 'NetworkObjGroup' in obj:
        return "objectRef#NetworkObjGroup"
    elif 'NetworkObj' in obj:
        return "objectRef#NetworkObj"
    else:
        return "IPv4Address"
    
