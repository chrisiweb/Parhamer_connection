# Issues

## General
- #8: Rename files/directories with special Symbols (whitespaces, dots,...)

## LaTeX File Creator 1.2.py
- #4: Can't save, when Folder doesn't exist
```
Exception in Tkinter callback
Traceback (most recent call last):
  File "/usr/lib/python3.5/tkinter/__init__.py", line 1562, in __call__
    return self.func(*args)
  File "Aufgabensammlung (inoffiziell)/LaTeX File Creator 1.2.py", line 351, in save_file_typ1
    for all in os.listdir(gk_path_temp):
FileNotFoundError: [Errno 2] No such file or directory: 'Typ 1 Aufgaben/_Grundkompetenzen/AG - Algebra und Geometrie/AG-L 5.3/Einzelbeispiele'
```

- #5: move dictionaries in config-file

## Typ1 LaTeX file assistent 4.0.py
- #6: Searching doesn't work
```
Exception in Tkinter callback
Traceback (most recent call last):
  File "/usr/lib/python3.5/tkinter/__init__.py", line 1562, in __call__
    return self.func(*args)
  File "Aufgabensammlung (inoffiziell)/Typ 1 Aufgaben/Typ1 LaTeX file assistent 4.0.py", line 297, in control_cb
    for i, line in enumerate(file):
  File "/usr/lib/python3.5/codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4 in position 32: invalid continuation byte
```

## Typ2 LaTeX file assistent 3.1.py
- #7: Searching doesn't work
```
Exception in Tkinter callback
Traceback (most recent call last):
  File "/usr/lib/python3.5/tkinter/__init__.py", line 1562, in __call__
    return self.func(*args)
  File "Aufgabensammlung (inoffiziell)/Typ 1 Aufgaben/Typ1 LaTeX file assistent 4.0.py", line 297, in control_cb
    for i, line in enumerate(file):
  File "/usr/lib/python3.5/codecs.py", line 321, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4 in position 32: invalid continuation byte
```
