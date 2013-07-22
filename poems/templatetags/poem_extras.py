from django import template

register = template.Library()

@register.filter(name='addpoemslashes')
def addpoemslashes(value):
    """Replaces all newlines with slashes """
    return value.replace("\r", "").replace("\n", ' / ')

@register.filter(name='truncatefrontpage')
def truncatefrontpage(value):
  max_length = 400
  newval = []
  for line in value.split("\n"):
    newval.append(line)
    if sum([len(l) for l in newval]) + len(line) > max_length:
      break
  return addpoemslashes("\n".join(newval) )

@register.filter(name='fixFormatNames')
def fixFormatNames(value):
  if value == "Freeverse":
    return "Free Verse"
  else:
    return value

# @register.filter(name='cut')
# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

# @register.filter()
# def lower(value): # Only one argument.
#     """Converts a string into all lowercase"""
#     return value.lower()
