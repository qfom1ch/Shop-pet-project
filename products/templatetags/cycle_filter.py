from django import template

register = template.Library()


@register.filter
def create_range(value, start_index=0):
    """range function for templates"""
    return range(start_index, value + start_index)


@register.filter
def subtract(value, arg):
    """subtraction function for templates"""
    return value - arg
