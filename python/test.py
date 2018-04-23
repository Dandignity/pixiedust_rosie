# coding: utf-8
#  -*- Mode: Python; -*-                                              

from __future__ import unicode_literals, print_function

import sys, json, rosie, rosie_matcher, classify_data
from adapt23 import *

# ------------------------------------------------------------------
# COMMAND LINE ARGUMENTS
# E.g. python test_classify_data ../data/HCUP-err1.csv 20
#
try:
    datafile = sys.argv[1] 
except IndexError:
    print("Missing required argument: name of data file")
    sys.exit(-1)
try:
    samplesize = sys.argv[2]
except IndexError:
    samplesize = 1

samplesize = int(samplesize)    

def test():
    s = classify_data.Schema(datafile, samplesize)
    s.load_and_process()

    for removed_row in s.inconsistent_rows:
        i, row = removed_row
        if len(row) > s.cols:
            print("row", i, "has too many columns", s.sample_data[i])
        else:
            print("row", i, "has too few columns", s.sample_data[i])

    print()
    print("In a sample of", samplesize, "rows, we excluded", len(s.inconsistent_rows),
          "rows which did not have the expected number of columns.")

    print("\nData has", s.cols, "columns, and sample set has", len(s.sample_data), "rows")
    print()

    print()
    print("For demonstration purposes, we will delete columns 4 and 22-end...")
    s.hide_column(4)
    for i in range(22, s.cols):
        s.hide_column(i)

    print()
    classify_data.print_sample_data_verbosely(s, 0)

    print()
    classify_data.print_ambiguously_typed_columns(s)


    if False:
        print()
        print("Sample data with visible columns only")
        for row in s.sample_data:
            visible = [datum for i, datum in enumerate(row) if s.column_visibility[i]]
            print(visible)

        for c in range(0, s.cols):
            data, errs = s.convert(c)
            print(c, data)
            print(c, "rows that failed:", errs)

    print()
    print("Now we change the native type of column 0 to float:")
    s.set_native_type(0, float)
    print(0, s.convert(0))

    print()
    print("Now we change the native type of column 11 to complex: (it should fail)")
    s.set_native_type(11, complex)
    print(11, s.convert(11, '*FAIL*'))

    print()
    print("Make a new column based on column 26 to extract the numeric part:")
    tr1 = classify_data.Transform(26)
    new = s.new_columns(tr1)
    assert( new is False )
    assert( 'pattern' in tr1.errors ) # Please enter a pattern

    tr1._pattern = classify_data.Pattern(None, '{[^0-9]* n}')
    new = s.new_columns(tr1)
    assert( new is False )
    assert( 'pattern' in tr1.errors ) # Please enter a pattern

    assert(len(tr1.components) == 1)
    pat = tr1.components[0]
    assert(pat._name == b'n')
    assert(pat._definition is None)
    pat._definition = b'[0-9]*'

    new = s.new_columns(tr1)
    assert( new )
    assert( tr1.errors == None )
    # print('*** pattern:', tr1._pattern._definition)
    # print('*** components:', map23(lambda c: (c._name, c._definition), tr1.components))
    # print('*** imports:', tr1.imports)

    print(new)

# ---------------------------------------------------------------------------------------------------
    print()
    print("Make TWO new columns based on column 26 to extract the alpha prefix and the numeric part:")

    tr2 = classify_data.Transform(26, '{prefix num.int}')
    new = s.new_columns(tr2)
    assert( new is False )
    assert( 'pattern' in tr2.errors )
    
    assert(len(tr2.components) == 2)
    pat = tr2.components[0]
    assert(pat._name == b'prefix')
    assert(pat._definition is None)
    pat._definition = b'[A-Z]+'

    new = s.new_columns(tr2)
    print(tr2.errors)
    assert( new )
    assert( tr2.errors is None )

    print('*** pattern:', tr2._pattern._definition)
    print('*** components:', map23(lambda c: (c._name, c._definition), tr2.components))
    print('*** imports:', tr2.imports)
    

    print(new)

    print()
    print("COMMIT the two cols above:")

    s.commit_new_columns(tr2)

    # '{prefix BreakOutCode}', ['prefix', 'BreakOutCode'], 'import num; BreakOutCode=num.int; prefix=[A-Z]+')

    s.set_native_type(28, lambda x: "foo"+str(int(x)))
    classify_data.print_sample_data_verbosely(s, 0)
# ---------------------------------------------------------------------------------------------------

test()

