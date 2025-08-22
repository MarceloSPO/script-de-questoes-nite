import sys

def get_url_flag():
  for index, arg in enumerate(sys.argv):
    if arg == "--url":
      url_flag = sys.argv[index + 1]      
      return url_flag