%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                                                                   %%
%% This is file `pst-moire.pro'                                      %%
%%                                                                   %%
%% IMPORTANT NOTICE:                                                 %%
%%                                                                   %%
%% Package `pst-moire'                                               %%
%%                                                                   %%
%% Jürgen Gilg, Manuel Luque, Jean-Michel Sarlat                     %%
%%                                                                   %%
%% Copyright (C) 2018                                                %%
%%                                                                   %%
%% This program can redistributed and/or modified under              %%
%% the terms of the LaTeX Project Public License                     %%
%% Distributed from CTAN archives in directory                       %%
%% macros/latex/base/lppl.txt; either version 1.3c of                %%
%% the License, or (at your option) any later version.               %%
%%                                                                   %%
%% DESCRIPTION:                                                      %%
%%   `pst-moire' is a PSTricks package to draw moire patterns        %%
%%                                                                   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
/moireDict 100 dict def
moireDict begin
/pst-Fresnel {
gsave
0 0 translate
1 2 R R mul {%
    /n_1 exch def
    /n n_1 1 add def
    /R_1 n_1 sqrt def
    /R n sqrt def
    /width R R_1 sub unit def
    /radius R R_1 add 2 div unit def
    width setlinewidth
    linecolor % \pst@usecolor\pslinecolor
    circle
    stroke
    } for
grestore
} def
%
/pst-radial {
/secteur {
gsave
    newpath
    0 0 moveto
    0 0 Runit 0 1 arc
    closepath
    linecolor
    fill
grestore
    }
def
gsave
newpath
Runit 0 moveto
0 0 Runit 0 360 arc
Runit 10 div 0 moveto
0 0 Runit 10 div 360 0 arcn
closepath
clip
1 1 120 { % les angles
    secteur
    3 rotate
    } for
grestore
} def
%
/pst-linear {
/trait {
    newpath
    0 Runit neg moveto
    0 Runit lineto
    linecolor
    linewidth
%    Tr 2 div setlinewidth
    stroke
    }
def
gsave
Runit neg 0 translate
  trait
 nr {
  Tr 0 translate
  trait
} repeat
grestore
} def
%
/pst-square {
/Square {
    newpath
    Side neg Side neg moveto
    Side Side neg lineto
    Side Side lineto
    Side neg Side lineto
    closepath
    linecolor
    linewidth
    stroke
    }def
gsave
0 1 NombreTraits 2 div {% 50 carrés espacés de 2 mm
    /Side exch mm 2 mul mul def
    Square
    } for
grestore
} def
%
/pst-Newton {
/SquareNewton {
    newpath
    Side neg Side neg moveto
    Side Side neg lineto
    Side Side lineto
    Side neg Side lineto
    closepath
    linecolor
    width setlinewidth % Width mm
    stroke
    }
def
gsave
1 2 R R mul {%
    /n_1 exch def
    /n n_1 1 add def
    /R_1 n_1 sqrt def
    /R n sqrt def
    /width R R_1 sub unit def
    /Side R R_1 add 2 div unit def
     SquareNewton
    } for
grestore
}def
%
/pst-circle {
    gsave
/rad 1 mm mul def
1 1 nr {/rad exch def
    /radius rad Tr mul def
    circle     
    linecolor
    linewidth
    stroke
    } for
grestore
} def 
%
/pst-Bouasse{
/grille {
  gsave   %  <-- Herbert neu 
  newpath %  <-- Herbert neu
  0 1 51 { % 51 traits
    /trait exch def
    /xS 2 trait mul 0.01 trait dup mul mul add % en mm
        mm mul
        64 mm mul sub % en pts
    def
%gsave
%newpath
    xS 183 neg moveto
    xS 183 lineto
    linewidth
    linecolor
    stroke
    } for
} def % dessin de la grille
reduc reduc scale
    grille
grestore
} def
%
/pst-Gauss {
0 0 translate
10 dict begin
/A1 3 def
/K1 0.5 def
/TRAME {
-40 E1 2 mul 40 {/n exch def
gsave
    n E1 mul unit % x
    A1 unit 2.71828 K1 n E1 mul mul dup mul neg exp mul % y
    translate
    linecolor
    linewidth
     -6 unit -6 m mul unit moveto
      6 unit 6 m mul unit lineto
     stroke
grestore
     } for
} def
Runit neg dup
Runit 2 mul dup
rectclip
    TRAME
end
} def
%
/pst-dot {
/DOT {DotSize DotStyle Dot} def
/pas {DotSize DS 4 mul} bind def
R unit neg pas R unit { /xPos exch def
R unit neg pas R unit { /yPos exch def
xPos yPos DOT
    } for
} for
} def
%
/pst-chess {
/DOT {DotSize DotStyle Dot} def
/pas {DotSize DS 4 mul} bind def
R unit neg pas R unit { /xPos exch def
R unit neg pas R unit { /yPos exch def
xPos yPos DOT
    } for
} for
%
R unit neg pas 2 div add pas R unit pas 2 div sub { /xPos exch def
R unit neg pas 2 div add pas R unit pas 2 div sub{ /yPos exch def
xPos yPos DOT
    } for
} for
} def
%
end
% END pst-moire.pro
