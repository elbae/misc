# Some shell commands

### Man page organization
```
1   User commands
2   Programming interfaces for kernel system calls
3   Programming interfaces to the C library
4   Special files such as device nodes and drivers
5   File formats
6   Games and amusements
7   Misc
8   Sysadmin commands
```
### apropos
apropos - search the list of man pages for possible matches based on a search term.
```
apropos crack
cracklib-check (8)   - Check passwords using libcrack2
cracklib-format (8)  - cracklib dictionary utilities
cracklib-packer (8)  - cracklib dictionary utilities
cracklib-unpacker (8) - cracklib dictionary utilities
create-cracklib-dict (8) - Check passwords using libcrack2
fcrackzip (1)        - a Free/Fast Zip Password Cracker
fcrackzipinfo (1)    - display zip information
update-cracklib (8)  - Regenerate cracklib dictionary
```

### whatis
```
whatis (1)           - display one-line manual page descriptions
```

### info
```
info (1)             - read Info documents
```

### zless
```
zless (1)            - file perusal filter for crt viewing of compressed text
	read .gzip
```
## Expansion

```
echo Front-{A,B,C}-Back
Front-A-Back Front-B-Back Front-C-Back
```
```
echo Num_{1..10}
Num_1 Num_2 Num_3 Num_4 Num_5 Num_6 Num_7 Num_8 Num_9 Num_10
```

```
echo {Z..A}    
Z Y X W V U T S R Q P O N M L K J I H G F E D C B A
```

```
echo {Z,A{1..5},b{1..3}} 
Z A1 A2 A3 A4 A5 b1 b2 b3
```

### Curson movement commands
```
ctrl+a   move cursor to the beginning of the line.
ctrl+e   move cursor to the end of the line.
ctrl+f   move cursor forward one char
ctrl+b   move cursor backward one char
alt+f    move cursor forward one word
alb+b    move cursor backward one word
ctrl+l   clear 
```