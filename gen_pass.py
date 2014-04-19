import scrypt
import string

DIFFICULTY = 2**20  # should take a few seconds to try a new master password
SALT = ""  # just some random keyboard bashing
PW_LENGTH = 25
CHARSET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+~"


def makePass(site, username, master, salt, charset, length):
  # use an unambiguous encoding
  pre_key = ""
  lengths = ",".join([str(len(x)) for x in [site, username, master]])
  pre_key += lengths + " "
  pre_key += site
  pre_key += username
  pre_key += master

  print "scrypting..."
  int_passwd = int(scrypt.hash(pre_key, salt, DIFFICULTY).encode('hex'), 16)
  print "done"
  password = ''
  for _ in range(length):
    next_index = int_passwd % len(charset)
    next_char = charset[next_index]
    int_passwd = (int_passwd - next_index) / len(charset)
    password += next_char

  return password


if __name__ == '__main__':
  import pygtk
  pygtk.require('2.0')
  import gtk
  import getpass
  import time

  site = raw_input("Site: ")
  username = raw_input("Username: ")
  master = getpass.getpass("Master password: ")

  # TODO get character set and password length from database if not previously set

  password = makePass(site, username, master, SALT, CHARSET, PW_LENGTH)
  clipboard = gtk.clipboard_get()
  clipboard.set_text(password)
  clipboard.store()
  print "Password stored to clipboard for 10 seconds"
  for i in range(10):
    print 10 - i
    time.sleep(1)
  print "Done"
  clipboard.clear()
