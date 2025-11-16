% $Id: pst-ovl.pro 1169 2020-05-01 14:27:32Z herbert $
%
%% PostScript prologue for pst-ovl.tex.
%% Version 0.04, 2014/05/12
%%
%% This program can be redistributed and/or modified under the terms
%% of the LaTeX Project Public License Distributed from CTAN archives
%% in directory macros/latex/base/lppl.txt.
%
%
/tx@ovlDict 10 dict def 
tx@ovlDict begin
%
/BeginOL { 
  dup -1 eq exch TheOL eq or 
    { IfVisible not { Visible /IfVisible true def } if } 
    { IfVisible { Invisible /IfVisible false def } if } ifelse 
} def
%
/InitOL { 
  /OLUnit [ 3000 3000 matrix defaultmatrix dtransform ] cvx def
  /Visible { CP OLUnit idtransform T moveto } def 
  /Invisible { CP OLUnit neg exch neg exch idtransform T moveto } def 
  /BOL { BeginOL } def
  /IfVisible true def 
} def
%
end
%
% END pst-ovl.pro
