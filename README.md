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

### Cursor movement commands
```
ctrl+a   move cursor to the beginning of the line.
ctrl+e   move cursor to the end of the line.
ctrl+f   move cursor forward one char.
ctrl+b   move cursor backward one char.
alt+f    move cursor forward one word.
alb+b    move cursor backward one word.
ctrl+l   clear.
```

### Edit, cut and paste commands
```
ctrl+d   delete the char.
ctrl+t   transpose the current char with the preceding.
alt+t    transpose the word with the preceding.
alt+l    convert the chars from the cursor to the end to lowercase.
alt+u    convert the chars from the cursor to the end to uppercase.

ctrl+k   kill text from cursor to end of the line.
ctrl+u   kill text from cursor to beginning of the line.
alt+d    kill text from cursor to end of the word.
alt+bksp kill text from cursor to beginning of the word.
ctrl+y   yank text from kill-ring and insert it at the cursor location.
```

### Completion
```
$   variables
~   users
    commands
```    

### Shell history

```
!n      expands the n° line of the history
!str    repeat last list item starting with string
!?str   repeat last list item containing string
ctrl+r  search backwards in the history
ctrl-j  copies the text result of search
```

### File attributes

```
-rw-rw-r-- 1 andrea andrea 1 mag 12 15:30 foo.txt

first char   file type
chars 1-10   file mode
 owner permission
 group permission
 world permission
```

The file type can be:
```
-   regular file
d   directory
l   symbolic link
c   character special file
b   block special file
```

### File permission examples
```
-rwx------   regular file readable, writable and executable only by the file owner.
-rw-------   regular file readable and writable only by the file owner.
-rw-r--r--   regual file readable and writable by the owner. Members of file's owner group can read, world can read.
lrwxrwxrwx   symbolic link with dummy permissions.
drwxrwx---   directory, owner and members of the same group may enter the dir and create, rename and remove files within it.
drwxr-x---   directory, owner may enter the directory and create, rename and delete files. Members of the same group may enter but cannot create, delete, or rename files.
```

### Chmod 
Changes the mode (permission) of a file or directory with either octal number representation and symbolic representation.

####test
```
```



