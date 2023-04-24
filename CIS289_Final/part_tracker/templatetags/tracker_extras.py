from django import template

register = template.Library()


def multiply(value, arg):
    return "{:.2f}".format(int(value) * float(arg))


register.filter("multiply", multiply)