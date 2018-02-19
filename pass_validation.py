import re

def pass_validation(password):
   if len(password) < 8:
       return "Make sure your password is at lest 8 letters"
   elif re.search('[0-9]',password) is None:
       return "Make sure your password has a number in it"
   elif re.search('[A-Z]',password) is None:
       return "Make sure your password has a capital letter in it"
   else:
       return "Your password seems fine"