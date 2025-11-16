%%
%% This is file `pst-intersect.pro',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% pst-intersect.dtx  (with options: `prolog')
%% 
%% This is a generated file.
%% 
%% Project: pst-intersect
%% Version: 0.4 (2014/03/16)
%% 
%% Copyright (C) 2007-2014 by Christoph Bersch <usenet@bersch.net>
%% 
%% This work may be distributed and/or modified under the
%% conditions of the LaTeX Project Public License, either version 1.3c
%% of this license or (at your option) any later version.
%% The latest version of this license is in
%%   http://www.latex-project.org/lppl.txt
%% and version 1.3c or later is part of all distributions of LaTeX
%% version 2008/05/04 or later.
%% 
%% This work has the LPPL maintenance status "maintained".
%% 
%% The current maintainer of this work is Christoph Bersch.
%% 
%% This work consists of the files pst-intersect.dtx and pst-intersect.ins
%% and the derived files
%%     pst-intersect.sty, pst-intersect.tex, pst-intersect.pro.
%% 
/tx@IntersectDict 200 dict def
tx@IntersectDict begin
/VecAdd {
    3 -1 roll add 3 1 roll add exch
} bind def
/VecSub {
    neg 3 -1 roll add 3 1 roll neg add exch
} bind def
/VecScale {
  dup 4 -1 roll mul 3 1 roll mul
} bind def
/ToPnt {
    [ 3 1 roll ]
} bind def
/MaxPrecision 1e-6 def
/Epsilon 1e-4 def
/MinClippedSizeThreshold 0.8 def
/H1Interval [0 0.5] def
/H2Interval [0.5 MaxPrecision add 1] def
/IntersectBeziers {
  2 copy length 2 eq exch length 2 eq and {
    IntersectLineSegms
  }{
    2 copy [0 1] [0 1] IterateIntersection
  } ifelse
  3 -1 roll exch
} bind def
/IntersectLines {
  (IntersectLines) DebugBegin
  2 copy
  exch { aload pop } forall 5 -1 roll { aload pop } forall
  8 -2 roll 2 copy 10 4 roll 4 2 roll 2 copy 6 2 roll 10 2 roll
  VecSub
  6 2 roll 4 2 roll VecSub
  8 4 roll 4 2 roll VecSub
  6 copy 12 -4 roll
  neg 4 -1 roll mul 3 1 roll mul add
  dup 0 eq {
    9 { pop } repeat [] []
  } {
    dup 10 1 roll 5 1 roll
     4 -1 roll mul 3 1 roll mul sub exch div
     6 1 roll 4 -1 roll mul 3 1 roll mul sub exch div
     [ exch ] exch [ exch ]
   } ifelse
  DebugEnd
} bind def
/IntersectLineSegms {
  IntersectLines
  dup length 0 eq not {
    0 get exch 0 get
    2 copy 2 copy 0 ge exch 0 ge and 3 1 roll 1 le exch 1 le and and {
      [ exch ] exch [ exch ]
    } {
      pop pop [] []
    } ifelse
  } if
} bind def
/IntersectLineLineSegm {
  tx@IntersectDict begin IntersectLines end
  dup length 0 eq not {
    0 get dup dup 0 ge exch 1 le and {
      [ exch ]
    } {
      pop pop [] []
    } ifelse
  } if
  3 -1 roll exch
} bind def
/IntersectLinePath {
  (IntersectLinePath) DebugBegin
  3 dict begin
    PreparePath
    2 copy ElongateLine exch 3 -1 roll pop
    /isect [] def
    /t -1 def
    /n -1 def
    {
      /n n 1 add def
      2 copy IntersectBeziers
      dup 5 1 roll LoadIntersectionPoints
      dup length 0 gt {
        /isect exch def
        0 get aload pop add 0.5 mul n add /t exch def
        exch pop
        exit
      } {
        pop pop pop
      } ifelse
    } forall
    t isect
  end
  DebugEnd
} bind def
/ElongateLine {
  exch { aload pop } forall
  4 2 roll 2 copy 6 2 roll
  VecSub 0 5 1 roll
  6 -1 roll {
    {
      aload pop
      6 2 roll 4 copy 10 4 roll
      6 2 roll VecSub 4 2 roll
      tx@EcldDict begin Project end
      tx@Dict begin Pyth end
      6 -1 roll 2 copy
      gt { pop } { exch pop } ifelse
      5 1 roll
    } forall
  } forall
  % for a line
  5 -1 roll VecScale 4 copy VecSub ToPnt 5 1 roll VecAdd ToPnt ToPnt
  % for a ray
  %4 2 roll 2 copy ToPnt 6 1 roll 4 2 roll 5 -1 roll 1.1 mul VecScale VecAdd ToPnt ToPnt
} bind def
/IntersectPaths {
  (IntersectPaths) DebugBegin
  6 dict begin
    2 copy exch PreparePath dup length /nA exch def
    exch PreparePath dup length /nB exch def
    /isect [] def
    /tA [] def /tB [] def
    { % [pathA] [Bi]
      /nB nB 1 sub def
      exch dup 3 1 roll % [pathA] [Bi] [pathA]
      {
        /nA nA 1 sub def
        exch dup 3 1 roll % [pathA] [Bi] [Aj] [Bi]
        IntersectBeziers % [curveA] [tA] [curveB] [tB]
        4 copy LoadIntersectionPoints
        [ exch isect aload pop ] /isect exch def
        exch pop 3 -1 roll pop
        [ tB aload length 2 add -1 roll TArray { nB add } forall ] /tB exch def
        [ tA aload length 2 add -1 roll TArray { nA add } forall ] /tA exch def
      } forall
      pop % remove [Bi]
      dup length /nA exch def
    } forall
    pop % remove [pathA]
    [ isect { aload pop } forall ] 3 1 roll tA exch tB
  end
  DebugEnd
} bind def
/IntersectCurvePath {
  (IntersectCurvePath) DebugBegin
  6 dict begin
    2 copy PreparePath dup length /n exch def
    /isect [] def
    /tA [] def /tB [] def
    {
      /n n 1 sub def
      exch dup 3 -1 roll
      IntersectBeziers
      4 copy LoadIntersectionPoints
      [ exch isect aload pop ] /isect exch def
      pop 3 -1 roll pop
      [ tB aload length 2 add -1 roll TArray { n add } forall ] /tB exch def
      [ tA aload length 2 add -1 roll TArray aload pop ] /tA exch def
    } forall
    pop
    [ isect { aload pop } forall ] 3 1 roll tA exch tB
  end
  DebugEnd
} bind def
/IntersectPathCurve {
  exch IntersectCurvePath 4 2 roll
} bind def
/MergeAndSortArrays {
  [ 3 1 roll aload pop counttomark -1 roll aload pop ]
  dup length 0 gt {
    dup dup 0 get type /arraytype eq {
      hulldict /comp get
    } {
      /lt
    } ifelse
    exch quicksort
  } if
} bind def
/SaveIntersection {
  (SaveIntersection) DebugBegin
  exch dup 3 1 roll % isectname add? isectname
  currentdict exch known and {
    load begin % pnts A tA B tB /A /B
      dup currentdict exch known { % /nameB already saved.
        4 -1 roll pop % pnts A tA tB /A /B
        nametostr (@t) strcat cvn dup load 4 -1 roll
        MergeAndSortArrays def
      } {
        dup 5 -1 roll def % pnts A tA B tB /A /B
        nametostr (@t) strcat cvn 3 -1 roll TArray def
      } ifelse % pnts A tA /A
      dup currentdict exch known { % /nameB already saved.
        3 -1 roll pop
        nametostr (@t) strcat cvn dup load 3 -1 roll
        MergeAndSortArrays def
      } {
        dup 4 -1 roll def
        nametostr (@t) strcat cvn exch TArray def
      } ifelse
      /Points exch ArrayToPointArray Points ArrayToPointArray
      MergeAndSortArrays PointArrayToArray def
    end
  } {
    4 dict dup 3 1 roll def
    begin
      dup 5 -1 roll def
      nametostr (@t) strcat cvn 3 -1 roll TArray def
      dup 4 -1 roll def
      nametostr (@t) strcat cvn exch TArray def
      /Points exch def
    end
  } ifelse
  DebugEnd
} bind def
/TArray {
  dup length 0 gt {
    dup 0 get type /arraytype eq {
      [ exch
      { %dup type /nulltype eq { pop exit } if
   aload pop add 0.5 mul
      } forall ]
    } if
    dup /lt exch quicksort
  } if
} bind def
/InitTracing {
  /movetype /moveto load def
  /linetype /lineto load def
  /curvetype /curveto load def
} bind def
/GetFullPath {
  (GetFullPath) DebugBegin
  { /movetype counttomark 3 roll }
  { /linetype counttomark 3 roll }
  { /curvetype counttomark 7 roll }{} pathforall
  DebugEnd
} bind def
/ReversePath {
  gsave newpath
    [ exch aload pop InitTracing
    { counttomark 0 eq { exit } if
      load exec
    } loop
    reversepath
    GetFullPath ]
  grestore
} bind def
/ReverseCurve {
  PointArrayToArray aload pop % [ tstart tstop [ X0 Y0 X1 Y1...
  counttomark -2 4 { 2 roll } for ] ArrayToPointArray
} bind def
/ReverseInterval {
  3 -1 roll dup 4 1 roll GetSegmentCount
  dup 4 1 roll exch sub 3 1 roll sub exch
} bind def
/UnifyInterval {
  exch dup 0 lt { pop 0 } if exch
  3 -1 roll dup 4 1 roll GetSegmentCount
  2 copy exch dup 3 1 roll % [curve] tstart tstop cnt tstop cnt tstop
  lt exch 0 lt or { exch } if pop % (tstop < 0 | cnt < tstop)
} bind def
/PreparePath {
  (PreparePath) DebugBegin
  [ exch aload pop
  {
    dup type /nametype eq not { exit } if
    dup /movetype eq {
      pop ToPnt /@mycp exch def
    } {
      dup /linetype eq {
        pop [ @mycp 4 2 roll 2 copy ToPnt /@mycp exch def ToPnt ]
      } {
        pop [ @mycp 8 2 roll 2 copy ToPnt /@mycp exch def
        ToPnt 5 1 roll ToPnt 4 1 roll ToPnt 3 1 roll ]
      } ifelse
      counttomark 1 roll
    } ifelse
  } loop ]
  DebugEnd
} bind def
/GetSegmentCount {
  (GetSegmentCount) DebugBegin
  dup IsPath {
    [ exch aload pop 0
    {
      counttomark 1 eq { exit } if
      exch
      dup /movetype eq {
        pop 3 1 roll pop pop
      }{
        dup /linetype eq {
          pop 1 add 3 1 roll pop pop
        }{
          pop 1 add 7 1 roll 6 { pop } repeat
        } ifelse
      } ifelse
    } loop
    exch pop
  } {
    % a Bezier curve is a single segment
    length 0 gt { 1 } { 0 } ifelse
  } ifelse
  DebugEnd
} bind def
/LoadLineIntersectionPoints {
  (LoadLineIntersectionPoints) DebugBegin
  exch [ exch { aload pop } forall ]
  tx@Dict begin tx@FuncDict begin 2 dict begin
    dup length 2 idiv 1 sub /BezierType exch def /Points exch def
    [ exch { GetBezierCoor } forall ]
  end end end
  DebugEnd
} bind def
/LoadCurveIntersectionPoints {
  (LoadCurveIntersectionPoints) DebugBegin
  2 {
    4 2 roll
    [ exch { aload pop } forall ]
    exch [ exch { aload pop } forall ]
  } repeat
  tx@Dict begin tx@FuncDict begin 2 dict begin
    dup length 2 idiv 1 sub /BezierType exch def /Points exch def
      [ exch { GetBezierCoor } forall ]
    3 1 roll
    dup length 2 idiv 1 sub /BezierType exch def /Points exch def
      [ exch { GetBezierCoor } forall ]
    end
    2 {
      [ exch aload length 4 idiv {
        [ 5 1 roll ] counttomark 1 roll
      } repeat ]
      exch
    } repeat
    2 {
      dup hulldict /comp get exch quicksort exch
    } repeat
    2 dict begin
      /B exch def /A exch def
      [ 0 1 A length 1 sub {
        dup A exch get exch B exch get % [IAi] [IBi]
        2 copy aload pop VecSub Pyth exch
        aload pop VecSub Pyth lt { exch } if pop
        aload pop VecAdd 0.5 VecScale
      } for ]
    end
  end end
  DebugEnd
} bind def
/LoadIntersectionPoints {
  (LoadIntersectionPoints) DebugBegin
  4 copy pop exch pop length 2 eq exch length 2 eq and {
    pop pop LoadLineIntersectionPoints
  }{
    LoadCurveIntersectionPoints
  } ifelse
  DebugEnd
} bind def
/IterateIntersection {
    (IterateIntersection) DebugBegin
    12 dict begin
/precision MaxPrecision def
        4 2 roll 2 copy 6 2 roll
        dup IsPath not { PointArrayToArray } if
        0 exch { dup type /nametype eq { pop }{ abs max} ifelse } forall
        exch dup IsPath not { PointArrayToArray } if
        { dup type /nametype eq { pop }{ abs max} ifelse } forall
        Epsilon mul /epsilon exch def
        /counter 0 def
/depth 0 def
/domsA [] def
/domsB [] def
/domsA /domsB 6 2 roll _IterateIntersection
domsB domsA
    end
    dup length 0 gt {
      TArraysRemoveDup
    } if
    DebugEnd
} bind def
/TArraysRemoveDup {
  4 dict begin
    /tB exch def
    /tA exch def
    /j 0 def
    [ tA 0 get tB 0 get
    1 1 tA length 1 sub {
      /i exch def
      tA j get aload pop tA i get aload pop tx@Dict begin Pyth2 end MaxPrecision gt
      tB j get aload pop tB i get aload pop tx@Dict begin Pyth2 end MaxPrecision gt and {
        % keep the current parameter point
        /j i def
        tB i get tA i get
        counttomark 2 idiv 1 add 1 roll
      } if
    } for
    counttomark 2 idiv 1 add [ exch 1 roll ] % [ ... [tB]
    counttomark 1 add 1 roll ] exch % [tA] [tB]
  end
} bind def
/_IterateIntersection {
    (_IterateIntersection) DebugBegin
    CloneVec /domB exch def
    CloneVec /domA exch def
    CloneCurve /CurveB exch def
    CloneCurve /CurveA exch def
    /iter 0 def
    /depth depth 1 add def
    /dom null def
    /counter counter 1 add def
    CheckIT {
(>> curve subdivision performed: dom(A) = ) domA CurveToString strcat
(, dom(B) = ) strcat domB CurveToString strcat ( <<) strcat ==
    } if
    CurveA IsConstant CurveB IsConstant and {
CurveA MiddlePoint ToPnt
CurveB MiddlePoint ToPnt AreNear {
    domA domB 4 -1 roll exch PutInterval PutInterval
} {
    pop pop
} ifelse
    }{
counter 100 lt {
    {
/iter iter 1 add def
iter 100 lt
domA Extent precision ge
domB Extent precision ge or and not {
    iter 100 ge {
false
    } {
CurveA MiddlePoint ToPnt
CurveB MiddlePoint ToPnt AreNear {
    domA domB true
}{
    false
} ifelse
    } ifelse
    exit
} if
CheckIT {
    (counter: ) counter 20 string cvs strcat
    (, iter: ) iter 20 string cvs strcat strcat
    (, depth: ) depth 20 string cvs strcat strcat ==
} if
CurveA CurveB ClipCurve /dom exch def

CheckIT {(dom : ) dom CurveToString strcat == } if
dom IsEmptyInterval {
    CheckIT { (empty interval, exit) == } if
    false exit
} if
dom aload pop 2 copy min 3 1 roll max gt {
    CheckIT {
(dom[0] > dom[1], invalid!) ==
    } if
    false exit
} if

domB dom MapTo /domB exch def
CurveB dom Portion

CurveB IsConstant CurveA IsConstant and {
    CheckIT {
           (both curves are constant: ) ==
(C1: [ ) CurveA { CurveToString ( ) strcat strcat } forall (]) strcat ==
(C2: [ ) CurveB { CurveToString ( ) strcat strcat } forall (]) strcat ==
    } if
    CurveA MiddlePoint ToPnt
    CurveB MiddlePoint ToPnt AreNear {
domA domB true
    } {
false
    } ifelse
    exit
} if
dom Extent MinClippedSizeThreshold gt {
    CheckIT {
(clipped less than 20% : ) ==
(angle(A) = ) CurveA dup length 1 sub get aload pop
      CurveA 0 get aload pop VecSub
          exch 2 copy 0 eq exch 0 eq and {
  pop pop (NaN)
      } {
  atan 20 string cvs
      } ifelse strcat ==
        (angle(B) = ) CurveB dup length 1 sub get aload pop
                      CurveB 0 get aload pop VecSub
      exch 2 copy 0 eq exch 0 eq and {
  pop pop (NaN)
      } {
  atan 20 string cvs
      } ifelse strcat ==
        (dom : ) == dom == (domB :) == domB ==
    } if
    CurveA CurveB domA domB iter
          7 -2 roll 2 copy 9 2 roll 2 copy
    domA Extent domB Extent gt {
CurveA CloneCurve dup H1Interval Portion % pC1
CurveA CloneCurve dup H2Interval Portion % pC2
domA H1Interval MapTo                    % dompC1
domA H2Interval MapTo                    % dompC2
3 -1 roll exch % /domsA /domsB /domsA /domsB pC1 dompC1 pC2 dompC2
CurveB exch domB 8 4 roll % /domsA /domsB pC2 CurveB dompC2 domB /domsA /domsB pC1 dompC1
CurveB exch domB % /domsA /domsB pC2 CurveB dompC2 domB /domsA /domsB pC1 CurveB dompC1 domB
    } {
CurveB CloneCurve dup H1Interval Portion % pC1
CurveB CloneCurve dup H2Interval Portion % pC2
domB H1Interval MapTo                    % dompC1
domB H2Interval MapTo                    % dompC2
8 -2 roll exch 8 2 roll 6 -2 roll exch 6 2 roll % /domsB /domsA /domsB /domsA pC1 pC2 dompC1 dompC2
3 -1 roll exch % /domsB /domsA /domsB /domsA pC1 dompC1 pC2 dompC2
CurveA exch domA 8 4 roll % /domsB /domsA pC2 CurveA dompC2 domA /domsB /domsA pC1 dompC1
CurveA exch domA          % /domsB /domsA pC2 CurveA dompC2 domA /domsB /domsA pC1 CurveA dompC1 domA
    } ifelse

    _IterateIntersection
    _IterateIntersection
    /iter exch def
    /domB exch def
    /domA exch def
    /CurveB exch def
    /CurveA exch def
    false exit
} if
CurveA CurveB /CurveA exch def /CurveB exch def
domA domB /domA exch def /domB exch def
exch
    } loop
    {
4 -1 roll exch PutInterval PutInterval
CheckIT {
    (found an intersection ============================) ==
} if
    } { pop pop } ifelse
} {
    pop pop
} ifelse
    } ifelse
    /depth depth 1 sub def
    DebugEnd
} bind def
/PutInterval {
    CloneVec [ exch 3 -1 roll dup 4 1 roll load aload pop ] def
} bind def
/IsEmptyInterval {
    aload pop 0 eq exch 1 eq and
} bind def
/ToUnitInterval {
    ToUnitRange exch ToUnitRange 2 copy gt {
exch
    } if
    ToPnt
} bind def
/ToUnitRange {
    dup 0 lt {
pop 0
    }{
dup 1 gt {
    pop 1
} if
    } ifelse
} bind def
/CloneCurve {
    [ exch {
CloneVec
    } forall ]
} bind def
/CloneVec {
    aload pop ToPnt
} bind def
/MapTo {
    (MapTo) DebugBegin
    exch aload 0 get 3 1 roll exch sub 2 copy % [I] J0 Jextent J0 Jextent
    5 -1 roll aload aload pop % J0 Jextent J0 Jextent I0 I1 I0 I1
    min 4 -1 roll mul % J0 Jextent J0 I0 I1 min(I0,I1)*Jextent
    4 -1 roll add [ exch % J0 Jextent I0 I1 [ J0new
    6 2 roll max mul add ]
    DebugEnd
} bind def
/Portion {
    (Portion) DebugBegin
    dup Min 0 eq { % [CurveB] [I]
Max dup 1 eq {% [CurveB] I.max()
    % I.max() == 1
    pop pop
} { % [CurveB] I.max()
    LeftPortion
} ifelse
    } { % [CurveB] [I]
2 copy Min % [CurveB] [I] [CurveB] I.min()
RightPortion
dup Max 1 eq {
    % I.max() == 1
    pop pop
} {% [CurveB] [I]
    dup aload pop exch sub 1 3 -1 roll Min sub div % [CurveB] (I1-I0)/(1-I.min())
    LeftPortion
} ifelse
    } ifelse
    DebugEnd
} bind def
/LeftPortion {
    (LeftPortion) DebugBegin
    exch dup length 1 sub dup 4 1 roll % L-1 t [CurveB] L-1
    1 1 3 -1 roll { % L-1 t [CurveB] i
4 -1 roll dup 5 1 roll % L-1 t [CurveB] i L-1
-1 3 -1 roll % L-1 t [CurveB] L-1 -1 i
{ % L-1 t [CurveB] j
    2 copy 5 copy % L-1 t [CurveB] j [CurveB] j t [CurveB] j [CurveB] j
    1 sub get 3 1 roll get % L-1 t [CurveB] j [CurveB] j t B[j-1] B[j]
    Lerp put pop % L-1 t [CurveB]
} for
    } for
    pop pop pop
    DebugEnd
} bind def
/RightPortion {
    (RightPortion) DebugBegin
    exch dup length 1 sub dup 4 1 roll % L-1 t [CurveB] L-1
    1 1 3 -1 roll {% L-1 t [CurveB] i
4 -1 roll dup 5 1 roll % L-1 t [CurveB] i L-1
exch sub 0 1 3 -1 roll  % L-1 t [CurveB] 0 1 L-i-1
{% L-1 t [CurveB] j
    2 copy 5 copy
    get 3 1 roll 1 add get Lerp put pop
} for
    } for
    pop pop pop
    DebugEnd
} bind def
/Lerp {
    (Lerp) DebugBegin
    3 -1 roll dup 1 exch sub 3 1 roll % [A] (1-t) [B] t
    exch aload pop 3 -1 roll VecScale % [A] (1-t) B.x*t B.y*t
    4 2 roll
    exch aload pop 3 -1 roll VecScale VecAdd ToPnt % [A.x*(1-t)+B.x*t A.y*(1-t)+B.y*t]
    DebugEnd
} bind def
/IsConstant {
    aload length [ exch 1 roll ] true 3 1 roll
    {
exch dup 4 1 roll
AreNear and exch
    } forall
    pop
} bind def
/AreNear {
    (AreNear) DebugBegin
    aload pop 3 -1 roll aload pop
    VecSub abs epsilon lt exch abs epsilon lt and
    DebugEnd
} bind def
/Min {
    aload pop min
} bind def
/Max {
    aload pop max
} bind def
/Extent {
    aload pop exch sub
} bind def
/MiddlePoint {
    dup dup length 1 sub get aload pop
    3 -1 roll 0 get aload pop
    VecAdd 0.5 VecScale
} bind def
/OrthogonalOrientationLine {
    (OrthogonalOrientationLine) DebugBegin
    dup dup length 1 sub get aload pop 3 -1 roll 0 get aload pop VecSub
    neg exch
    4 2 roll 2 copy 6 2 roll VecAdd
    ImplicitLine
    DebugEnd
} bind def
/PickOrientationLine {
    (PickOrientationLine) DebugBegin
    dup dup length 1 sub exch 0 get% [Curve] L-1 P0
    exch -1 1 {% [Curve] P0 i
3 -1 roll dup 4 1 roll exch get % [Curve] P0 Pi
2 copy AreNear {
    pop
} {
    exit
} ifelse
    } for
    3 -1 roll pop
    exch aload pop 3 -1 roll aload pop ImplicitLine
    DebugEnd
} bind def
/ImplicitLine {
    4 copy % Xi Yi Xj Yj Xi Yi Xj Yj
    3 -1 roll sub 7 1 roll sub 5 1 roll % Yj-Yi Xi-Xj Xi Yi Xj Yj
    % Yi*Xj - Xi*Yj
    4 -1 roll mul neg % Yj-Yi Xi-Xj Yi Xj -Yj*Xi
    3 1 roll mul add % Yj-Yi Xi-Xj Yi*Xj-Yj*Xi | l0 l1 l2
    3 1 roll 2 copy tx@Dict begin Pyth end dup dup % l2 l0 l1 L L L
    5 -1 roll exch % l2 l1 L L l0 L
    div 5 1 roll % l0/L l2 l1 L L
    3 1 roll div % l0/L l2 L l1/L
    3 1 roll div % l0/L l1/L l2/L
} bind def
/distance {
    5 1 roll 3 -1 roll mul 3 1 roll mul add add
} bind def
/ArrayToPointArray {
    aload length dup 2 idiv {
3 1 roll [ 3 1 roll ] exch
dup 1 sub 3 1 roll 1 roll
    } repeat 1 add [ exch 1 roll ]
} bind def
/PointArrayToArray {
    aload length dup {
1 add dup 3 -1 roll aload pop 4 -1 roll 1 add 2 roll
    } repeat 1 add [ exch 1 roll ]
} bind def
/ClipCurve {
    (ClipCurve) DebugBegin
    4 dict begin
    /CurveB exch def /CurveA exch def
    CurveA IsConstant {
     CurveA MiddlePoint CurveB OrthogonalOrientationLine
    } {
CurveA PickOrientationLine
    } ifelse
    CheckIT {
3 copy exch 3 -1 roll (OrientationLine : )
3 { exch 20 string cvs ( ) strcat strcat } repeat ==
    } if
    CurveA FatLineBounds
    CheckIT { dup (FatLineBounds : ) exch aload pop exch 20 string cvs (, ) strcat exch 20 string cvs strcat strcat == } if
    CurveB ClipCurveInterval
    end
    DebugEnd
} bind def
/FatLineBounds {
    (FatLineBounds) DebugBegin
    /dmin 0 def /dmax 0 def
    {
4 copy aload pop 5 2 roll distance
dup dmin lt { dup /dmin exch def } if
dup dmax gt { dup /dmax exch def } if
pop pop
    } forall
    [dmin dmax]
    DebugEnd
} bind def
/ClipCurveInterval {
    (ClipCurveInterval) DebugBegin
    15 dict begin
    /curve exch def
    aload pop 2 copy min /boundMin exch def max /boundMax exch def
    [ 4 1 roll ] cvx /fatline exch def
    % number of sub-intervals
    /n curve length 1 sub def
    % distance curve control points
    /D n 1 add array def
    0 1 n { % i
dup curve exch get aload pop % i Pi.x Pi.y
fatline distance % distance d of Point i from the orientation line, on stack; i d
exch dup n div % d i i/n
[ exch 4 -1 roll ] % i [ i/n d ]
D 3 1 roll put
    } for
    D ConvexHull /D exch def
    /getX { D exch get 0 get } def
    /getY { D exch get 1 get } def
    /tmin 1 def /tmax 0 def
    0 getY dup
    boundMin lt /plower exch def
    boundMax gt /phigher exch def
    plower phigher or not {
tmin 0 getX gt { /tmin 0 getX def } if
tmax 0 getX lt { /tmax 0 getX def } if
    } if
    1 1 D length 1 sub {
/i exch def
/clower i getY boundMin lt def
/chigher i getY boundMax gt def
clower chigher or not {
    tmin i getX gt { /tmin i getX def } if
    tmax i getX lt { /tmax i getX def } if
} if
clower plower eq not {
    boundMin i 1 sub i D Intersect % t on stack
    dup tmin lt { dup /tmin exch def } if
    dup tmax gt { dup /tmax exch def } if
    pop
    /plower clower def
} if
chigher phigher eq not {
    boundMax i 1 sub i D Intersect
    dup tmin lt { dup /tmin exch def } if
    dup tmax gt { dup /tmax exch def } if
    pop
    /phigher chigher def
} if
    } for
    /i D length 1 sub def
    /clower 0 getY boundMin lt def
    /chigher 0 getY boundMax gt def
    clower plower eq not {
boundMin i 0 D Intersect
dup tmin lt { dup /tmin exch def } if
dup tmax gt { dup /tmax exch def } if
pop
    } if
    chigher phigher eq not {
boundMax i 0 D Intersect
dup tmin lt { dup /tmin exch def } if
dup tmax gt { dup /tmax exch def } if
pop
    } if
    [tmin tmax]
    end
    DebugEnd
} bind def
/Intersect {
    dup 4 -1 roll get aload pop
    4 2 roll exch get aload pop
    4 2 roll 2 copy 6 2 roll VecSub
    5 2 roll
    neg 3 -1 roll add
    3 -1 roll div
    3 -1 roll mul add
} bind def
/IsPath {
  dup length 1 sub get type /nametype eq { true } { false } ifelse
} bind def
/ShowPathPortion {
  (ShowPathPortion) DebugBegin
  8 dict begin
  /tstop exch def
  /tstart exch def
  /savecp { ToPnt cvx /@cp exch def } def
  InitTracing
  /n 0 def
  mark exch aload pop
  {
    counttomark 0 eq n tstop ge or { cleartomark exit } if
    dup /movetype eq not { /n n 1 add def } if
    dup /movetype eq {
      pop savecp
    } {
      tstart n ge {
        /curvetype eq { 6 2 roll 4 { pop } repeat } if
        savecp
      } {
        tstart n 1 sub gt tstop n lt or {
          tstart n sub 1 add tstop n sub 1 add
          ToUnitInterval exch
          /linetype eq {
            3 1 roll ToPnt
            tstart n 1 sub gt { @cp ToPnt } { currentpoint ToPnt } ifelse exch ToPnt
            dup 3 -1 roll Portion
            aload pop exch
            tstart n 1 sub gt {
              exch aload pop 3 -1 roll aload pop ArrowA
              tstop n le {
                currentpoint 4 2 roll ArrowB linetype pop pop
              } {
                linetype
              } ifelse
            } {
              pop aload pop currentpoint 4 2 roll ArrowB linetype pop pop
            } ifelse
          } {
            7 1 roll
            [ tstart n 1 sub gt { @cp }{ currentpoint } ifelse
            9 3 roll ] ArrayToPointArray
            dup 3 -1 roll
            Portion
            { aload pop } forall
            tstart n 1 sub gt {
              8 -4 roll 4 2 roll ArrowA 6 2 roll
            } {
              8 -2 roll pop pop
            } ifelse
            tstop n le { ArrowB } if
            curvetype
          } ifelse
        }{
          tstart n 1 sub eq {
            /linetype eq {
              @cp ArrowA
              tstop n eq {
                currentpoint 4 2 roll ArrowB linetype pop pop
              } {
                linetype
              } ifelse
            } {
              6 -2 roll @cp ArrowA 6 2 roll
              tstop n eq {
                ArrowB
              } if
              curvetype
            } ifelse
          } {
            /linetype eq {
              tstop n eq {
                currentpoint 4 2 roll ArrowB linetype pop pop
              }{
                linetype
              } ifelse
            } {
              tstop n eq {
                ArrowB
              } if
              curvetype
            } ifelse
          } ifelse
        } ifelse
      } ifelse
    } ifelse
  } loop
  end
  DebugEnd
} bind def
/GetCurvePoint {
  dup IsPath {
    5 dict begin
    exch dup /tstart exch def
    1 add cvi /tstop exch def
    /savecp { ToPnt cvx /@cp exch def } def
    /n 0 def
    mark exch aload pop
    {
      counttomark 0 eq n tstop ge or { cleartomark exit } if
      dup /movetype eq not { /n n 1 add def } if
      dup /movetype eq {
        pop savecp
      } {
        tstart n ge {
          /curvetype eq { 6 2 roll 4 { pop } repeat } if
          savecp
        } {
          tstart n 1 sub gt {
            tstart n sub 1 add tstop n sub 1 add
            ToUnitInterval exch
            /linetype eq {
              3 1 roll ToPnt
              tstart n 1 sub gt { @cp ToPnt } { currentpoint ToPnt } ifelse exch ToPnt
              dup 3 -1 roll Portion
            } {
              7 1 roll
              [ @cp 9 3 roll ] ArrayToPointArray
              dup 3 -1 roll
              Portion
            } ifelse
            0 get aload pop
          }{
            /curvetype eq {
              pop pop pop pop
            } if
          } ifelse
          counttomark 1 add 2 roll cleartomark exit
        } ifelse
      } ifelse
    } loop
    end
  } {
    exch dup 0 eq {
      pop 0 get aload pop
    } {
      0 exch ToUnitInterval exch dup 3 -1 roll Portion
      dup length 1 sub get aload pop
    } ifelse
  } ifelse
} bind def
/TraceCurveOrPath {
  4 1 roll
  UnifyInterval
  3 -1 roll dup IsPath {
    4 -1 roll pop
    3 1 roll 2 copy gt {
      ReverseInterval
      3 -1 roll ReversePath 3 1 roll
    } if
    ShowPathPortion
  }{ % tstart tstop [curve]
    mark exch 4 2 roll % [ [curve] tstart tstop
      2 copy gt { % tstart > tstop
        exch
        [ 4 -1 roll ReverseCurve 3 1 roll % [ [curve'] tstart tstop
      } if
      ToUnitInterval exch dup 3 -1 roll Portion
      { aload pop } forall
      counttomark -2 4 { 2 roll } for
      counttomark 2 sub 2 idiv
      counttomark 2 add -1 roll exec
    } ifelse
} bind def
 % Graham Scal algorithm to compute the convex hull of a set of
 % points. Code written by Bill Casselman,
 %  http://www.math.ubc.ca/~cass/graphics/text/www/
 %
 % [[X1 Y1] [X2 Y2] ... [Xn Yn]] hull -> [[...] ... [...]]
 %
/hulldict 32 dict def
hulldict begin

 % u - v
/vsub { 2 dict begin
/v exch def
/u exch def
[
  u 0 get v 0 get sub
  u 1 get v 1 get sub
]
end } def

 % u - v rotated 90 degrees
/vperp { 2 dict begin
/v exch def
/u exch def
[
  v 1 get u 1 get sub
  u 0 get v 0 get sub
]
end } def

/dot { 2 dict begin
/v exch def
/u exch def
  v 0 get u 0 get mul
  v 1 get u 1 get mul
  add
end } def

 % P Q
 % tests whether P < Q in lexicographic order
 % i.e xP < xQ, or yP < yQ if xP = yP
/comp { 2 dict begin
/Q exch def
/P exch def
P 0 get Q 0 get lt
  P 0 get Q 0 get eq
  P 1 get Q 1 get lt
  and
or
end } def

end

 % args: an array of points C
 % effect: returns the array of points on the boundary of
 %     the convex hull of C, in clockwise order

/ConvexHull {
(ConvexHull) DebugBegin
hulldict begin
/C exch def
/comp C quicksort
/n C length def
 % Q might circle around to the start
/Q n 1 add array def
Q 0 C 0 get put
Q 1 C 1 get put
/i 2 def
/k 2 def
 % i is next point in C to be looked at
 % k is next point in Q to be added
 % [ Q[0] Q[1] ... ]
 % scan the points to make the top hull
n 2 sub {
  % P is the current point at right
  /P C i get def
  /i i 1 add def
  {
    % if k = 1 then just add P
    k 2 lt { exit } if
    % now k is 2 or more
    % look at Q[k-2] Q[k-1] P: a left turn (or in a line)?
    % yes if (P - Q[k-1])*(Q[k-1] - Q[k-2])^perp >= 0
    P Q k 1 sub get vsub
    Q k 1 sub get Q k 2 sub get vperp
    dot 0 lt {
      % not a left turn
      exit
    } if
    /k k 1 sub def
  } loop
  Q k P put
  /k k 1 add def
} repeat

 % done with top half
 % K is where the right hand point is
/K k 1 sub def

/i n 2 sub def
Q k C i get put
/i i 1 sub def
/k k 1 add def
n 2 sub {
  % P is the current point at right
  /P C i get def
  /i i 1 sub def
  {
    % in this pass k is always 2 or more
    k K 2 add lt { exit } if
    % look at Q[k-2] Q[k-1] P: a left turn (or in a line)?
    % yes if (P - Q[k-1])*(Q[k-1] - Q[k-2])^perp >= 0
    P Q k 1 sub get vsub
    Q k 1 sub get Q k 2 sub get vperp
    dot 0 lt {
      % not a left turn
      exit
    } if
    /k k 1 sub def
  } loop
  Q k P put
  /k k 1 add def
} repeat

 % strip Q down to [ Q[0] Q[1] ... Q[k-2] ]
 % excluding the doubled initial point
[ 0 1 k 2 sub {
  Q exch get
} for ]
end
DebugEnd
} def

/qsortdict 8 dict def

qsortdict begin

 % args: /comp a L R x
 % effect: effects a partition into two pieces [L j] [i R]
 %     leaves i j on stack

/partition { 8 dict begin
/x exch def
/j exch def
/i exch def
/a exch def
dup type /nametype eq { load } if /comp exch def
{
  {
    a i get x comp exec not {
      exit
    } if
    /i i 1 add def
  } loop
  {
    x a j get comp exec not {
      exit
    } if
    /j j 1 sub def
  } loop

  i j le {
    % swap a[i] a[j]
    a j a i get
    a i a j get
    put put
    /i i 1 add def
    /j j 1 sub def
  } if
  i j gt {
    exit
  } if
} loop
i j
end } def

 % args: /comp a L R
 % effect: sorts a[L .. R] according to comp
/subsort {
 % /c a L R
[ 3 1 roll ] 3 copy
 % /c a [L R] /c a [L R]
aload aload pop
 % /c a [L R] /c a L R L R
add 2 idiv
 % /c a [L R] /c a L R (L+R)/2
3 index exch get
 % /c a [L R] /c a L R x
partition
 % /c a [L R] i j
 % if j > L subsort(a, L, j)
dup
 % /c a [L R] i j j
3 index 0 get gt {
  % /c a [L R] i j
  5 copy
  % /c a [L R] i j /c a [L R] i j
  exch pop
  % /c a [L R] i j /c a [L R] j
  exch 0 get exch
  % ... /c a L j
  subsort
} if
 % /c a [L R] i j
pop dup
 % /c a [L R] i i
 % if i < R subsort(a, i, R)
2 index 1 get lt {
  % /c a [L R] i
  exch 1 get
  % /c a i R
  subsort
}{
  4 { pop } repeat
} ifelse
} def

end % qsortdict

 % args: /comp a
 % effect: sorts the array a
 % comp returns truth of x < y for entries in a

/quicksort { qsortdict begin
dup length 1 gt {
 % /comp a
dup
 % /comp a a
length 1 sub
 % /comp a n-1
0 exch subsort
} {
pop pop
} ifelse
end } def
/debug {
    dup 1 add copy {==} repeat pop
} bind def
/DebugIT false def
/CheckIT false def
/DebugDepth 0 def
/DebugBegin {
  DebugIT {
    /DebugProcName exch def
    DebugDepth 2 mul string
    0 1 DebugDepth 2 mul 1 sub {
      dup 2 mod 0 eq { (|) }{( )} ifelse
      3 -1 roll dup 4 2 roll
      putinterval
    } for
    DebugProcName strcat ==
    /DebugDepth DebugDepth 1 add def
  }{
    pop
  } ifelse
} bind def
/DebugEnd {
  DebugIT {
    /DebugDepth DebugDepth 1 sub def
    DebugDepth 2 mul 2 add string
    0 1 DebugDepth 2 mul 1 sub {
      dup 2 mod 0 eq { (|) }{ ( ) } ifelse
      3 -1 roll dup 4 2 roll
      putinterval
    } for
    dup DebugDepth 2 mul (+-) putinterval
    ( done) strcat ==
  } if
} bind def
/strcat {
    exch 2 copy
    length exch length add
    string dup dup 5 2 roll
    copy length exch
    putinterval
} bind def
/nametostr {
    dup length string cvs
} bind def
/ShowCurve {
    { aload pop } forall
    8 -2 roll moveto curveto
} bind def
/CurveToString {
    (CurveToString) DebugBegin
    aload pop ([) 3 -1 roll 20 string cvs strcat (, ) strcat exch 20 string cvs strcat (]) strcat
    DebugEnd
} bind def
end % tx@IntersectDict
