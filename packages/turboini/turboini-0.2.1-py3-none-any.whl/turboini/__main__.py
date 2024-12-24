import sys
import os
import shutil
import configparser



filename = sys.argv[1]
cmd = sys.argv[2]
section = sys.argv[3]

target_k = None
if len(sys.argv) > 4:
    target_k = sys.argv[4]

target_v = None
if len(sys.argv) > 5:
    target_v = sys.argv[5]

if os.path.isfile(filename):
    shutil.copyfile(filename, filename + ".previous")

p = configparser.ConfigParser()

if os.path.isfile(filename):
    p.read(filename)

if cmd == "set":
    if section not in p.sections():
        p.add_section(section)
    p.set(section, target_k, target_v)

if cmd == "unset":
    if section not in p.sections():
        p.add_section(section)
    p.remove_option(section, target_k)

if cmd == "unsection":
    print(p.sections())
    p.remove_section(section)
    print(p.sections())

# for s in p.sections():
#     #logging.info("Table [%s] detected" % s)
#     for k, v in p.items(s):
#         print("[%s] %s=%s" % (s, k, v))

with open(filename, 'w') as f:
    p.write(f)
