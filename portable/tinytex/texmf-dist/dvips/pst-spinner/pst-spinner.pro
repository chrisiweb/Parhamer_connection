%% $Id: pst-spinner.pro 466 2017-05-23 05:41:09Z herbert $
%% Package `pst-spinner.pro'
%%
%%
%% This program can be redistributed and/or modified under the terms
%% of the LaTeX Project Public License Distributed from CTAN archives
%% in directory macros/latex/base/lppl.txt.
%%
/tx@spinnerDict 20 dict def tx@spinnerDict begin
%
/arctan { dup 0 ge { 1 atan }{ neg 1 atan neg } ifelse } def

/BallBearing {
  /point exch def
  /couleur exch def
  newpath
  point ri 0 360 arc
  point ri 0.15 cm add 360 0 arcn
  closepath
  0.25 setgray
  fill 
  newpath
  point r1 0 360 arc
  point r1 0.15 cm sub 360 0 arcn
  closepath
  0.25 setgray
  fill 
  newpath
  point r1 0.15 cm sub 0 360 arc
  point ri 0.15 cm add 360 0 arcn
  closepath
  couleur
  fill 
} def
%
% le contour du triple fidget spinner
/TripleSpinner {
  1 setlinejoin
  newpath
  O1 /yO1 exch def /xO1 exch def
  xO1 r1 a1 add alpha1 neg cos mul add
  yO1 r1 a1 add alpha1 neg sin mul add
  moveto
  O1 r1 a1 add alpha1 neg alpha1 180 add arc
  A' r2 alpha1 beta1 arcn
  O2 r1 a1 add 180 beta1 add alpha2 arc
  C' r2 alpha2 180 sub alpha2 neg arcn
  O3 r1 a1 add alpha2 neg 180 add 360 beta1 sub arc
  B' r2 beta1 180 sub neg alpha1 180 sub neg arcn
  r1 rho moveto
  O1 r1 360 0 arcn
  r1 0 moveto
  0 0 r1 360 0 arcn
  O2 moveto r1 0 rmoveto
  O2 r1 360 0 arcn
  O3 moveto r1 0 rmoveto
  O3 r1 360 0 arcn
} def
%
/makeSpinner {
  1 setlinecap
  /r1 1.1 cm def
  /ri 0.4 cm def
  /a1 R1 3 div r1 sub def
  /rho R1 r1 sub a1 sub def
  /r2 2 r1 mul a1 mul 3 a1 dup mul mul add rho dup mul add rho r1 a1 2 mul add mul sub
   rho 2 a1 mul sub div  def
  /rho2 r2 r1 add 2 a1 mul add def
  /alpha1 rho rho2 2 div sub rho2 3 sqrt mul 2 div div arctan def
  /beta1 rho rho2 add neg 3 sqrt rho2 rho sub mul div arctan def
  /alpha2 rho 2 div neg rho2 add 3 sqrt 2 div rho mul neg div arctan def
  /A {0 R1} def
  /B {R1 3 sqrt mul -2 div R1 -2 div} def
  /C {R1 3 sqrt mul 2 div R1 -2 div} def
  /O1 {0 rho} def
  /O2 {rho 3 sqrt mul -2 div rho -2 div} def
  /O3 {rho 3 sqrt mul 2 div rho -2 div} def
  /A' {rho2 3 sqrt mul 2 div neg  rho2 2 div} def
  /B' {rho2 3 sqrt mul 2 div    rho2 2 div} def
  /C' {0 rho2 neg} def
  gsave
  spinnerROT rotate
  gsave
  TripleSpinner
  clip
  ifPst@customize { spinnerImage }{ spinnerFillColor fill } ifelse
  grestore
  TripleSpinner
  spinnerLineColor
  spinnerLW SLW
  stroke
  {color1} {O1} BallBearing
  {color2} {O2} BallBearing
  {color3} {O3} BallBearing
  {color0} {0 0} BallBearing
  grestore
  ifPst@mask {
    ifPst@customizeMask {
      gsave
      newpath
      r1 0 moveto
      0 0 r1 0 360 arc
      closepath
      clip
      spinnerImage
      grestore 
    }{
      newpath
      0 0 r1 0 360 arc
      colorMask
      fill
    } ifelse
    0 0 r1 0 360 arc
    0.5 setlinewidth
    0 setgray
    stroke
  } if
} def  % makeSpinner
%
end
%%
%% end 