## Implementation of Iterated Consesus in Python.
Generates all prime implicants (aka prime cubes) given any cover to a boolean function.

Input to function iterated_consensus() is a cover in the form of [ [cube1] , [cube2] , ... ]

Where each cube is an array of 0s, 1s, or -s (dont cares) represented by three letters

(0): ZER\
(1): ONE\
(-): DNC

Example:
```
  cube1 = [ZER, DNC, DNC, ONE]
  cube2 = [DNC, ZER, ZER, DNC]
  cube3 = [ONE, ONE, DNC, ZER]
  cover = [cube1, cube2, cube3]
```

Output is a list of all prime implicants printed on stdout

Example: \
Output of iterated_consensus(cover)
```
  ZER DNC DNC ONE
  
  DNC ZER ZER DNC
  
  ONE ONE DNC ZER
  
  ONE DNC ZER ZER
```
