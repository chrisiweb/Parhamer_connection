%% $Id: pst-fractal.pro 679 2017-12-04 21:41:23Z herbert $
%%
%% This is file `pst-fractal.pro',
%%
%% IMPORTANT NOTICE:
%%
%% Package `pst-fractal'
%%
%% Herbert Voss <voss _at_ PSTricks.de>
%%
%% This program can be redistributed and/or modified under the terms
%% of the LaTeX Project Public License Distributed from CTAN archives
%% in directory macros/latex/base/lppl.txt.
%%
%% DESCRIPTION:
%%   `pst-fractal' is a PSTricks package to draw fractal objects
%%
%%
%% version 0.07 / 2022-10-13  Herbert Voss <hvoss _at_ tug.org>
%
/tx@fractalDict 100 dict def
tx@fractalDict begin
%
/tx@Fractal {
%    \pst@temp@A 
%    \pst@temp@B 
%    \pst@number\pst@fractal@xWidth
%    \pst@number\pst@fractal@yWidth
%    \pst@fractal@cx 
%    \pst@fractal@cy  
%    \pst@fractal@maxIter
%    \pst@fractal@dIter
%    \pst@fractal@maxRadius
%    {\pst@usecolor\pst@fractal@baseColor} 
%    \ifx\pst@fractal@type\pst@fractal@Julia true \else false \fi
%    \ifPst@CMYK true \else false \fi
%    tx@fractalDict begin tx@Fractal end
  /ifCMYK ED
  /ifJulia ED
  /baseColor ED
  /maxRadius ED
  /dIter ED
  /maxIter ED
  /cy ED 
  /cx ED
  /MaxYPixel ED
  /MaxXPixel ED
  /MaxY ED /MaxX ED
  /MinY ED /MinX ED
  /rPixel 1 def
  /totMaxIter maxIter dIter mul def
%
  /DX MaxX MinX sub def
  /DY MaxY MinY sub def
  /dx DX MaxXPixel div def /dy DY MaxYPixel div def
%
  /convertX { MinX sub DX sub dx div } def % user -> pt
  /convertY { MinY sub dy div } def        % user -> pt
  /convertXY { convertY exch convertX exch } def
%
  /putPixel {%  x y auf dem Stack in Benutzerkoordinaten
    convertXY
    rPixel 0 360 arc fill 
  } def
%
  MinX dx MaxX {
    ifJulia { /x exch def }{ /cx exch def /x 0.0 def } ifelse
    MinY dy MaxY {
      ifJulia { /y exch def }{ /cy exch def /y 0.0 def } ifelse
      /iter 0 def
      /z [x y] def
      /c [cx cy] def
      /plot true def
      totMaxIter cvi {
         z cxnorm2 maxRadius gt {
         /plot false def 
         exit
        }{% Calculate next value
%           z 5 cxexp c add
%           z dup cxmul c cxadd 
	    z FractalFunc
          /z ED
	  /iter iter dIter add def
        } ifelse
      } repeat
      plot{ 
        baseColor x y putPixel 
      }{ iter 400 add  
	 ifCMYK { tx@addDict begin wavelengthToCMYK Cyan Magenta Yellow Black end setcmykcolor 
	 }{ tx@addDict begin wavelengthToRGB Red Green Blue end setrgbcolor } ifelse 
         ifJulia { x y }{ cx cy } ifelse
	 putPixel stroke 
      }ifelse   % Plot point if point is in set
    } for
  } for
} def
%
/tx@Sierpinski { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    \pst@temp@A 
%    \pst@temp@B 
%    \pst@temp@C  
%    { \pst@usecolor\pslinecolor }
%    \pst@fractal@plotpoints
20 dict begin
  /plotpoints ED
  /setColor ED
  /Coor ED   
  /Sx 0 def /Sy 0 def
  /putPixel {	0.5 0 360 arc stroke } def % x y on stack
  /newPosition {			% point # on stack
    Coor exch 2 getinterval aload pop 
    /y exch def  /x exch def 
    x Sx sub 2 div Sx add /Sx exch def 
    y Sy sub 2 div Sy add /Sy exch def
    Sx Sy putPixel 
  } def
  /drawFrame {
    Coor aload pop
    newpath
    moveto
    nCoor 1 sub { lineto } repeat % n-1 times
    gsave 0.9 setgray fill grestore 
    setColor
    closepath
    stroke 
  } def
  /nCoor Coor length 2 div 0.5 add cvi def % # of dots
  drawFrame
  plotpoints cvi {
    rand nCoor mod 
    dup add newPosition   
  } repeat
end
} def
%
/Rot-90 {
  2 dict begin
  /y exch def /x exch def
  y
  x neg
  end
} def
%
/tx@SierpinskiCurve { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%25 dict begin
  /Pi [1.5 cmunit 1 cmunit
     1 cmunit 0.5 cmunit
     1 cmunit -0.5 cmunit
     1.5 cmunit -1 cmunit ] def
%
  /P0 Pi def
  /coefficient 1 def
  3 {
    P0
    [
      0 2 Pi length 2 sub {/i exch def
        Pi i get Pi i 1 add get exch neg % Rot-90
      } for
    ]  /Pi exch def
    P0 Pi concatarray /P0 exch def
  } repeat
%
/P1 {[
  0 2 P0 length 2 sub {/i exch def
    P0 i get P0 i 1 add get % Rot-90
    -2 cmunit coefficient mul add exch
    -2 cmunit coefficient mul add exch
  } for
] } def
%
/P2 {[
  0 2 P0 length 2 sub {
    /i exch def
    P0 i get P0 i 1 add get exch neg % Rot-90
    2 cmunit coefficient mul add exch
   -2 cmunit coefficient mul add exch
   } for ]
} def
%
/P3 {[
  0 2 P0 length 2 sub {
    /i exch def
    P0 i get P0 i 1 add get neg exch neg exch % Rot-90 Rot-90
    2 cmunit coefficient mul add exch
    2 cmunit coefficient mul add exch
  } for
] } def
%
/P4 {[
   0 2 P0 length 2 sub {/i exch def
     P0 i get P0 i 1 add get neg exch % Rot-90 Rot-90 Rot-90
     -2 cmunit coefficient mul add exch
     2 cmunit coefficient mul add exch
   } for
] } def
  n@ 1 eq {/Sierpinsky P0 def}{
      n@ 1 sub {
        /Sierpinsky P1 P2 concatarray P3 concatarray P4 concatarray def
    /Tab1 [
      0 2 Sierpinsky length 2 sub {/i exch def
        Sierpinsky i 2 getinterval
      } for
    ] def
    /i@ Sierpinsky length 8 div 2.5 mul cvi def %
    /Sierpinsky2 [
      Tab1 length {
        Tab1 i@ get
        /i@ i@ 1 add def
        i@ Tab1 length ge {/i@ 0 def} if
      }repeat
    ] def
    /P0 [
      0 1 Sierpinsky2 length 1 sub {/i exch def
        Sierpinsky2 i get aload pop
      } for
    ] def
    /coefficient coefficient 2 mul def
    } repeat    
  } ifelse
%
    newpath
    Sierpinsky 0 get Sierpinsky 1 get moveto
      0 2 Sierpinsky length 2 sub {/i exch def
      i 2 div Npts ge {exit} if
      Sierpinsky i get Sierpinsky i 1 add get lineto
    } for
    Npts 4 n@ 1 add exp cvi ge { closepath } if
    useFill { gsave fillColor fill grestore } if 
%
    useLineStyle
%end
} def 
%
/tx@Phyllotaxis { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
%	\pst@tempA 
%	\pst@fractal@c 
%	\pst@fractal@angle 
%	\pst@fractal@maxIter CMYK
10 dict begin
  /ifCMYK ED
  /maxIter ED
  /fractalAngle ED
  /c ED
  translate
  /angle fractalAngle dup 0 eq { pop 360 5 sqrt 1 add 2 div dup mul div } if def
  maxIter cvi -1 0 {
    angle rotate
    0 0 moveto
    dup sqrt c mul c lineto
    c c neg rlineto
    c neg dup rlineto
    closepath
    gsave
      1 exch maxIter cvi div 90 mul cos 0 
      ifCMYK { tx@addDict begin RGBtoCMYK end setcmykcolor }{ setrgbcolor } ifelse
      fill
    grestore
    stroke
  } for
end
} def
%
/tx@Fern { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    \pst@fractal@scale 
%    \pst@tempA 
%    \pst@fractal@maxIter
%    \pst@fractal@radius
%    \pst@number\pslinewidth
%    { \pst@usecolor\pslinecolor }
20 dict begin
  /setColor ED
  SLW
  /radius ED
  /maxIter ED  
  translate
  dup scale
  /m1 [  0.00  0.00  0.00  0.16  0.00 0.00 ] def
  /m2 [  0.85 -0.04  0.04  0.85  0.00 1.60 ] def
  /m3 [  0.20  0.23 -0.26  0.22  0.00 1.60 ] def
  /m4 [ -0.15  0.26  0.28  0.24  0.00 0.44 ] def
  1 setlinecap
  setColor
  0 0 % start point
  maxIter cvi {
  % get a transformation matrix probabilistically
  /r rand 100 mod def
  r  1 lt { /m m1 def }{ r 86 lt 
    { /m m2 def }{ r 93 lt { 
      /m m3 def }{ /m m4 def } ifelse } ifelse } ifelse
  % Make a linear transformation, then
  % plot a point at current location
   m transform 2 copy radius 0 360 arc
   stroke
  } repeat
end
} def
%
/tx@Kochflake { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    \pst@tempA
%    { \pst@usecolor\pslinecolor }
%    \pst@fractal@scale
%    \pst@fractal@angle
%    CLW
%    \pst@fractal@maxIter
  /maxIter ED
  10 10 scale
  45 rotate
  /side {
    dup 0 gt { 
      1 sub 1 3 div dup scale side 60 rotate side 
      -120 rotate side 60 rotate side 3 dup scale 1 add
    }{ 1 1 rlineto 1 1 translate } ifelse 
  } def
  /star { 
    dup currentlinewidth 1 1 
    4 -1 roll { pop 3 div } for 
    setlinewidth
    0 0 moveto 
    side -120 rotate side -120 rotate side
    pop
    closepath
  } def
  maxIter star
} def
%
/tx@Appolonius { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%    \pst@fractal@dIter
%    \pst@number\pst@fractal@Radius
%    \ifPst@fractal@Color true \else false \fi
%    \ifPst@CMYK true \else false \fi
%    gsave
%    \pst@tempA translate
%    \pst@usecolor\pslinecolor
%    \pst@fractal@scale
%    \pst@number\pslinewidth SLW
%
30 dict begin
  /ifCMYK ED
  /ifColor ED
  /Radius ED
  /dIter ED
  /icount 380 def
  /setWaveColor {
    /icount icount dup 780 gt { pop 380 }{ dIter add } ifelse def
    tx@addDict begin icount 
    ifCMYK { wavelengthToCMYK Cyan Magenta Yellow Black end setcmykcolor 
    }{ wavelengthToRGB Red Green Blue end setrgbcolor } ifelse 
  } def
  /collect { [ 4 1 roll ] } def
  /nget { exch dup 3 1 roll exch get } def
  /polydup { 1 add [ exch 1 roll ] aload aload pop } def
  /circle { aload pop newpath 0 360 arc closepath 
    ifColor { gsave setWaveColor fill grestore } if
    stroke } def
  /inverse {
     aload 4 1 roll 3 1 roll dup mul exch dup mul add exch dup mul sub
     dup 0 eq not {1 exch div} if
     exch
     aload pop
     4 -1 roll dup 5 1 roll mul 3 1 roll
     4 -1 roll dup 5 1 roll mul 3 1 roll
     4 -1 roll dup 5 1 roll mul 3 1 roll
     4 -1 roll pop
     dup 0 lt {neg} if
     collect
  } def
  /between {
     collect
     0 nget 2 get exch 1 nget 2 get exch 3 1 roll
     lt {aload pop 3 1 roll exch 3 -1 roll collect} if
     0 nget 2 get exch 2 nget 2 get exch 3 1 roll
     lt {aload pop 3 -1 roll exch 3 1 roll collect} if
     1 nget 0 get exch 2 nget 2 get exch
     2 nget 0 get exch 1 nget 2 get exch
     1 nget 2 get exch 2 nget 2 get exch
     7 1 roll add 5 1 roll mul 3 1 roll mul add exch div
     /xdisp exch def
     1 nget 1 get exch 2 nget 2 get exch
     2 nget 1 get exch 1 nget 2 get exch
     1 nget 2 get exch 2 nget 2 get exch
     7 1 roll add 5 1 roll mul 3 1 roll mul add exch div
     /ydisp exch def
     0 nget aload pop 3 1 roll ydisp sub 3 1 roll xdisp sub 3 1 roll
     collect
     inverse dup
     /first exch def
     /second exch def
     1 nget 1 get exch 2 nget 1 get exch 3 1 roll sub /xvect exch def
     2 nget 0 get exch 1 nget 0 get exch 3 1 roll sub /yvect exch def
     xvect dup mul yvect dup mul add sqrt
     dup 0.0 eq not { first 2 get 2 mul exch div} if
     dup xvect mul /xvect exch def
     yvect mul /yvect exch def
     first aload pop 3 1 roll yvect add 3 1 roll xvect add 3 1 roll
     collect
     inverse /first exch def
     second aload pop 3 1 roll yvect sub 3 1 roll xvect sub 3 1 roll
     collect
     inverse /second exch def
     first second
     first 2 get second 2 get sub
     0 gt { exch } if
     pop
     aload pop
     3 1 roll ydisp add 3 1 roll xdisp add 3 1 roll collect
     exch pop
  } def
  /appol {
     aload pop 3 polydup between
     dup circle
     2 nget CLW gt { 1 1 3 { pop 3 polydup collect 5 1 roll 4 -1 roll } for } if
     pop pop pop pop
  } def
  /inside {
     /temp exch def
     0 120 240 {
          /angle exch def
          temp aload pop
          3 sqrt 2 div 1 add div
          /radius exch def
          angle sin radius mul
          angle cos radius mul
          exch 4 -1 roll add
          3 1 roll add
          radius 3 sqrt 2 div mul
          collect
     } for
  } def
%
  [ 0 0 Radius ] dup inside 4 polydup
  1 1 4 { pop circle } for
  1 1 4 { pop 3 polydup collect 5 1 roll 4 1 roll } for
  pop pop pop pop { count 0 eq { exit } if appol } loop
end
} def
%
/tx@Hugo { %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%Creator: Hugo M. Ayala'89, MIT
%    \pst@fractal@scale 
%    \pst@tempA 
%    \pst@fractal@maxIter, which is the depth
%    \pst@number\pslinewidth
%    { \pst@usecolor\pslinecolor }
50 dict begin
/setColor ED
SLW
/depth ED  
translate
dup scale
2 setlinecap
setColor
%
/oldarrayx [0 540 72 72] def
/oldarrayy [0 396 720 72] def
%
/scl .1 def
%
realtime srand
/prorand { rand 32768 div 32768 div 1 sub scl mul} def
/findrow {8 mul 7 sub sqrt 1 add 2 div truncate} def
/findindex {dup 1 sub mul 2 div 1 add} def
/findcolumn {dup findrow findindex sub} def
/findnewrow {2 mul 1 sub} def
/findnewcolumn {2 mul} def
/findarraysize {dup 1 add mul 2 div 1 add} def
/findnumoflines {dup 1 sub mul 2 div 3 mul} def
/findnumpoints {dup 1 add mul 2 div} def
/gtol {2 exch exp 1 add} def
/fixangle {dup 180 ge {180 sub} if} def
/backangle {dup 180 ge {180 sub} {180 add} ifelse} def
/splitline { 
  tpx btx add 2 div /mdx exch def
  tpy bty add 2 div /mdy exch def
  tpy bty sub tpx btx sub atan
  90 add fixangle
  /lineangle exch def
  tpy bty sub dup mul
  tpx btx sub dup mul
  add sqrt /linelen exch def
  prorand linelen mul dup
  lineangle cos mul mdx add /mdx exch def
  lineangle sin mul mdy add /mdy exch def
} def
%
/findnewindex{ cvi /oldindex exch def
  oldindex findrow cvi dup /oldrow exch def
  findindex oldindex exch sub cvi /oldcolumn exch def
  oldrow findnewrow cvi dup /newrow exch def findindex
  oldcolumn findnewcolumn cvi dup /newcolumn exch def add
  cvi /newindex exch def
} def
%
/drawfractal {
  1 1 generation gtol 1 sub findnumpoints {
    cvi /topindex exch def
    topindex dup findcolumn exch findrow 1 add findindex add cvi
    /leftindex exch def
    leftindex 1 add cvi 
    /rightindex exch def
    /tpx oldarrayx topindex get def
    /tpy oldarrayy topindex get def
    /btx oldarrayx leftindex get def
    /bty oldarrayy leftindex get def
    /mdx oldarrayx rightindex get def
    /mdy oldarrayy rightindex get def
    tpx tpy moveto
    btx bty lineto
    mdx mdy lineto
    closepath stroke 
  } for
} def
%
1 1 depth {
  /generation exch def
  generation gtol findarraysize cvi dup array /newarrayx exch def
  array /newarrayy exch def
  1 1 generation 1 sub gtol findnumpoints {
    findnewindex
    newarrayx newindex
    oldarrayx oldindex get put
    newarrayy newindex
    oldarrayy oldindex get put
  } for
  1 1 generation 1 sub gtol 1 sub findnumpoints {
     findnewindex
     newcolumn newrow 2 add findindex add cvi dup
     /leftindex exch def 
     2 add cvi /rightindex exch def
     newcolumn newrow 1 add findindex add cvi
     /mindex exch def
     /tpx newarrayx newindex get def
     /tpy newarrayy newindex get def
     /btx newarrayx leftindex get def
     /bty newarrayy leftindex get def
     splitline
     newarrayx mindex mdx put
     newarrayy mindex mdy put
     mindex 1 add cvi /mindex exch def
     /btx newarrayx rightindex get def
     /bty newarrayy rightindex get def
     splitline
     newarrayx mindex mdx put
     newarrayy mindex mdy put
     /mindex leftindex 1 add cvi def
     /tpx newarrayx leftindex get def
     /tpy newarrayy leftindex get def
     splitline
     newarrayx mindex mdx put
     newarrayy mindex mdy put 
   } for
   /oldarrayx newarrayx def
   /oldarrayy newarrayy def
   7 generation sub 5 div setlinewidth
%   drawfractal showpage 
} for 
drawfractal  
end
} def  % end of /tx@Hugo
%
/FibonacciFractal {
  20 dict begin
  n@ 2 sub {
	/Fi F2 F1 concatstrings def
	/F1 F2 def
	/F2 Fi def
      } repeat
    /S Fi def
    /nS S length def % nombre de lettres
    0 1 nS 2 sub {/j exch def
      x1 y1 translate
      /x0 0 def /y0 0 def
      /k S j 1 getinterval cvi def
      k 0 eq {
	j 2 mod 0 eq {
          angle neg rotate
          tx  ty lineto
          currentpoint /y1 exch def /x1 exch def
          /flag 0 def
        }{
          angle rotate
          tx ty lineto
          currentpoint /y1 exch def /x1 exch def
          /flag 1 def
        } ifelse
      }{
	tx ty lineto
	currentpoint /y1 exch def /x1 exch def
	/flag 2 def
      } ifelse
    } for
    setLineColor
    stroke
    Pst@juxtaposition {
    x1 y1 translate
    flag 1 eq {-1 1 scale} if
    flag 2 eq {90 rotate 1 -1 scale } if
    0 0 moveto
    /x0 0 def /y0 0 def
    /F1 (1) def
    /F2 (0) def
    /x1 0 def /y1 1 cmunit def
    x1 y1 lineto
    n@ 3 sub{
      /Fi F2 F1 concatstrings def
      /F1 F2 def
      /F2 Fi def
    } repeat
    /S Fi def
    /nS S length def % nombre de lettres
    0 1 nS 2 sub {/j exch def
      x1 y1 translate
      /x0 0 def /y0 0 def
      /k S j 1 getinterval cvi def
      k 0 eq {
	j 2 mod 0 eq {
          -90 rotate
          tx  ty lineto
          currentpoint /y1 exch def /x1 exch def
        }{
          90 rotate
          tx ty lineto
          currentpoint /y1 exch def /x1 exch def
        } ifelse
      }{
	tx ty lineto
	currentpoint /y1 exch def /x1 exch def
      } ifelse
    } for
    ColorF
    stroke
    } if % end Pst@juxtaposition
    end
} def
%
/newFibonacciFractal {
  20 dict begin
  n@ 2 sub {
    /Fi F2 F1 concatstrings def
    /F1 F2 def
    /F2 Fi def
  } repeat
  % The Dense Fibonacci Word
  /DFW () def
  0 2 F2 length 2 sub {
    /i exch def
    /I F2 i 2 getinterval def
    I (00) eq {DFW (0) concatstrings /DFW  exch def } if
    I (01) eq {DFW  (1) concatstrings /DFW  exch def } if
    I (10) eq {DFW  (2) concatstrings /DFW  exch def } if
  } for
% morphismes
% newFibonacci
% 0->"", 1->1, 2->2
  /F2 DFW def
  /Fi () def
  0 1 F2 length 1 sub {
    /i exch def
    /I F2 i 1 getinterval def
    I (0) eq {Fi m@0 concatstrings /Fi exch def} if
    I (1) eq {Fi m@1 concatstrings /Fi exch def} if
    I (2) eq {Fi m@2 concatstrings /Fi exch def} if
  } for
  /S Fi def
  /nS S length def % nombre de lettres
  0 1 nS 1 sub {
    /j exch def
    x1 y1 translate
    /x0 0 def /y0 0 def
    /k S j 1 getinterval cvi def
    k 1 eq {angle neg rotate
      tx  ty lineto
      currentpoint /y1 exch def /x1 exch def
    } if
    k 2 eq { angle rotate
      tx  ty lineto
      currentpoint /y1 exch def /x1 exch def
    } if
    k 0 eq {
      tx  ty lineto
      currentpoint /y1 exch def /x1 exch def
    } if
  } for
  setLineColor
  stroke
  end
} def
%
/i-FibonacciFractal {
  20 dict begin
  /F0 (0) def
  /Fi () def
  i@ 1 sub { 
    Fi (0) concatstrings /Fi exch def
  } repeat
  Fi (1) concatstrings
  /F1 exch def
  n@ {
    F1 F0 concatstrings
    /Fi exch def
    /F0 F1 def
    /F1 Fi def
  } repeat
  /S Fi def
  0 0 translate
  0 0 moveto
  currentpoint /y0 exch def /x0 exch def
  0 1 cmunit lineto
  currentpoint /y1 exch def /x1 exch def
  /tx {x1 x0 sub} def
  /ty {y1 y0 sub} def
%
  /nS S length def % nombre de lettres
  0 1 nS 2 sub {
    /j exch def
    x1 y1 translate
    /x0 0 def /y0 0 def
  /k S j 1 getinterval cvi def
  k 0 eq {
    j 2 mod 0 eq {
              angle neg rotate
              tx  ty lineto
              currentpoint /y1 exch def /x1 exch def
    }{
              angle rotate
              tx ty lineto
              currentpoint /y1 exch def /x1 exch def
    } ifelse
  }{
    tx ty lineto
    currentpoint /y1 exch def /x1 exch def
   } ifelse
  } for
  setLineColor
  stroke
  end
} def
%
/k-FibonacciFractal {
  20 dict begin
  /f0 (0) def
  /fi (0) def
  k@ 2 sub {
    fi (0) concatstrings /fi exch def
  } repeat
  fi (1) concatstrings
  /f1 exch def
  /fi f1 def
  n@ 1 sub {
    k@ 1 sub { f1 fi concatstrings /f1 exch def } repeat
    f1 f0 concatstrings /f1 exch def
     /f0 fi def
    /fi f1 def
  } repeat
  /S f1 def
  t@x cmunit_1 28.45 mul t@y cmunit_1 28.45 mul translate
  0 0 moveto
  currentpoint /y0 exch def /x0 exch def
  0 1 cmunit lineto
  currentpoint /y1 exch def /x1 exch def
  /tx {x1 x0 sub} def
  /ty {y1 y0 sub} def
  /nS S length def % nombre de lettres
  0 1 nS 1 sub {/j exch def
  x1 y1 translate
  /x0 0 def /y0 0 def
  /k S j 1 getinterval cvi def
  k 0 eq {
  j 2 mod 0 eq {
              angle neg rotate
              tx  ty lineto
              currentpoint /y1 exch def /x1 exch def
              }
             {
              angle rotate
              tx ty lineto
              currentpoint /y1 exch def /x1 exch def
              }
             ifelse
} {
    tx ty lineto
    currentpoint /y1 exch def /x1 exch def
    } ifelse
  } for
  setLineColor
  stroke
  end
} def
%
/Biperiodic-FibonacciWords {
  20 dict begin
/f0 () def
/f1 (0) def
/f2 a@ 1 sub {(0) f0 concatstrings /f0 exch def} repeat f0 (1) concatstrings def
3 1 n@ {/i exch def
/fi () def
i 2 mod 0 eq {
 a@ { fi f2 concatstrings /fi exch def } repeat
 }{
 b@ { fi f2 concatstrings /fi exch def } repeat
 } ifelse
 fi f1 concatstrings /fi exch def
 /f1 f2 def
 /f2 fi def
} for
/S f2 def
t@x cmunit_1 28.45 mul t@y cmunit_1 28.45 mul translate
0 0 moveto
currentpoint /y0 exch def /x0 exch def
1 cmunit 0 cmunit lineto
currentpoint /y1 exch def /x1 exch def
/tx {x1 x0 sub} def
/ty {y1 y0 sub} def
/nS S length def % nombre de lettres
0 1 nS 1 sub {/j exch def
x1 y1 translate
/x0 0 def /y0 0 def
/k S j 1 getinterval cvi def
k 0 eq {
j 2 mod 0 eq {
              angle neg rotate
              tx  ty lineto
              currentpoint /y1 exch def /x1 exch def
              }
             {
              angle rotate
              tx ty lineto
              currentpoint /y1 exch def /x1 exch def
              }
             ifelse
} {
tx ty lineto
currentpoint /y1 exch def /x1 exch def
} ifelse
} for
    setLineColor
stroke
end
 }def
%
/InverseLR {
      1 dict begin
	/str exch def
	0 1 str length 1 sub {/i exch def
	  str i 1 getinterval (L) eq {str i (R) putinterval }{str i (L) putinterval }ifelse
	} for
	str
      end
} def
%
/FibonacciPolyominoes {
  20 dict begin
  gsave
  t@x  t@y translate
  /q0 () def
  /q1 (R) def
  /N n@ 3 mul 1 add def
  2 1 N {
    /n exch def
    n 3 mod 2 eq {/qi q1 q0 concatstrings def}
               {/qi q1 q0 InverseLR concatstrings def} ifelse
    /q0 q1 def
    /q1 qi def
  } for
  /q_1 q1 reversestring def
  /qii () def
  /Q 3 {qii q1 concatstrings /qii exch def } repeat 
    qii q_1 reversestring concatstrings def
% remarque
% identique /Q 4{qii q1 concatstrings /qii exch def} repeat qii def
  /tx {x1 x0 sub} def
  /ty {y1 y0 sub} def
  /y0 0 def /x0 0 def
  /x1 x0 0 cmunit add def /y1 y0 1 cmunit add def
  newpath
  x0 y0 moveto
  x1 y1 lineto
  0 1 Q length 1 sub {/i exch def
         x1 y1 translate
  Q i 1 getinterval (L) eq {
         90  rotate
         tx  ty lineto
         currentpoint /y1 exch def /x1 exch def
         }{
         90 neg rotate
         tx  ty lineto
         currentpoint /y1 exch def /x1 exch def
         }ifelse
       } for
  closepath
  setFillColor
  setLineColor
  grestore
  end
} def
%
/Rot2 { % Rot-90+translation
     2 dict begin
     /y exch neg def /x exch def
     y 2 n@ 1 add exp 1 sub add
     x neg 2 n@ exp 1 sub add
     end
   } def
/Trans1 {
  2 dict begin
  /y exch def /x exch def
  x
  y 2 n@ exp add
  end
} def
/Trans2 {
  2 dict begin
  /y exch def /x exch def
  x 2 n@ exp add
  y 2 n@ exp add
  end
} def
%
/HilbertFractal {
  /M0 [[0 0]  [0 1] [1 1] [1 0]] def
  /n@ 1 def
  N@ {
    /M1 [] def
    /M2 [] def
    /M3 [] def
    /M4 [] def
    0 1 M0 length 1 sub {/i exch def
    /M M0 i get def
    /Mt [
      0 2 M length 2 sub {
        /k exch def
        M k 2 getinterval
      } for
    ] def
    M1 [Mt {aload pop exch  } forall] concatarray /M1 exch def
    M2 [Mt {aload pop Trans1} forall] concatarray /M2 exch def
    M3 [Mt {aload pop Trans2} forall] concatarray /M3 exch def
    M4 [Mt {aload pop Rot2  } forall] concatarray /M4 exch def
    } for
    /n@ n@ 1 add def
    /M0 [M1 M2 M3  M4] def
  } repeat
% tableau des points
  /HilbertCurve [
    0 1 M0 length 1 sub {
      /i exch def
      /lePt M0 i get def
      0 2 lePt length 2 sub {
        /j exch def
	lePt j get cmunit
	lePt j 1 add get cmunit
      } for
    } for
  ] def
% le dessin de la courbe
  newpath
  0 0 moveto
  0 2 HilbertCurve length 2 sub {
    /i exch def
    i 2 div Npts ge {exit} if
    HilbertCurve i get
    HilbertCurve i 1 add get
    lineto
  } for
} def
%
end