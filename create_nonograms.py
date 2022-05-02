
nonogramm_empty = """\\renewcommand{\\arraystretch}{1.2}
\\begin{tabular}{c|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|}
\multicolumn{1}{l}{}&\multicolumn{1}{c}{A}&\multicolumn{1}{c}{B}&\multicolumn{1}{c}{C}&\multicolumn{1}{c}{D}&\multicolumn{1}{c}{E}&\multicolumn{1}{c}{F}&\multicolumn{1}{c}{G}&\multicolumn{1}{c}{H}&\multicolumn{1}{c}{I}&\multicolumn{1}{c}{J}\\\\ \cline{2-11}
0& A0 & B0 & C0 & D0 & E0 & F0 & G0 & H0 & I0 & J0 \\\\ \cline{2-11}
1& A1 & B1 & C1 & D1 & E1 & F1 & G1 & H1 & I1 & J1 \\\\ \cline{2-11}
2& A2 & B2 & C2 & D2 & E2 & F2 & G2 & H2 & I2 & J2 \\\\ \cline{2-11} 
3& A3 & B3 & C3 & D3 & E3 & F3 & G3 & H3 & I3 & J3 \\\\ \cline{2-11}
4& A4 & B4 & C4 & D4 & E4 & F4 & G4 & H4 & I4 & J4 \\\\ \cline{2-11}
5& A5 & B5 & C5 & D5 & E5 & F5 & G5 & H5 & I5 & J5 \\\\ \cline{2-11}
6& A6 & B6 & C6 & D6 & E6 & F6 & G6 & H6 & I6 & J6 \\\\ \cline{2-11}
7& A7 & B7 & C7 & D7 & E7 & F7 & G7 & H7 & I7 & J7 \\\\ \cline{2-11} 
8& A8 & B8 & C8 & D8 & E8 & F8 & G8 & H8 & I8 & J8 \\\\ \cline{2-11} 
9& A9 & B9 & C9 & D9 & E9 & F9 & G9 & H9 & I9 & J9 \\\\ \cline{2-11}
\end{tabular}"""

list_all_pixels = [
'A0', 'B0', 'C0', 'D0', 'E0', 'F0', 'G0', 'H0', 'I0', 'J0',
'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1',
'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2',
'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3',
'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4',
'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5',
'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6', 'J6',
'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7',
'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8',
'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9']

all_nonogramms = {
    'affe': [
        "A1", "A2", "A8", "A9", "B0", "B1", "B2", "B5", "B6", "B8", "B9", "C0", "C1", "C2", "C3", "C4", "C5", "C8", "C9", "D3",
        "D4", "D5", "D6", "D7", "D8", "D9", "E3", "E4", "E8", "E9", "F3", "F4", "F8", "F9", "G3", "G4", "G5", "G8", "G9", "H0",
        "H1", "H3", "H4", "H5", "H6", "H8", "H9", "I0", "I3", "I6", "I7", "I8", "I9", "J0", "J1", "J2", "J3", "J8", "J9"
    ],
    'affengesicht': [
        "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "B1", "B2", "B3", "B8", "B9", "C0", "C1", "C2", "C4", "C9", "D0", "D1",
        "D2", "D4", "D9", "E0", "E1", "E2", "E6", "E8", "E9", "F0", "F1", "F2", "F6", "F8", "F9", "G0", "G1", "G2", "G4", "G9",
        "H0", "H1", "H2", "H4", "H9", "I1", "I2", "I3", "I8", "I9", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9"
    ],
    'alien 1':[
    "A4", "A5", "A6", "B0", "B3", "B4", "C0", "C2", "C3", "C4", "C5", "C6", "C7", "D1", "D2", "D3", "D5", "D6", "D8", "E2",
    "E3", "E4", "E5", "E6", "F2", "F3", "F4", "F5", "F6", "G1", "G2", "G3", "G5", "G6", "G8", "H0", "H2", "H3", "H4", "H5",
    "H6", "H7", "I0", "I3", "I4", "J4", "J5", "J6"        
    ],
    'alien 2': [
        "A5", "A6", "A7", "B4", "B5", "B6", "C3", "C4", "C5", "C6", "C7", "D3", "D5", "D6", "D8", "E2", "E3", "E4", "E5", "E6", "F3",
        "F5", "F6", "F8", "G3", "G4", "G5", "G6", "G7", "H4", "H5", "H6", "I5", "I6", "I7"
    ],
    'alien 3' : [
        "A5", "B4", "C1", "C2", "C3", "C4", "C5", "C7", "D2", "D4", "D5", "D6", "E2", "E3", "E4", "E5", "F2", "F4", "F5", "F6", "G1",
        "G2", "G3", "G4", "G5", "G7", "H4", "I5"
    ],
    'alien 4' : [
        "B4", "B5", "C2", "C3", "C4", "C5", "C7", "D2", "D5", "D6", "E2", "E3", "E4", "E5", "F2", "F5", "F6", "G2", "G3", "G4", "G5", "G7", "H4", "H5"
    ],
    'alien 5' : [
        "A2", "B1", "B3", "B5", "B6", "C1", "C3", "C4", "C5", "C6", "C7", "D3", "D5", "D6", "D8", "E3", "E4", "E5", "E6", "F3", "F5", "F6", "F8", "G1",
        "G3", "G4", "G5", "G6", "G7", "H1", "H3", "H5", "H6", "I2"
    ],
    'alien 6' : [
        "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B6", "B7", "C1", "C4", "C6", "C7", "C8", "C9", "D0", "D1", "D2", "D6", "D7", "D8",
        "D9", "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "G0", "G1", "G2", "G6",
        "G7", "G8", "G9", "H1", "H4", "H6", "H7", "H8", "H9", "I1", "I2", "I6", "I7", "J2", "J3", "J4", "J5", "J6"    
    ],
    'babylöwe' : [
        "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "B0", "B5", "B6", "B7", "B8", "B9", "C0", "C1", "C3", "C6", "C7",
    "C8", "C9", "D0", "D1", "D4", "D6", "D9", "E0", "E1", "E3", "E8", "E9", "F0", "F5", "F9", "G0", "G1", "G2", "G3", "G4", "G5", "G8", "G9", "H0",
    "H1", "H4", "H5", "H8", "H9", "I0", "I1", "I2", "I9", "J0", "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9"
    ],
    'blume': [
        "C6", "C7", "D1", "D2", "D3", "D6", "D7", "E0", "E1", "E3", "E4", "E8", "F0", "F2", "F4", "F5", "F6", "F7", "F8", "F9", "G0", "G1", "G3", "G4",
        "G7", "H1", "H2", "H3", "H5", "H6", "I5", "I6"
    ],
    'clown': [
        "A2", "A4", "A5", "B2", "B3", "B6", "B7", "B9", "C1", "C2", "C8", "C9", "D0", "D2", "D3", "D9", "E0", "E2", "E4", "E5",
        "E7", "E9", "F0", "F1", "F2", "F4", "F5", "F7", "F9", "G0", "G1", "G2", "G3", "G6", "G9", "H1", "H2", "H8", "H9", "I2",
        "I3", "I6", "I7", "I9", "J2", "J4", "J5"
    ],
    'cocktailglas': [
        "A2", "A3", "B2", "B3", "B4", "C2", "C4", "C5", "D2", "D5", "D9", "E2", "E5", "E6", "E7", "E8", "E9", "F2", "F4", "F5",
        "F6", "F7", "F8", "F9", "G2", "G3", "G5", "G9", "H1", "H2", "H4", "H5", "I0", "I2", "I3", "I4", "J2", "J3"
    ],
    'elefant': [
        "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "B0", "B1", "B2", "B3", "B4", "B5", "C0", "C1", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "D0", "D1",
        "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E0", "E1", "E2", "E3", "E4", "E6", "E7", "E8", "E9", "F6", "F7", "G2", "G3", "G4", "G5", "G6", "G7",
        "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "I2", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "J3", "J4", "J5", "J6", "J7", "J8", "J9"
    ],
    'ente': [
        "A2", "B1", "B2", "C0", "C2", "C3", "C4", "C5", "C6", "C7", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "E4", "E5", "E6", "E7",
        "E8", "E9", "F5", "F6", "F7", "F8", "F9", "G5", "G6", "G7", "G8", "G9", "H5", "H6", "H7", "H8", "I5", "I6", "I7", "J3", "J4", "J5", "J6"    
    ],
    'fernseher': [
        "A2", "A3", "A4", "A5", "A6", "A7", "A8", "B2", "B4", "B6", "B7", "B8", "B9", "C0", "C2", "C3", "C4", "C5", "C6", "C7",
        "C8", "D1", "D2", "D3", "D7", "D8", "E2", "E8", "F2", "F8", "G1", "G2", "G8", "H0", "H2", "H8", "I2", "I3", "I7", "I8",
        "I9", "J2", "J3", "J4", "J5", "J6", "J7", "J8"
    ],
    'fragezeichen' : [
        "B1", "B2", "C0", "C1", "C2", "D0", "E0", "E5", "E6", "E8", "E9","F0", "F5",
    "F6", "F8", "F9", "G0", "G4", "G5", "H0", "H1", "H2", "H3", "H4", "H5", "I1", "I2", "I3", "I4"
    ],
    'fragezeichen 2': [
        "C2", "C3", "D1", "D2", "D3", "E1", "E2", "E5", "E6", "E8", "F1", "F2", "F5", "F6", "F8", "G1", "G2", "G3", "G4", "G5", "H2", "H3", "H4"        
    ],
    'fuchs': [
        "B1", "B2", "B3", "B4", "B5", "B6", "C2", "C3", "C4", "C5", "C6", "C7", "D3", "D4", "D6", "D7", "D8", "E4", "E5", "E6", "E7", "E8", "E9", "F4",
        "F5", "F6", "F7", "F8", "F9", "G3", "G4", "G6", "G7", "G8", "H2", "H3", "H4", "H5", "H6", "H7", "I1", "I2", "I3", "I4", "I5", "I6"
    ],
    'hase 1': [
        "A5", "A6", "A7", "B4", "B5", "B6", "B7", "B8", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C8", "C9", "D0",
    "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E4", "E5", "E6", "E7", "E9", "F4", "F5", "F6", "F7", "F9", "G0",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "H0", "H1", "H2", "H3", "H4", "H5", "H6", "H8", "H9", "I4", "I5",
    "I6", "I7", "I8", "J5", "J6", "J7"
    ],
    'hase 2': [
        "B3", "B4", "C2", "C4", "C9", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E3", "E4", "E5", "E6",
    "E7", "E8", "F4", "F5", "F6", "F7", "F8", "F9", "G5", "G6", "G7", "G8", "G9", "H6", "H7", "H8", "H9", "I8"
    ],
    'haus': [
        "A4", "A5", "A6", "A7", "A8", "A9", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "C2", "C3", "C4", "C5", "C6",
    "C7", "C8", "C9", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E0", "E1", "E2", "E3", "E4", "E7", "E8", "E9",
    "F0", "F1", "F2", "F3", "F4", "F7", "F8", "F9", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "H2", "H3", "H4",
    "H5", "H6", "H7", "H8", "H9", "I3", "I4", "I5", "I6", "I7", "I8", "I9", "J4", "J5", "J6", "J7", "J8", "J9"
    ],
    'haus 2': [
        "B3", "B4", "B5", "B6", "B7", "B8", "B9", "C0", "C1", "C2", "C3", "C4", "C9", "D1", "D2", "D3", "D4", "D6", "D7", "D9", "E1",
        "E2", "E3", "E4", "E9", "F1", "F2", "F3", "F4", "F6", "F7", "F8", "F9", "G1", "G2", "G3", "G4", "G6", "G7", "G8", "G9", "H2",
        "H3", "H4", "H9", "I3", "I4", "I5", "I6", "I7", "I8", "I9"
    ],
    'herz': [
        "A2", "A3", "A4", "B1", "B2", "B5", "C1", "C6", "C7", "D2", "D7", "D8", "E3", "E8", "E9", "F3", "F8", "F9", "G2", "G7",
        "G8", "H1", "H6", "H7", "I1", "I2", "I5", "J2", "J3", "J4"        
    ],
    'hund': [
        "A1", "A2", "B1", "B2", "C0", "C1", "C2", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E0",
    "E1", "E2", "E3", "E4", "E5", "E6", "F3", "F4", "F5", "F6", "G3", "G4", "G5", "G6", "H3", "H4", "H5", "H6", "I3", "I4", "I5", 
    "I6", "I7", "I8", "I9", "H3"
    ],
    'käfer': [
        "A2", "A3", "A4", "A5", "B0", "B2", "B3", "B4", "B5", "B6", "B7", "C0", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "D0", "D1",
        "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E1", "E2", "E3", "E4", "E5", "F1", "F2", "F3", "F4", "F5", "G0", "G1", "G3", "G4",
        "G5", "G6", "G7", "G8", "G9", "H0", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "I0", "I2", "I3", "I4", "I5", "I6", "I7", "J2", "J3", "J4", "J5"
    ],
    'kaffee': [
        "A8", "B3", "B4", "B5", "B6", "B7", "B9", "C0", "C1", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "D3", "D6", "D7",
        "D8", "D9", "E0", "E1", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "G0", "G1",
        "G3", "G4", "G5", "G6", "G7", "G8", "G9", "H3", "H4", "H5", "H6", "H7", "H9", "I4", "I6", "I9", "J4", "J5", "J8"
    ],
    'kamel': [
        "A5", "A6", "B5", "B6", "B7", "C7", "D6", "D7", "D9", "E5", "E6", "E7", "E8", "E9", "F4", "F5", "F6", "F7", "G0", "G4",
    "G5", "G6", "G7", "G9", "H2", "H5", "H6", "H7", "H8", "H9", "I0", "I1", "I6", "I7", "J0", "J1", "J3"        
    ],
    'katze': [
    "A3", "A6", "A7", "B1", "B2", "B3", "B4", "B6", "B9", "C0", "C1", "C2", "C4",
    "C5", "C6", "C7", "C8", "C9", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "E0",
    "E1", "E2", "E4", "E5", "E6", "E7", "E8", "E9", "F1", "F2", "F3", "F4", "F6",
    "F7", "F8", "F9", "G3", "G7", "G8", "G9", "H8", "H9", "I4", "I5", "I6", "I8",
    "J3", "J4", "J6", "J7", "J8"
    ],
    'kirschen': [
        "A3", "B2", "B3", "B6", "B7", "B8", "C1", "C3", "C5", "C6", "C7", "C8", "C9", "D1", "D2", "D5", "D6", "D7", "D8", "D9",
    "E0", "E1", "E5", "E6", "E8", "E9", "F0", "F1", "F2", "F3", "F4", "F6", "F7", "F8", "G0", "G2", "G5", "G9", "H1", "H3",
    "H5", "H6", "H7", "H8", "H9", "I2", "I3", "I5", "I6", "I8", "I9", "J3", "J6", "J7", "J8"        
    ],
    'kobold' : [
        "A4", "B4", "B5", "B6", "C0", "C1", "C2", "C3", "C4", "C8", "D0", "D1", "D2", "D3", "D4", "D6", "D8", "D9", "E0", "E1",
        "E2", "E3", "E4", "E7", "E9", "F0", "F1", "F2", "F3", "F4", "F7", "F9", "G0", "G1", "G2", "G3", "G4", "G6", "G8", "G9",
        "H0", "H1", "H2", "H3", "H4", "H8", "I4", "I5" ,"I6", "J4"
    ],
    'könig': [
        "B3", "B4", "B5", "B6", "B7", "C1", "C2", "C4", "C8", "D2", "D4", "D7", "D8", "E1", "E2", "E5", "E7", "E8", "F2", "F4",
        "F7", "F8", "G1", "G2", "G4", "G8", "H3", "H4", "H5", "H6", "H7"
    ],
    'krankenwagen': [
        "A2", "A3", "A4", "A5", "A6", "A9", "B1", "B2", "B5", "B6", "B7", "B9", "C1", "C5", "C6", "C8", "C9", "D0", "D1", "D2",
        "D3", "D4", "D5", "D6", "D7", "D9", "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E9", "F1", "F2", "F3", "F4", "F5", "F6",
        "F9", "G1", "G2", "G4", "G5", "G6", "G9", "H1", "H5", "H6", "H7", "H9", "I1", "I2", "I4", "I5", "I6", "I8", "I9",
        "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J9"        
    ],
    'lama': [
        "A2", "A3", "B0", "B1", "B2", "B3", "C2", "C3", "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E6", "E7", "E8",
        "E9", "F6", "F7", "G6", "G7", "H6", "H7", "H8", "H9", "I4", "I5", "I6", "I7", "I8", "I9"
    ],
    'läufer': [
        "A9", "B3", "B4", "B8", "B9", "C2", "C3", "C7", "C8", "D2", "D5", "D6", "D7", "E2", "E3", "E4", "E5", "E6", "E9", "F2", "F3", "F4",
        "F6", "F8", "F9", "G0", "G1", "G2", "G3", "G6", "G7", "G8", "H0", "H1", "H3", "I3", "J2", "J3"
    ],
    'luftballon': [
        "A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B0",
        "C4", "C5", "C6", "C7", "C8", "C9", "D5", "D6", "D7", "D8", "D9", "E6", "E9", "F9", "G6", "G9", "H1", "H2", "H5", "H6",
        "H7", "H8", "H9", "I0", "I4", "I5", "I6", "I7", "I8", "I9", "J0", "J1", "J2", "J3", "J4", "J5", "J6", "J7", "J8", "J9"
    ],
    'marienkäfer': [
        "B5", "B6", "B7", "C4", "C5", "C6", "C7", "C8", "D1", "D3", "D5", "D6", "D7", "D9", "E2", "E3", "E4", "E5", "E7", "E8", "E9", "F2", "F3",
        "F4", "F5", "F6", "F7", "F8", "F9", "G1", "G3", "G5", "G6", "G8", "G9", "H4", "H5", "H6", "H7", "H8", "I5", "I6", "I7"
    ],
    'maus': [
        "A6", "A7", "A8", "B1", "B2", "B9", "C0", "C3", "C5", "C6", "C7", "C8", "C9", "D0", "D2", "D3", "D4", "D5", "D6", "D7",
        "D8", "D9", "E1", "E2", "E4", "E5", "E6", "E7", "E8", "E9", "F2", "F3", "F4", "F6", "F7", "F8", "F9", "G1", "G2", "G4",
        "G5", "G6", "G7", "G8", "G9", "H0", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "I0", "I3", "I5", "I6", "I7", "I8",
        "I9", "J1", "J2", "J6", "J7", "J8"
    ],
    'musiknoten': [
        "A7", "A8", "B6", "B7", "B8", "B9", "C6", "C7", "C8", "C9", "D1", "D2", "D3", "D4", "D5", "D6",
    "D7", "D8", "E1", "E3", "F1", "F3", "G0", "G3", "G6", "G7", "H0", "H2", "H5", "H6", "H7", "H8", "I0", "I2", "I5",
    "I6", "I7", "I8", "J0", "J1", "J2", "J3", "J4", "J5", "J6", "J7"
    ],
    'pacman': [
        "A3", "A4", "A5", "A6", "A7", "B2", "B8", "C1", "C9", "D1", "D9", "E1", "E9", "F1", "F3", "F9", "G1", "G5", "G9", "H1", "H4",
        "H6", "H9", "I2", "I3", "I7", "I8", "J5"
    ],
    'panda': [
        "A0", "A1", "A2", "B0", "B1", "B4", "B5", "B6", "C0", "C3", "C6", "D3", "D4", "D5", "D6", "E7", "E9", "F7", "F9", "G3", "G4", "G5",
        "G6", "H0", "H3", "H6", "I0", "I1", "I4", "I5", "I6", "J0", "J1", "J2"
    ],
    'pfeil & bogen': [
        "A4", "A6", "B5", "C5", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E2", "E5", "E8", "F3", "F5", "F7", "G4", "G5", "G6",
        "H5", "I4", "I5", "I6", "J5"
    ],
    'pudel': [
        "A1", "A2", "B1", "B2", "B5", "B6", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C9", "D0", "D1", "D2", "D3", "D5", "D6", "D7",
        "D8", "D9", "E1", "E2", "E3", "E6", "F6", "G6", "H5", "H6", "H7", "H9", "I5", "I6", "I7", "I8", "I9", "J3", "J4"
    ],
    'puppe': [
        "A0", "A1", "A4", "A5", "A8", "A9", "B0", "B5", "B8", "B9", "C1", "C2", "C5", "C6", "C9", "D0", "D2", "D3", "D5", "D6",
        "D7", "D8", "E0", "E1", "E2", "E4", "E5", "E6", "E7", "E8", "F0", "F1", "F2", "F4", "F5", "F6", "F7", "F8", "G0", "G2",
        "G3", "G5", "G6", "G7", "G8", "H1", "H2", "H5", "H6", "H9", "I0", "I5", "I8", "I9", "J0", "J1", "J4", "J5", "J8", "J9" 
    ],
    'qualle': [
        "A4", "A5", "A9", "B3", "B4", "B5", "B8", "C2", "C3", "C4", "C5", "C7", "C9", "D1", "D2", "D3", "D5", "D6", "D8", "E0", "E1", "E2", "E3",
        "E4", "E5", "E7", "E9", "F0", "F1", "F2", "F3", "F4", "F5", "F7", "F9", "G1", "G2", "G3", "G5", "G6", "G8", "H2", "H3", "H4", "H5", "H7",
        "H9", "I3", "I4", "I5", "I8", "J4", "J5", "J9"
    ],
    'rakete': [
        "A9", "B8", "C7", "D2", "D3", "D4", "D5", "D6", "D7", "D9", "E0", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "F0", "F1", "F2", "F3",
        "F4", "F5", "F6", "F7", "F8", "G2", "G3", "G4", "G5", "G6", "G7", "G9", "H7", "I8", "J9"
    ],
    'regenschirm': [
        "A4", "B3", "B4", "C2", "C3", "C4", "D1", "D2", "D3", "D4", "D8", "D9", "E0", "E1", "E2", "E3", "E4", "E9", "F0", "F1", "F2",
        "F3", "F4", "F5", "F6", "F7", "F8", "F9", "G1", "G2", "G3", "G4", "H2", "H3", "H4", "I3", "I4", "J4"
    ],
    'regenschirm 2': [
        "A4", "A5", "B3", "B4", "C2", "C3", "C4", "C5", "D1", "D2", "D3", "D4", "D9", "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "F1",
        "F2", "F3", "F4", "G2", "G3", "G4", "G5", "H3", "H4", "I4", "I5"
    ],
    'schildkröte': [
        "A5", "A6", "B5", "B6", "C6", "D5", "D6", "D7", "E4", "E5", "E6", "F4", "F5", "F6", "G4", "G5", "G6", "H5", "H6", "H7", "I6"
    ],
    'schmetterling': [
        "A3", "A7", "A8", "B2", "B4", "B6", "B7", "B8", "B9", "C2", "C5", "C6", "C9", "D0", "D3", "D6", "D9", "E1", "E2", "E3",
        "E4", "E5", "E6", "E7", "E8", "E9", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "G0", "G3", "G6", "G9", "H2",
        "H5", "H6", "H9", "I2", "I4", "I6", "I7", "I8", "I9", "J3", "J7", "J8"
    ],
    'schnecke': [
        "A2", "A3", "A4", "A5", "A6", "A7", "A9", "B1", "B2", "B4", "B5", "B6", "B7", "B8", "B9", "C0", "C1", "C2", "C3", "C4",
        "C5", "C6", "C7", "C8", "C9", "D0", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "E0", "E1", "E3", "E4", "E6", "E7",
        "E8", "E9", "F0", "F1", "F2", "F5", "F6", "F7", "F8", "F9", "G1", "G2", "G3", "G4", "G5", "G6", "G8", "G9", "H2", "H3",
        "H4", "H8", "H9", "I6", "I8", "I9", "J7", "J8"
    ],
    'schwert': [    
        "A8", "A9", "B4", "B8", "B9", "C5", "C7", "D5", "D6", "E4", "E5", "E6", "E7", "F3", "F4", "F5", "F8", "G2", "G3", "G4",
        "H1", "H2", "H3", "I0", "I1", "I2", "J0", "J1"
    ],
    'skorpion': [
        "A3", "A4", "A5", "A8", "B3", "B4", "B8", "B9", "C3", "C6", "C8", "C9", "D3", "D4", "D5", "D6", "D7", "D8", "E5", "E6", "E7", "F5",
        "F6", "F7", "F8", "G0", "G1", "G2", "G5", "G6", "G7", "G9", "H0", "H1", "H5", "H6", "H7", "H8", "I0", "I1", "I6", "I7", "I9", "J1",
        "J2", "J3", "J4", "J5", "J6"
    ],
    'smiley': [
        "A2", "A3", "A4", "A5", "A6", "B1", "B7", "C0", "C5", "C8", "D0", "D3", "D6", "D8", "E0", "E6", "E8", "F0", "F3", "F6", "F8", "G0",
        "G5", "G8", "H1", "H7", "I2", "I3", "I4", "I5", "I6"
    ],
    'wassermelone': [
        "A4", "A5", "A6", "A7", "B3", "B6", "B7", "C2", "C4", "C6", "C7", "D1", "D6", "D7", "E0", "E2", "E6", "E7", "F1", "F4", "F6", "F7",
        "G2", "G6", "G7", "H3", "H6", "H7", "I4", "I5", "I6", "I7"
    ],
    'wecker': [
        "A1", "A2", "B0", "B1", "B3", "B4", "B5", "B6", "C0", "C2", "C3", "C4", "C5", "C6", "C7", "C9", "D1",
    "D2", "D3", "D4", "D5", "D7", "D8", "D9", "E1", "E2", "E3", "E4", "E6", "E7", "E8", "F1", "F5", "F6", "F7", "F8",
    "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "H0", "H2", "H3", "H4", "H5", "H6", "H7", "H9", "I0", "I1",
    "I3", "I4", "I5", "I6", "J1", "J2"
    ],
}