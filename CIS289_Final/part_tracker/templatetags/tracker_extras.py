from django import template

register = template.Library()


def multiply(value, arg):
    return "{:.2f}".format(int(value) * float(arg))


register.filter("multiply", multiply)

def de_space(value):
    new_value = str(value).replace(" ", "_")
    return new_value


register.filter("de_space", de_space)


def typeof(value):
    return type(value)


register.filter("typeof", typeof)


def get_value(dict, key):
    return dict[key]


register.filter("get_value", get_value)

def get_index(passed_list, index):
    return passed_list[index]


register.filter("get_index", get_index)

