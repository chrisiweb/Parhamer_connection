%% $Id: pst-bezier.pro 323 2016-08-20 17:57:28Z herbert $
%% PostScript prologue for pst-bezier.tex.
%%
%% Version 0.02, 2016/08/19
%%
%% For distribution, see pst-bezier.tex.
%%
%% 
tx@Dict begin
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Auxiliary routines:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%% [x1 y1] [x2 y2] -> [ x1+y1  x2+y2 ]
/AddArrays2d {
    [ 3 1 roll %% Get the operands
    2 copy
    0 get exch
    0 get add %% first component finished
    %% second component:
    3 1 roll
    1 get exch
    1 get add ]} bind def

%% [x1 y1] [x2 y2] -> [ x1-x2  y1-y2 ]
/SubArrays2d {
    [ 3 1 roll exch
    2 copy
    0 get exch 0 get sub
    3 1 roll
    1 get exch
    1 get sub ] } bind def

%% [x y] s -> [s*x s*y]
/ScaleArray2d {
    [ 3 1 roll exch
    2 copy
    0 get mul
    3 1 roll
    1 get mul
    ] } bind def
%
%% << [Array of Bezier splines] /K 1 >> -> empty stack
%% Thereby, a Bezier spline is described by an array:
%% [x0 y0 x1 y1 x2 y2 x3 y3 sl sr]
%% (x0,y0) is the right control point
/pstBCurve {
begin %% LaTeX provides the dictionary (see above comments)
    1 1 Splines length 1 sub {
        /K exch def % K is the index of the spline.
%%
	%% First control point:
        Splines K get 0 get dup %% switch the cases /n and /s...
	/n eq { %% `not specified' -> automatically computed
            Splines K get 0 %% l(k) is going to be set...
		%% | -> p(k-1)+(p(k)-p(k-2))*sl(k)
                Splines K get 4 2 getinterval
                Splines K 2 sub get 4 2 getinterval
                SubArrays2d
                Splines K get 6 get ScaleArray2d
                Splines K 1 sub get 4 2 getinterval
                AddArrays2d
            putinterval %% ...setting l(k)
        } if
        /s eq { %% `symmetric' -> compute from r(k-1)
            Splines K get 0 %% l(k):=
		%% | -> 2*p(k-1)-r(k-1)
                Splines K 1 sub get 4 2 getinterval 2 ScaleArray2d
                Splines K 1 sub get 2 2 getinterval SubArrays2d
            putinterval %%
        } if
	%% Second control point:
        Splines K get 2 get dup %% (cases /n and /s)
	/n eq { %% `not specified' -> automatically computed
            Splines K get 2
		%% | -> p(k)+(p(k+1)-p(k-1))*sr(k)
                Splines K 1 sub get 4 2 getinterval
                Splines K 1 add get 4 2 getinterval
                SubArrays2d
                Splines K get 7 get ScaleArray2d
                Splines K get 4 2 getinterval
                AddArrays2d
            putinterval
        } if
        /s eq { %% `symmetric' -> compute from l(k+1)
            Splines K get 2
		%% | -> 2*p(k)-l(k+1)
                Splines K get 4 2 getinterval 2 ScaleArray2d
                Splines K 1 add get 0 2 getinterval SubArrays2d
            putinterval
        } if
    } for %% all splines.
    %%
    %% The current point is already correctly set by the LaTeX macro.
    %% So get ride of the 0th dummy spline.
    Splines 1 Splines length 1 sub getinterval {%
	aload pop pop pop %% get ride of the array itself and the scaling factor.
       curveto% now the actual spline is on the stack...
    } forall %% splines.
    /Points [ %% now save the points for the showpoints-feature.
        Splines 0 get 4 2 getinterval aload pop
        Splines 1 Splines length 1 sub getinterval { aload pop pop pop } forall
        ]
    end def %% Put points in the top dictionary
  } bind def
%
/tx@RQBCmasse {
   /P0P1{
      xP0 xP1 add
      yP0 yP1 add
    } def
    /P0P2{
      xP0 xP2 add
      yP0 yP2 add
    } def
    /P1P2{
      xP2 xP1 add
      yP2 yP1 add
    } def
    /B0 { 1 t sub dup mul } def
    /B1 {2 t mul 1 t sub mul }def
    /B2 { t dup mul }def
%
%  w0 abs 1e-6 gt {1}{0} ifelse /choixw0 exch def
%  w1 abs 1e-6 gt {1}{0} ifelse /choixw1 exch def
%  w2 abs 1e-6 gt {1}{0} ifelse /choixw2 exch def
%  /choix choixw2 4 mul choixw1 2 mul add choixw0 add def
   choix 1 eq {
       /den { w0 B0 mul }def %
       /RQBCmasse1 {
        0 1 nB {/t exch nB div def
       den 0 ne {
        w0 B0 mul xP0 mul B1 xP1 mul add B2 xP2 mul add den div
        w0 B0 mul yP0 mul B1 yP1 mul add B2 yP2 mul add den div
             } if
        } for
        } def
        /RQBCmasse2 {} def
        } if % fin choix 1
 choix 2 eq {
       /den {w1 B1 mul } def %
       /RQBCmasse1 {
        1 1 nB {/t exch nB div def
       den 0 ne {% B0*P0+w1*B1*P1+B2*P2
        B0 xP0 mul w1 B1 mul xP1 mul add B2 xP2 mul add den div
        B0 yP0 mul w1 B1 mul yP1 mul add B2 yP2 mul add den div
             } if
        } for
        } def
        /RQBCmasse2 {} def
        } if % fin choix 2
 choix 3 eq {
       /den { w0 B0 mul w1 B1 mul add } def % w0*B0+w1*B1
       /RQBCmasse1 {
        0 1 nB {/t exch nB div def
       den  1e-6 gt { % w0*B0*P0+w1*B1*P1+B2*P2
        w0 B0 mul xP0 mul w1 B1 mul xP1 mul add B2 xP2 mul add den div
        w0 B0 mul yP0 mul w1 B1 mul yP1 mul add B2 yP2 mul add den div
             } if
        } for
        } def
        /RQBCmasse2 {
        0 1 nB {/t exch nB div def
       	den  -1e-6 lt { % w0*B0*P0+w1*B1*P1+B2*P2
        w0 B0 mul xP0 mul w1 B1 mul xP1 mul add B2 xP2 mul add den div
        w0 B0 mul yP0 mul w1 B1 mul yP1 mul add B2 yP2 mul add den div
             } if
        } for
        } def
        } if % fin choix 3
  choix 4 eq {
       /den { w2 B2 mul } def % w2*B2
       /RQBCmasse1 {
        0 1 nB {/t exch nB div def
       den 0 ne { % B0*P0+B1*P1+w2*B2*P2
        B0 xP0 mul B1 xP1 mul add w2 B2 mul xP2 mul add den div
        B0 yP0 mul B1 yP1 mul add w2 B2 mul yP2 mul add den div
             } if
        } for
        } def
        /RQBCmasse2 {} def
        } if % fin choix 4
  choix 5 eq {
       /den {w0 B0 mul w2 B2 mul add} def % w0*B0+w2*B2
       /RQBCmasse1 {
        1 1 nB {/t exch nB div def
       den 0 ne { % w0*B0*P0+B1*P1+w2*B2*P2
        w0 B0 mul xP0 mul B1 xP1 mul add w2 B2 mul xP2 mul add den div
        w0 B0 mul yP0 mul B1 yP1 mul add w2 B2 mul yP2 mul add den div
             } if
        } for
        } def
       /RQBCmasse2 {} def
        } if % fin choix 5
  choix 6 eq {
       /den { w1 B1 mul w2 B2 mul add } def % w1*B1+w2*B2
       /RQBCmasse1 {
        0 1 nB {/t exch nB div def
       	den  1e-6 gt  { % B0*P0+w1*B1*P1+w2*B2*P2
        B0 xP0 mul w1 B1 mul xP1 mul add w2 B2 mul xP2 mul add den div
        B0 yP0 mul w1 B1 mul yP1 mul add w2 B2 mul yP2 mul add den div
             } if
        } for
        } def
        /RQBCmasse2 {
        0 1 nB {/t exch nB div def
       	den  -1e-6 lt  { % B0*P0+w1*B1*P1+w2*B2*P2
        B0 xP0 mul w1 B1 mul xP1 mul add w2 B2 mul xP2 mul add den div
        B0 yP0 mul w1 B1 mul yP1 mul add w2 B2 mul yP2 mul add den div
             } if
        } for        
        } def
        } if % fin choix 6
   choix 7 eq {
       /den { w0 B0 mul w1 B1 mul add w2 B2 mul add } def
% tableau de pointslist[(w0-w1+sqrt(-w0*w2+w1^2))/(w0-2*w1+w2),(w0-w1-sqrt(-w0*w2+w1^2))/(w0-2*w1+w2)]
     /RQBCmasse1 {
        0 1 nB  {/t exch nB  div def
       den  1e-6 gt  { % w0*B0*P0+w1*B1*P1+w2*B2*P2
       w0 B0 mul xP0 mul B1 w1 mul xP1 mul add w2 B2 mul xP2 mul add den div % xP
       w0 B0 mul yP0 mul B1 w1 mul yP1 mul add w2 B2 mul yP2 mul add den div % yP
                    } if
                } for
        } def
       /RQBCmasse2 {
        0 1 nB {/t exch nB div def
       den  -1e-6 lt  {
       w0 B0 mul xP0 mul B1 w1 mul xP1 mul add w2 B2 mul xP2 mul add den div % xP
       w0 B0 mul yP0 mul B1 w1 mul yP1 mul add w2 B2 mul yP2 mul add den div % yP
                    } if
                } for
        } def
        } if  % fin du choix 7
} def
%
end %% tx@Dict
