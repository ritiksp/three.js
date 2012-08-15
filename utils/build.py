#!/usr/bin/env python

import argparse
import json
import os
import shutil
import sys
import tempfile


def main(argv=None):

  parser = argparse.ArgumentParser()
  parser.add_argument('--include', action='append', choices=['common', 'canvas', 'webgl', 'extras'], required=True)
  parser.add_argument('--externs', action='append', default=['externs_common.js'])
  parser.add_argument('--minify', action='store_true', default=False)
  parser.add_argument('--output', default='../build/three.js')
  # parser.add_argument('--debug', help='Generate list of files to include for debugging', action='store_true', default=False)
  args = parser.parse_args()

  # load files

  f =  open('files.json', 'r')
  files = json.load(f)
  f.close()

  output = args.output

  # merge

  print(' * Building ' + output)

  file, path = tempfile.mkstemp()

  for include in args.include:
    for filename in files[include]:
        src = open(filename, 'r')
        os.write(file, src.read())
        src.close()

  # save

  if args.minify is False:

      shutil.copy(path, output)

  else:

    externs = ' --externs '.join(args.externs)
    os.system('java -jar compiler/compiler.jar --warning_level=VERBOSE --jscomp_off=globalThis --externs %s --jscomp_off=checkTypes --language_in=ECMASCRIPT5_STRICT --js %s --js_output_file %s' % (externs, path, output))

    # header

    f = open(output,'r')
    text = f.read()
    f.close()

    f = open(output,'w')
    f.write(("// %s - http://github.com/mrdoob/three.js\n" % os.path.basename(output)) + text)
    f.close()

  os.unlink(path)


if __name__ == "__main__":
  main()

