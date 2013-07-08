from django import template

register = template.Library()

@register.filter(name='addpoemslashes')
def addpoemslashes(value):
    """Replaces all newlines with slashes """
    return value.replace("\r", "").replace("\n", ' / ')

@register.filter(name='truncatefrontpage')
def truncatefrontpage(value):
  return addpoemslashes("\n".join(value.split("\n")[:4]))

# @register.filter(name='cut')
# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

# @register.filter()
# def lower(value): # Only one argument.
#     """Converts a string into all lowercase"""
#     return value.lower()
