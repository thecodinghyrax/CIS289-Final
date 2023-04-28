from django import template

register = template.Library()


def multiply(value, arg):
    '''
    For multiplying two numbers in a template and formatting the result to two digits
    :param value: value is passed in implicitly from the filter
    :param arg: A number to multiply with the value
    :returns: The product as a two digit float
    '''
    return "{:.2f}".format(int(value) * float(arg))


register.filter("multiply", multiply)


def de_space(value):
    '''
    For removing a space in a string and replacing it with an underscore
    :param value: value is passed in implicitly from the filter
    :returns: The value string with underscored instead of spaces
    '''
    new_value = str(value).replace(" ", "_")
    return new_value


register.filter("de_space", de_space)


def typeof(value):
    '''
    Returns the type of the value in the template for debugging
    :param value: value is passed in implicitly from the filter
    :returns: The datatype of the value
    '''
    return type(value)


register.filter("typeof", typeof)


def get_value(dict, key):
    '''
    For getting the value of a dict using the provided key
    :param dict: value is a dict passed in implicitly from the filter
    :param key: A key from the dictonary
    :returns: The the value of the dict[key]
    '''
    return dict[key]


register.filter("get_value", get_value)


def get_index(passed_list, index):
    '''
    For retreving a list value based on the index 
    :param passed_list: A list of items that is passed in implicitly from the filter
    :param index: The index of a value from the list
    :returns: The value of the list item at the index specificed
    '''
    return passed_list[index]


register.filter("get_index", get_index)

