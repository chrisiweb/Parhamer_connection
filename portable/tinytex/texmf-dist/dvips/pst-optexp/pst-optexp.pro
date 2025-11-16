%%
%% This is file `pst-optexp.pro',
%% generated with the docstrip utility.
%%
%% The original source files were:
%%
%% pst-optexp.dtx  (with options: `prolog')
%% 
%% This is a generated file.
%% 
%% Project: pst-optexp
%% Version: 6.1 (2022/02/06)
%% 
%% Copyright (C) 2007-2022 by Christoph Bersch <usenet@bersch.net>
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
%% This work consists of the files pst-optexp.dtx and pst-optexp.ins
%% and the derived files
%%     pst-optexp.sty, pst-optexp.pro.
%% 
/tx@OptexpDict 200 dict def
tx@OptexpDict begin
/DebugOE false def
/DebugDepth 0 def
/DebugBegin {
  DebugOE {
    /DebugProcName ED
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
  DebugOE {
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
/DebugMsg {
  DebugOE {
    DebugDepth 1 add 2 mul string
    0 1 DebugDepth 2 mul 1 add {
      dup 2 mod 0 eq { (|) }{( )} ifelse
      3 -1 roll dup 4 2 roll
      putinterval
    } for
    exch strcat ==
  }{
    pop
  } ifelse
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
/PrintWarning {
  (Warning pst-optexp: ) exch strcat (\n) strcat print
} bind def
/CompUnknownWarning {
  (Component ') exch strcat (' unknown) strcat Warning
} bind def
/OneFiberCompWarning {
  (Found only one unsupported component in beam path, drawing no beam) Warning
} bind def
/FiberCompWarning {
  (Found an unsupported component in beam path, stopping beam path) Warning
} bind def
/inttostr {
  dup type /integertype eq {
    dup log 1 add floor cvi string cvs
  } if
} bind def
/calcNodes {
  (calcNode) DebugBegin
  /YG exch def /XG exch def
  /by exch YG sub def
  /bx exch XG sub def
  /ay YG 3 -1 roll sub def
  /ax XG 3 -1 roll sub def
  ax ay NormalizeVec bx by NormalizeVec VecAdd
  2 copy Pyth abs 1e-4 lt {
    pop pop ax ay -90 matrix rotate dtransform
  } if
  /cy ED /cx ED
  /c ax bx add ay by add Pyth def
  c 0 eq {
    ax ay bx by DotProd 0 gt {
      /cx ax def
      /cy ay def
    }{
      /cx ay def
      /cy ax neg def
    } ifelse
  } if
  cx cy NormalizeVec 2 copy
  XG YG VecAdd /Y@A ED /X@A ED
  XG YG 4 2 roll VecSub /Y@B ED /X@B ED
  true
  ax by mul ay bx mul sub 0 le {
    pop false
    Y@A X@A
    /X@A X@B def
    /Y@A Y@B def
    /X@B exch def
    /Y@B exch def
  } if
  DebugEnd
} bind def
/capHeight {
    dup mul neg exch abs dup 3 1 roll dup mul add sqrt sub
} bind def
/leftCurvedIfc {
  /R1 exch def /h exch def
  0 R1 abs dup R1 h capHeight exch sub R1 sign mul dup
  h exch atan exch
  h neg exch atan
  R1 0 lt {
    /ArcL /arcn load def
  } {
    /ArcL /arc load def
  } ifelse
  R1
} bind def
/rightCurvedIfc {
  /R2 exch def /h exch def
  0 R2 abs dup R2 h capHeight sub R2 sign mul dup
  h neg exch atan exch
  h exch atan
  R2 0 lt {
    /ArcR /arcn load def
  } {
    /ArcR /arc load def
  } ifelse
  R2
} bind def
/SlopeAngle {
  (SlopeAngle) DebugBegin
  @GetCenter 3 -1 roll @GetCenter @ABVect exch atan
  DebugEnd
} bind def
/DefineExtNode {%
  (DefineExtNode) DebugBegin
  @@y mul RefFac mul @@y0 add
  exch @@x mul RefFac mul @@x0 add exch
  DebugEnd
} bind def
/GetInternalNodeNames {
  (GetInternalNodeNames) DebugBegin
  /reverse ED
  dup cvn load /N get dup
  reverse { -1 1 } { 1 1 3 -1 roll } ifelse
  { inttostr
    3 -1 roll dup 4 1 roll exch NodeName 3 1 roll
  } for
  pop pop
  DebugEnd
} bind def
/GetInternalBeamNodes {
  (GetInternalBeamNodes) DebugBegin
  [ 3 1 roll GetInternalNodeNames ]
  { @GetCenter } forall
  DebugEnd
} bind def
/InitOptexpComp {%
  /@@x 0 def
  /@@y 0 def
  /@@x0 0 def
  /@@y0 0 def
  /@xref [0] def
  /@yref [0] def
  /RefFac 1 def
} bind def
/NewTempNodeComp {
  (NewTempNodeComp) DebugBegin
  /sc ED
  dup cvn
  6 dict dup 3 1 roll def begin
    /ambiguous false def
    /allowbeaminside false def
    /forcebeaminside false def
    /name ED
    /correct false def
    {0 0} exch 3 -1 roll exec
    gsave
      translate
      /CompMtrx CM def
    grestore
    /N 1 def
    /n bgRefIndex def
    5 dict dup dup /P@1 ED /P@N ED
    begin
      /mode trans def
      {} 0 0 PlainIfc
    end
  /adjustRel true def
  end
  DebugEnd
} bind def
/CurvedIfc {
  5 2 roll
  2 copy 5 3 roll exec 3 -1 roll exec VecAdd
  5 -1 roll exec /Y ED /X ED
  exch exec 3 -1 roll 3 copy exec /RY ED /RX ED
  3 1 roll NormalizeVec 3 -1 roll exec
  tx@Dict begin Pyth end dup
  3 1 roll mul 1.00001 mul /NAup ED
  mul 1.00001 mul /NAlow ED
} bind def
/PlainIfc {
  5 2 roll
  dup 3 -1 roll exec NormalizeVec 3 -1 roll exec 2 copy /DY ED /DX ED
  tx@Dict begin Pyth end dup 4 2 roll
  exch exec 3 -1 roll exec /Y ED /X ED
  3 1 roll mul 1.00001 mul /NAup ED
  mul 1.00001 mul /NAlow ED
} bind def
/PathIfc {
  pop pop /NAup 0 def /NAlow 0 def
  3 1 roll /Path ED
  exec 3 -1 roll exec /Y ED /X ED
} bind def
/NewCompIfc {
  /scl ED
  /next ED
  dup (P@) exch strcat cvn
  6 dict dup
  3 1 roll def
  begin
    3 -1 roll
    /mode ED
    6 -1 roll dup 7 -1 roll
    {scl} 8 -2 roll next
  end
  exec scl ToVec 3 1 roll NodeName @NewNode
} bind def
/relative 0 def /absolute 1 def /center 2 def /firstcomp 3 def
/refl 0 def /trans 1 def /absorb 2 def /refltrans 3 def /auto 4 def /undefined -1 def
/desc 0 def /asc 1 def /amb 2 def
/ok 0 def /tir 1 def /missed 2 def
/bgRefIndex 0 def
/NewOptexpComp {
  (NewOptexpComp) DebugBegin
  /sc ED dup cvn
  gsave
  13 dict dup 3 1 roll def begin
  /name ED
  /forcebeaminside ED
  /allowbeaminside ED
  /ambiguous ED
  /grating false def
  dup type /booleantype eq not { false } if /correct ED
  tx@Dict begin
    STV {CP T} stopped pop
  end
  /CompMtrx CM def
  grestore
  counttomark dup 6 idiv dup /N ED 6 mul eq { 1 } if
  cvx 1 EvalRefIndex /n ED
  ambiguous {
    /ambIfc ED
  }{
    /ambIfc 0 def
  } ifelse
  1 N eq {
      name (1) 3 -1 roll {sc} NewCompIfc
      (1) (2) IfcCopy
      (2) (N) IfcAlias
  }{
    N -1 1 { %
      inttostr exch name 3 1 roll {sc} NewCompIfc
    } for
    N inttostr (N) IfcAlias
  } ifelse
  ambiguous ambIfc 0 gt and {
    ambIfc inttostr (C) IfcCopy
  } if
  end
  pop
  DebugEnd
} bind def
/NewOptexpFiberComp {
  (NewOptexpFiberComp) DebugBegin
  /sc ED dup cvn
  gsave
  12 dict dup 3 1 roll def begin
  /name ED
  tx@Dict begin
    STV {CP T} stopped pop
  end
  /CompMtrx CM def
  grestore
  counttomark /N ED
  1 N eq {
    {0 1} 0 0 trans name (1) {PlainIfc} {sc} NewCompIfc
    (1) (2) IfcCopy
    (2) (N) IfcAlias
  }{
    N -1 1 {
      inttostr
      {0 1} 0 0 absorb name 6 -1 roll {PlainIfc} {sc} NewCompIfc
    } for
    N inttostr (N) IfcAlias
  } ifelse
  end
  pop
  DebugEnd
} bind def
/IfcCopy {
  2 copy IfcName exch IfcName load dup
  length dict copy def
  name exch NodeName name 3 -1 roll NodeName
  tx@NodeDict begin
    load dup length dict copy def
  end
} bind def
/IfcAlias {
  2 copy IfcName exch IfcName load def
  tx@NodeDict begin
    name exch NodeName name 3 -1 roll NodeName load def
  end
} bind def
/CompAlias {
  2 copy cvn dup currentdict exch known {
    load def
  } {
    pop
  } ifelse
  tx@NodeDict begin
  1 {
    3 copy inttostr dup
    3 1 roll 2 copy NodeName
    currentdict exch known {
      NodeName load 3 1 roll NodeName ED
      1 add
    } {
      pop (N) NodeName load 3 1 roll
      pop (N) NodeName ED
      pop exit
    } ifelse
  } loop
  mark (A) (B) (@A) (@B) (Center) (Label) (Rotref)
       (TrefA) (TrefB) (@TrefA) (@TrefB) (Ext) (Origin)
  counttomark {
    counttomark 3 add -2 roll 2 copy counttomark 1 add 2 roll
    3 -1 roll dup 4 1 roll NodeName dup
    currentdict exch known {
      load 3 1 roll exch NodeName ED
    } {
      pop pop pop
    } ifelse
  } repeat pop
  exch 1 1 8 {
    3 copy
    (Ext) exch 5 string cvs strcat dup 3 1 roll
    NodeName 3 1 roll NodeName
    dup currentdict exch known {
      load def pop
    } {
      pop pop pop exit
    } ifelse
  } for
  pop pop
  end
} bind def
/GetPlaneVec {
  (GetPlaneVec) DebugBegin
  cvn load begin
    IfcName load begin
      currentdict /RX known {
        RX RY CompMtrx dtransform CM idtransform
        neg exch
      } {
        DX DY CompMtrx dtransform CM idtransform
      } ifelse
    end
  end
  DebugEnd
} bind def
/GetIfcCenter {
  (GetIfcCenter) DebugBegin
  dup type /stringtype eq not {
    dup xcheck not {
      0 get (C) exch
    } {
      exec pop pop pop
    } ifelse
  } if
  cvn load begin
    IfcName load begin
      currentdict /RX known {
        X RX sub Y RY sub
      } {
        X Y
      } ifelse
      CompMtrx transform CM itransform
    end
  end
  DebugEnd
} bind def
/GetIfcCenterCorr {
  (GetIfcCenterCorr) DebugBegin
  cvn load begin
    IfcName load begin
      currentdict /XCorr known {
        XCorr YCorr
      }{
        X Y
      } ifelse
      currentdict /RX known {
        RX neg RY neg VecAdd
      } if
      CompMtrx transform CM itransform
    end
  end
  DebugEnd
} bind def
/TransformInVec {
  (TransformInVec) DebugBegin
  3 1 roll
  GetIfcCenter 4 2 roll
  GetIfcCenter 5 -2 roll
  @ABVect
  3 -1 roll exec 2 copy 6 2 roll
  0 eq exch 0 eq and not {
    exch atan matrix rotate dtransform
  } {
    4 2 roll pop pop
  } ifelse
  ToVec
  DebugEnd
} bind def
/TransformStartPos {
  (TransformStartPos) DebugBegin
  exec 2 copy 6 2 roll 0 eq exch 0 eq and not
  3 1 roll GetIfcCenter 4 2 roll
  GetIfcCenter 5 2 roll {
    2 copy 8 2 roll
    @ABVect exch atan matrix rotate dtransform
    VecAdd
  } {
    6 2 roll pop pop pop pop
  } ifelse
  ToVec
  DebugEnd
} bind def
/GetNearestPlane {
  (GetNearestPlane) DebugBegin
  3 copy 1 exch GetIfcCenter @ABDist /dist ED /nearestPlane 1 def
  dup cvn load /N get 2 1 3 -1 roll {
    4 copy exch GetIfcCenter @ABDist dup dist lt {
      /dist ED /nearestPlane ED
    } {
      pop pop
    } ifelse
  } for
  pop pop pop nearestPlane
  DebugEnd
} bind def
/PushAmbCompPlanesOnStack {
 (PushAmbCompPlanesOnStack) DebugBegin
  currentdict /outToPlane undef
  PN IfcCnt eq not {
    exch dup 3 1 roll % nextifc ambcomp nextifc
    dup xcheck not {
      0 get (C) exch
    } {
      exec pop pop pop
    } ifelse
    [ 3 1 roll ] cvx /outToPlane ED
  } if
  /IfcCntTmp IfcCnt def
  aload pop /draw ED /name ED
  name cvn load /N get dup /N ED
  1 eq { /draw true def } if
  currentdict /Curr known {
    /CurrTmp /Curr load def
    /CurrVecTmp /CurrVec load def
  } {
    /CurrTmp /CurrLow load def
    /CurrVecTmp /CurrVecLow load def
  } ifelse
  PN 1 eq {
    [ (C) name name GetRefIndex trans draw] cvx
    name /outToPlane load GetNextPlane
    dup 0 eq not {
      [ exch name bgRefIndex trans draw ] cvx exch
      /IfcCntTmp IfcCntTmp 1 add def
    } {
      pop
    } ifelse
  }{
    CurrTmp name GetNearestPlane dup /firstPlane ED
    name isAmbiguousIfc not {
      firstPlane name
      name firstPlane GetIfcMode
      connectifc { bgRefIndex }{ name GetRefIndex } ifelse
      CurrTmp CurrVecTmp
      10 dict begin HandleInterface end pop
      ToVec /CurrVecTmp ED ToVec /CurrTmp ED
      [ firstPlane name
      connectifc {
        bgRefIndex
      }{
        name GetRefIndex
      } ifelse
      name firstPlane GetIfcMode
      true ] cvx
      /IfcCntTmp IfcCntTmp 1 add def
    } if
    PN IfcCnt eq {
      [ (C) name
      name GetRefIndex
      trans draw ] cvx
      IfcCntTmp IfcCnt gt { exch } if
    }{
      beamdiffractionorder null eq not name cvn load /grating get and {
        beamdiffractionorder dup 0 eq { pop () } if
        (C) exch 20 string cvs strcat
        dup (P@) exch strcat cvn name cvn load exch known not {
          pop beamdiffractionorder dup sign neg 1 {
            (C) exch 5 string cvs dup 3 1 roll strcat
            dup (P@) exch strcat cvn name cvn load exch known {
              3 -1 roll pop
              (Diffraction order ) beamdiffractionorder 5 string cvs strcat
              ( is not defined, using ) 4 -1 roll strcat strcat Warning
              exit
            } {
              pop
            } ifelse
          } for
        } if
        /@@centerifc ED
        mark @@centerifc name name GetRefIndex
        beamdiffractionorder 0 eq {
          trans
        }{
          name @@centerifc GetIfcMode refltrans eq {
            refltrans
          }{
            refl
          } ifelse
        } ifelse
      }{
        /@@centerifc (C) def
        [ @@centerifc name
        name GetRefIndex
        beammode auto eq {
          CurrVecTmp @@centerifc name GetPlaneVec
          name @@centerifc GetIfcMode refltrans eq { -90 matrix rotate dtransform } if
          NormalVec outToPlane GetIfcCenter @@centerifc name GetIfcCenter @ABVect DotProd
          0 lt {
            trans
          }{
            name @@centerifc GetIfcMode
            refltrans eq {
              refltrans
            }{
              refl
            } ifelse
          } ifelse
        } {
          beammode dup refl eq {
            pop name @@centerifc GetIfcMode dup refltrans eq not { pop refl } if
          } if
        } ifelse
      } ifelse
      dup 6 1 roll
      IfcCntTmp IfcCnt eq { true }{ draw } ifelse
      ] cvx
      @@centerifc name 4 -1 roll
      connectifc { bgRefIndex }{ name GetRefIndex } ifelse
      CurrTmp CurrVecTmp
      10 dict begin HandleInterface end pop
      ToVec /CurrVecTmp ED ToVec /CurrTmp ED
      name /outToPlane load GetNextPlane
      dup dup name isAmbiguousIfc exch 0 eq or not {
        [ exch name bgRefIndex trans draw ] cvx exch
        firstPlane name isAmbiguousIfc not { 3 -1 roll } if
        /IfcCntTmp IfcCntTmp 1 add def
      } {
        pop
        exec 3 -1 roll pop bgRefIndex 3 1 roll [ 6 1 roll ] cvx
        firstPlane name isAmbiguousIfc not { exch } if
      } ifelse
    } ifelse
  } ifelse
  /IfcCnt IfcCntTmp def
  DebugEnd
} bind def
/GetNextPlane {
  (GetNextPlane) DebugBegin
  2 copy (C) 3 -1 roll
  GetIfcCenter 3 -1 roll
  exec GetIfcCenter
  4 2 roll 4 copy @ABVect ToVec /Vec ED
  @ABDist /centerDist ED
  /sprod 1 def
  /nextPlane 0 def
  exch dup 3 1 roll
  cvn load dup /ambIfc get /ambIfc ED /N get 1 1 3 -1 roll {
   dup ambIfc eq not {
      3 copy 3 -1 roll 2 copy
      GetPlaneVec Vec 4 2 roll NormalVec
      Vec DotProd dup sprod lt 5 2 roll
      GetIfcCenter 3 -1 roll exec GetIfcCenter @ABDist
      centerDist lt and
      centerDist -1 eq { pop dup 0 gt } if
      { /sprod ED /nextPlane ED } { pop pop } ifelse
    } {
      pop
    } ifelse
  } for
  pop pop nextPlane
  DebugEnd
} bind def
/TraceBeam {
  (Tracebeam) DebugBegin
  AngToVec /InVec ED /StartPoint ED
  /oldbeaminsidelast currentdict /beaminsidelast known {
    beaminsidelast
  } {
    false
  } ifelse def
  exec
  connectifc {
    /nbeam bgRefIndex def
  } if
  /startinside startinside beaminsidefirst or def
  /stopinside stopinside beaminsidelast or def
  /PrevCorrect false def
  PrearrangePlanes
  PushAllPlanesOnStack
  currentdict /lastVecTmp known {
    lastVecTmp beamangle matrix rotate dtransform ToVec
  } {
    counttomark 2 ge beamalign relative eq and {
      2 copy /InVec load TransformInVec
    } {
      /InVec load
    } ifelse
  } ifelse
  /CurrVec ED
  currentdict /lastBeamPointTmp known {
    /lastBeamPointTmp load /Curr ED
  }{
    counttomark 2 ge {
      2 copy /StartPoint load  TransformStartPos
    } {
      /StartPoint load
    } ifelse
    /Curr ED
  } ifelse
  counttomark /IfcCnt ED
  /n1 bgRefIndex def
  /PN 1 def
  (start looping) DebugMsg
  {
    PN IfcCnt gt {
      exit
    } if
    (checked) DebugMsg
    beampathcount 0 eq {
      cleartomark mark exit
    } if
    dup xcheck not {
      PushAmbCompPlanesOnStack
    } if
    exec
    /draw ED /Mode ED /n2 ED 2 copy /CompName ED /IfcNum ED
    GetIfcCenter ToVec /CurrCenter ED
    Curr CurrVec
    connectifc PrevCorrect PN 2 gt and PN 2 eq or and {
      CurrVec CurrCenter PrevCenter PrevMode
      currentdict /relAngle known
      { relAngle } { 0 } ifelse connectInterfaces
      /relAngle ED
    } if
    CompName cvn load begin
      currentdict /adjustRel known aligntovector and {
        IfcNum IfcName load begin
          currentdict /RX known not {
            2 copy neg exch CM dtransform CompMtrx idtransform
            /DY ED /DX ED
          } if
        end
      } if
    end
    IfcNum CompName Mode n2 8 4 roll HandleInterface
    missed eq {
      counttomark PN 1 sub 3 mul sub {pop} repeat
      (The beam missed an interface) Warning exit
      exit
    } if
    PN 1 eq {
      pop pop
      /draw beaminsidefirst oldbeaminsidelast xor def
    } {
      ToVec /CurrVec ED
    } ifelse
    2 copy
    ToVec /Curr ED
    draw PN beampathskip 1 add gt and
    counttomark 3 roll
    /PrevCenter /CurrCenter load def
    /lastBeamPointTmp /Curr load def
    currentdict /lastVecTmp known {
      /prevVecTmp /lastVecTmp load def
      /lastVecTmp /CurrVec load def
    } {
      /CurrVec load dup /lastVecTmp ED /prevVecTmp ED
    } ifelse
    /PrevMode Mode def
    CompName cvn load /correct get /PrevCorrect ED
    PN IfcCnt eq {
      exit
    } {
      CurrVec 0 eq exch 0 eq and {
        IfcCnt PN sub {pop} repeat
        (Total internal reflection occured, this is not supported)
        Warning
        exit
      } if
      beampathcount 1 add PN eq {
        IfcCnt PN sub {pop} repeat
        exit
      } if
      /PN PN 1 add def
    } ifelse
  } loop
  DebugEnd
} bind def
/sign {
    0 ge { 1 } { -1 } ifelse
} bind def
/Chirality {
  4 -1 roll mul 3 1 roll mul sub sign
} bind def
/TraceInterfacePath {
  tx@IntersectDict begin
    /ArrowA { {currentpoint} stopped {moveto}{pop pop pop pop} ifelse } def
    {} TraceCurveOrPath
    currentdict /ArrowA undef
  end
} bind def
/TraceAndFillWideBeam {
  (TraceAndFillWideBeam) DebugBegin
  AngToVec /InvecLow ED /StartLow ED
  AngToVec /InvecUp ED /StartUp ED
  exec
  connectifc {
    /nbeam bgRefIndex def
  } if
  /startinside startinside beaminsidefirst or def
  /stopinside stopinside beaminsidelast or def
  /DrawnSegm 0 def
  /PrevCorrect false def
  PrearrangePlanes
  PushAllPlanesOnStack
  currentdict /lastVecTmpUp known
  currentdict /lastVecTmpLow known and {
    /CurrVecLow lastVecTmpLow beamangle matrix rotate dtransform ToVec def
    /CurrVecUp lastVecTmpUp beamangle matrix rotate dtransform ToVec def
  }{
    beamalign relative eq counttomark 2 ge and {
      2 copy /InvecLow load TransformInVec /CurrVecLow ED
      2 copy /InvecUp load TransformInVec /CurrVecUp ED
    } {
      /CurrVecLow /InvecLow load def
      /CurrVecUp /InvecUp load def
    } ifelse
  } ifelse
  currentdict /lastBeamPointTmpLow known
  currentdict /lastBeamPointTmpUp known and {
    /lastBeamPointTmpLow load /CurrLow ED
    /lastBeamPointTmpUp load /CurrUp ED
    loadbeam not beamdiv 0 eq not and {
      CurrVecLow CurrVecUp Chirality
      CurrLow CurrUp @ABVect CurrVecLow CurrVecUp VecAdd Chirality 0 lt { neg } if
      beamdiv sign eq not {
        /CurrVecLow load /CurrVecUp load /CurrVecLow ED /CurrVecUp ED
      } if
    } if
  } {
    counttomark 2 ge {
      2 copy /StartLow load TransformStartPos /CurrLow ED
      2 copy /StartUp load TransformStartPos /CurrUp ED
    } {
      /StartLow load /CurrLow ED
      /StartUp load /CurrUp ED
    } ifelse
  } ifelse
  /PrevVecUp /CurrVecUp load def
  /PrevVecLow /CurrVecLow load def
  counttomark /IfcCnt ED
  /n1 bgRefIndex def
  /CurrR false def
  /CurrPath false def
  /CurrUpT false def
  /CurrLowT false def
  /ret missed def
  /PN 1 def
  {
    PN IfcCnt gt {
      exit
    } if
    beampathcount 0 eq {
      cleartomark mark exit
    } if
    dup xcheck not {
      PushAmbCompPlanesOnStack
    } if
    exec
    PN beampathskip 1 add gt and /draw ED
    /Mode ED /n2 ED 2 copy /CompName ED /IfcNum ED
    GetIfcCenter ToVec /CurrPCenter ED
    /oldn1 n1 def
    CompName cvn load /adjustRel known aligntovector and {
      connectifc PrevCorrect PN 2 gt and PN 2 eq or and {
        CurrVecUp CurrVecUp CurrPCenter PrevPCenter PrevMode
        currentdict /relAngleUp known { relAngleUp } { 0 } ifelse
        connectInterfaces pop
        CurrVecLow CurrVecLow CurrPCenter PrevPCenter PrevMode
        currentdict /relAngleLow known { relAngleLow } { 0 } ifelse
        connectInterfaces pop
      } {
        CurrVecUp CurrVecLow
      } ifelse
      VecAdd NormalizeVec
      CompName cvn load begin
        IfcNum IfcName load begin
          currentdict /RX known not {
            CM dtransform CompMtrx idtransform
            /DX ED neg /DY ED
          } {
            pop pop
          } ifelse
        end
      end
    } if
    CurrUp CurrVecUp
    connectifc PrevCorrect PN 2 gt and PN 2 eq or and {
      CurrVecUp CurrPCenter PrevPCenter PrevMode
      currentdict /relAngleUp known { relAngleUp } { 0 } ifelse
      connectInterfaces /relAngleUp ED
    } if
    /PrevUp /CurrUp load def
    /PrevUpT /CurrUpT load def
    /PrevPath /CurrPath load def
    IfcNum CompName Mode n2 8 4 roll HandleInterface
    dup /ret ED
    missed eq {
      counttomark {pop} repeat
      (The upper beam missed an interface) Warning exit
    } if
    ToVec /CurrVecUp ED
    ToVec /CurrUp ED
    currentdict /isectT known currentdict /isectPath known and {
      /CurrUpT isectT def
      /CurrPath isectPath def
    } if
    /n1 oldn1 def
    /PrevLow /CurrLow load def
    /PrevLowT /CurrLowT load def
    CurrLow CurrVecLow
    connectifc PrevCorrect PN 2 gt and PN 2 eq or and  {
      CurrVecLow CurrPCenter PrevPCenter PrevMode
      currentdict /relAngleLow known { relAngleLow } { 0 } ifelse
      connectInterfaces /relAngleLow ED
    } if
    IfcNum CompName Mode n2 8 4 roll HandleInterface
    dup missed eq {
      /ret ED
      (The lower beam missed an interface) Warning
      counttomark {pop} repeat exit
    } if
    tir eq ret tir eq or {
      /ret tir def
    } {
      /ret ok def
    } ifelse
    ToVec /CurrVecLow ED
    ToVec /CurrLow ED
    currentdict /isectT known {
      /CurrLowT isectT def
    } if
    /PrevR CurrR def
    PrevR type /realtype eq {
      /CurrCenter load /PrevCenter ED
    } if
    IfcNum CompName isCurvedIfc {
      IfcNum CompName LoadIfc
      tx@Dict begin Pyth end /CurrR ED
      ToVec /CurrCenter ED
    } {
      /CurrR false def
      /CurrCenter false def
    } ifelse
    IfcNum CompName isPathIfc not {
      /CurrPath false def
      /CurrLowT false def
      /CurrUpT false def
    } if
    PN 1 gt currentdict /fillBeam known and {
      draw {
        /DrawnSegm DrawnSegm 1 add def
        PrevUp moveto CurrUp lineto
        IfcNum CompName isCurvedIfc {
          CurrCenter CurrUp CurrLow
          4 copy 3 -1 roll eq 3 1 roll eq and {
            6 {pop} repeat
          } {
            TangentCrosspoint
            CurrLow CurrR arct
          } ifelse
        } {
          IfcNum CompName isPathIfc {
            CurrPath CurrUpT CurrLowT TraceInterfacePath
          } {
            CurrLow lineto
          } ifelse
        } ifelse
        PrevLow lineto
        PrevPath type /booleantype eq not {
          PrevPath PrevLowT PrevUpT TraceInterfacePath
        } {
          PrevR type /booleantype eq not {
            PrevCenter PrevLow PrevUp
            4 copy 3 -1 roll eq 3 1 roll eq and {
              6 {pop} repeat
            } {
              TangentCrosspoint
              PrevUp PrevR arct
            } ifelse
          } {
            PrevUp lineto
          } ifelse
        } ifelse
      } if
      Mode refl eq draw and
      draw not DrawnSegm 0 gt and or {
        fillBeam newpath
        /DrawnSegm 0 def
      } if
    } if
    PN 1 eq {
      /CurrVecUp /PrevVecUp load def
      /CurrVecLow /PrevVecLow load def
    } if
    strokeBeam {
      CurrUp draw CurrLow draw counttomark 1 add 6 roll
    } if
    PN IfcCnt eq ret tir eq or
    beampathcount 1 add PN eq or {
      DrawnSegm 0 gt currentdict /fillBeam known and {
        fillBeam newpath
        /DrawnSegm 0 def
      } if
      IfcCnt PN sub {pop} repeat
      ret tir eq {
        (Total internal reflection occured, this is not supported)
        Warning
      } if
      exit
    } if
    /PN PN 1 add def
    /PrevVecUp /CurrVecUp load def
    /PrevVecLow /CurrVecLow load def
    /PrevPCenter /CurrPCenter load def
    /PrevMode Mode def
    CompName cvn load /correct get /PrevCorrect ED
  } loop
  DrawnSegm 0 gt currentdict /fillBeam known and {
    fillBeam newpath
    /DrawnSegm 0 def
  } if
  ret missed eq not {
    CurrLow CurrUp @ABVect % from Low to Up
    PrevVecUp PrevVecLow VecAdd
    2 copy 6 2 roll
    Chirality 0 lt
    3 1 roll 2 copy pop -1e-5 lt
    3 1 roll exch 1e-5 lt exch 0 lt and or xor {
      /lastBeamPointTmpUp /CurrLow load def
      /lastBeamPointTmpLow /CurrUp load def
      /lastVecTmpUp /CurrVecLow load def
      /lastVecTmpLow /CurrVecUp load def
    } {
      /lastBeamPointTmpLow /CurrLow load def
      /lastBeamPointTmpUp /CurrUp load def
      /lastVecTmpUp /CurrVecUp load def
      /lastVecTmpLow /CurrVecLow load def
    } ifelse
    /lastVecTmpUp load /lastVecTmpLow load
    /prevVecLow ED /prevVecUp ED
  } if
  DebugEnd
} bind def
/DrawbeamPrepare {
  {
    counttomark 6 le { exit } if
    3 index not { pop pop pop }{ exit } ifelse
  } loop
  {
    counttomark 3 le { exit } if
    counttomark 3 sub index not {
      counttomark -3 roll pop pop pop
    }{
      exit
    } ifelse
  } loop
} bind def
/DrawbeamSimple {
  pop 5 copy 3 -1 roll pop
  ArrowA pop pop pop pop
  counttomark 3 idiv -1 2 {
    pop {
      lineto
    }{
      moveto
    } ifelse
  } for
  {CP 4 2 roll ArrowB lineto pop pop } {moveto} ifelse
} bind def
/DrawbeamArrowInside {
  6 copy pop
  /y1 ED /x1 ED pop /y2 ED /x2 ED
  /Alpha y2 y1 sub x2 x1 sub Atan def
  pop 3 -1 roll 5 1 roll
  ArrowA
  x1 Alpha cos arrowlength mul add
  y1 Alpha sin arrowlength mul add
  5 -1 roll 3 1 roll true
  /N N 1 sub def
  N {
    6 copy pop
    /y1 ED /x1 ED pop /y2 ED /x2 ED /draw ED
    x1 y1 x2 y2 @ABDist dup
    arrowminlength ge
    exch arrowmaxlength dup 0 lt
    3 1 roll le or and {
      x1 y1
      arrowpos 1 gt {
        /Alpha y2 y1 sub x2 x1 sub Atan def
        /dArrowPos dArrowPosStart abs def
        /ArrowPos ArrowPosStart def
        arrowno {
          /ArrowPos ArrowPos dArrowPos add def
          x1 Alpha cos ArrowPos mul add
          y1 Alpha sin ArrowPos mul add
          6 index { ArrowInside } if
          pop pop
        } repeat
      }{
        arrowno 1 gt {
          1.0 arrowno 1.0 add div
        }{
          dArrowPosStart
        } ifelse /dArrowPos ED
        /ArrowPos ArrowPosStart def
        arrowno {
          /ArrowPos ArrowPos dArrowPos add def
          x2 x1 sub ArrowPos mul x1 add
          y2 y1 sub ArrowPos mul y1 add
          6 index { ArrowInside } if
          pop pop
        } repeat
      } ifelse
      pop pop
    } if
    draw {Lineto}{moveto} ifelse
  } repeat
  {CP 4 2 roll ArrowB lineto pop pop } {moveto} ifelse
} bind def
/isAmbiguous {
  cvn load dup /ambiguous known {
    /ambiguous get
  } {
    pop false
  } ifelse
} bind def
/isAmbiguousIfc {
  cvn load dup /ambiguous known {
    /ambIfc get eq
  } {
    pop pop false
  } ifelse
} bind def
/isCurvedIfc {
  cvn load begin
    IfcName load /RX known
  end
} bind def
/isPathIfc {
  cvn load begin
    IfcName load /Path known
  end
} bind def
/HandleInterface {
  (HandleInterface) DebugBegin
  /Yin ED /Xin ED /Y0 ED /X0 ED /n2 ED /mode ED
  currentdict /isectT undef currentdict /isectPath undef
  2 copy 2 copy LoadIfc % IfcNum name IfcNum name path
  dup type /arraytype eq { % is an path interface
    dup /isectPath exch def
    3 1 roll pop pop PathInterface % IfcNum name t X0' Y0' Xout Yout status
    dup missed eq not { 6 -1 roll /isectT exch def } if
  } {
    6 -2 roll
    isCurvedIfc { CurvedInterface }{ PlainInterface } ifelse
  } ifelse
  dup missed eq not useNA connectifc not and and {
    7 3 roll 2 copy 9 2 roll
    4 2 roll 2 copy
    %% X0' Y0' Xout Yout status X0' Y0' IfcNum CompName IfcNum CompName
    cvn load begin IfcName load dup /NAlow get exch /NAup get end
    2 copy lt {
      4 2 roll 2 copy LoadIfc NormalizeVec
      6 -2 roll isCurvedIfc {
        neg exch
      } if
      %% ... X0' Y0' NAlow NAup X Y dXp dYp
      8 -2 roll 6 -2 roll
      %% ... NAlow NAup dXp dYp X0' Y0' X Y
      @ABVect DotProd
      dup 4 -1 roll ge 3 1 roll ge and not
      {
        pop missed
      } if
    }{
      6 {pop} repeat
    } ifelse
  } {
    7 -2 roll pop pop
  } ifelse
  DebugEnd
} bind def
/LoadIfc {
  (LoadIfc) DebugBegin
  cvn load begin
    IfcName load begin
      currentdict /Path known {
        Path TransformPath
      } {
        X Y
        CompMtrx transform CM itransform
        currentdict /RX known { RX RY }{ DX DY } ifelse
        CompMtrx dtransform CM idtransform
      } ifelse
    end
  end
  DebugEnd
} bind def
/isFreeray {
  cvn load /n known
} bind def
/compIsKnown {
  dup type /stringtype eq { cvn } if
  tx@OptexpDict exch known
} bind def
/PrearrangePlanes {
  (PrearrangePlanes) DebugBegin
  counttomark dup 2 lt {
    dup 0 eq {
      (Found no component on stack, drawing no beam) PrintWarning
    }{
      exch dup
      compIsKnown {
        dup isFreeray {
          asc exch 3 -1 roll
        }{
          OneFiberCompWarning
          pop
        } ifelse
      }{
        CompUnknownWarning
      } ifelse
    } ifelse
    /N 0 def
  }{
    /N ED
    /CompA ED dup /CompB ED
    CompA compIsKnown CompB compIsKnown and {
      CompA isFreeray {
        CompA isAmbiguous {
          amb dup CompA
        } {
          CompB isAmbiguous {
            1 CompA GetIfcCenter (C) CompB GetIfcCenter @ABDist
            (N) CompA GetIfcCenter (C) CompB GetIfcCenter @ABDist
          } {
            1 CompA GetIfcCenter
            1 CompB GetIfcCenter
            (N) CompB GetIfcCenter
            true OrderNodes exch pop
            (N) CompA GetIfcCenter
            1 CompB GetIfcCenter
            (N) CompB GetIfcCenter
            true OrderNodes exch pop
          } ifelse
          le { desc } { asc } ifelse dup CompA
        } ifelse
        counttomark 2 roll
      }{
        FiberCompWarning
        counttomark 1 sub { pop } repeat
        /N 0 def
      } ifelse
    }{
      /N 0 def
      CompA compIsKnown not {CompA}{CompB} ifelse
      CompUnknownWarning
    } ifelse
  } ifelse
  2 1 N {
    /i ED exch /CompB ED
    CompB compIsKnown not {
      counttomark i 1 sub 2 mul 1 add sub { pop } repeat
      CompB CompUnknownWarning
      exit
    } if
    CompB isFreeray not {
      counttomark i 1 sub 2 mul 1 add sub { pop } repeat
      FiberCompWarning
      exit
    } if
    CompB isAmbiguous not {
      dup desc eq { 1 } { dup amb eq { (C) }{ (N) } ifelse } ifelse
      CompA GetIfcCenter
      1 CompB GetIfcCenter
      (N) CompB GetIfcCenter false OrderNodes dup dup
      4 -1 roll CompA exch 5 -1 roll CompB exch
      i 2 eq {
        4 copy 4 2 roll AdjustRelRot
      } if
      AdjustRelRot
    } {
      i 2 eq {
        CompB amb CompA desc AdjustRelRot
      } if
      pop amb dup
    } ifelse
    CompB /CompA CompB def
    counttomark 2 roll
  } for pop
  DebugEnd
} bind def
/AdjustRelRot {
  (AdjustRelRot) DebugBegin
  exch dup cvn load /adjustRel known aligntovector not and {
    dup dup 4 2 roll isAmbiguous {
      exch pop (C)
    }{
      desc eq { (N) }{ 1 } ifelse
    } ifelse
    exch GetIfcCenter 5 3 roll
    exch dup 3 1 roll isAmbiguous {
      pop (C)
    }{
      desc eq { 1 }{ (N) } ifelse
    } ifelse
    exch GetIfcCenter
    @ABVect exch atan exch
    cvn load begin
      adjustRel {
        matrix rotate CompMtrx matrix concatmatrix /CompMtrx ED
        /adjustRel false def
      } {
        pop
      } ifelse
    end
  } {
    pop pop pop pop
  } ifelse
  DebugEnd
} bind def
/PushAllPlanesOnStack {
  (PushAllPlanesOnStack) DebugBegin
  counttomark 2 div cvi /@N ED
  1 1 @N {
    /last false def
    /first false def
    dup 1 eq {
      /first true def pop beaminsidefirst
    } {
      @N eq {
        beaminsidelast
        /last true def
      } {
        beaminside
      } ifelse
    } ifelse
    exch load dup dup
    /forcebeaminside get {
      3 -1 roll pop true
    } {
      dup /allowbeaminside get 4 -1 roll and
    } ifelse
    /drawinside ED
    /ambiguous get {
      /name get drawinside [ 3 1 roll ]
      counttomark 1 roll pop
    } {
      begin
        desc eq {
          N N -1 1 1
        } {
          1 1 1 N N
        } ifelse
        first {
          startinside not {
            5 -2 roll
            pop pop
            2 copy 5 2 roll
          } {
            startinsidecount 0 gt N startinsidecount sub 1 gt and {
              3 -1 roll dup 4 1 roll
              N 1 sub startinsidecount sub mul
              6 -2 roll pop add dup 5 2 roll
            } if
          } ifelse
        } if
        last stopinsidecount 0 gt N stopinsidecount sub 1 gt and and {
          % 1 1 1 N N
          3 -1 roll dup 4 1 roll stopinsidecount mul
          6 -1 roll dup 7 1 roll add 3 1 roll pop pop dup
        } if
        5 1 roll
        {
          3 1 roll 2 copy 5 -1 roll
          dup 3 1 roll
          eq first not and {
            true
          } {
            drawinside
          } ifelse
          exch dup 4 -1 roll eq {
            bgRefIndex
          }{
            name GetRefIndex
          } ifelse
          exch inttostr exch
          3 1 roll name
          4 1 roll
          dup IfcName load /mode get
          3 1 roll 5 1 roll
          [ 6 1 roll ] cvx counttomark 1 roll
          last {
            savebeampoints 1 ge stopinside not and
            savebeampoints 1 lt beaminsidelast not and or {
              exit
            } if
          } if
        } for pop pop
      end
    } ifelse
  } for
  DebugEnd
  counttomark 1 eq { pop } if
} bind def
/IfcName {
  inttostr (P@) exch strcat cvn
} bind def
/GetIfcMode {
  exch cvn load begin
    IfcName load /mode get
  end
} bind def
/NodeName {
  dup /stringtype eq not { inttostr } if
  strcat (N@) exch strcat cvn
} bind def
/OrderNodes {
   7 1 roll 6 -2 roll 2 copy 8 2 roll
   @ABDist 5 1 roll @ABDist 2 copy gt {
       pop asc exch
   } {
       exch pop desc exch
   } ifelse
   3 -1 roll not {
       pop
   } if
} bind def
/NormalVec {
  neg exch 2 copy 6 2 roll DotProd 0 gt {
    -1 mul exch -1 mul exch
  } if
  NormalizeVec
} bind def
/DotProd {
    3 -1 roll mul 3 1 roll mul add
} bind def
/VecAngle {
  4 copy 4 copy DotProd 5 1 roll
  tx@Dict begin
    Pyth 3 1 roll Pyth
  end mul
  div Acos
  5 2 roll mul 4 1 roll 3 -1 roll mul 3 -1 roll sub
  0 le { -1 }{ 1 } ifelse mul
} bind def
/VecAdd {
    3 -1 roll add 3 1 roll add exch
} bind def
/VecSub {
    neg 3 -1 roll add 3 1 roll neg add exch
} bind def
/VecScale {
  dup 4 -1 roll mul 3 1 roll mul
} bind def
/ToVec {
    ToPnt cvx
} bind def
/ToPnt {
    [ 3 1 roll ]
} bind def
/AngToVec {
    dup cos exch sin ToVec
} bind def
/NormalizeVec {
  2 copy
  tx@Dict begin
    Pyth
  end
  dup 3 1 roll div 3 1 roll div exch
} bind def
/@ABVect {
  3 -1 roll exch sub 3 1 roll sub exch
} bind def
/@ABDist {
  3 -1 roll sub dup mul 3 1 roll sub dup mul add sqrt
} bind def
/@InterLines {
  tx@EcldDict begin
    EqDr /D1c exch def /D1b exch def /D1a exch def
    EqDr /D2c exch def /D2b exch def /D2a exch def
    D1a D2b mul D1b D2a mul sub dup
    ZeroEq { % parallel lines
      pop 0 0 missed
    }{
      /Det exch def
      D1b D2c mul D1c D2b mul sub Det div
      D1a D2c mul D2a D1c mul sub Det div
      ok
    } ifelse
  end
} bind def
/@GetCenter {
  tx@NodeDict begin load GetCenter end
} bind def
/@NewNode {
  tx@NodeDict begin
    false exch 10 {InitPnode } NewNode
  end
} bind def
/RefractVec {
  (RefractVec) DebugBegin
  TransformRefIndex exch TransformRefIndex exch div /n ED
  /Ynorm ED /Xnorm ED
  NormalizeVec /Yin ED /Xin ED
  n abs 1 eq {
    Xin Yin
  }{
    /costheta1 Xnorm Ynorm Xin neg Yin neg DotProd def
    1 n dup mul 1 costheta1 dup mul sub mul sub
    dup 0 lt {
      pop 0 0
    } {
      sqrt /costheta2 ED
      n Xin mul n Yin mul
      n costheta1 mul costheta2 sub dup
      Xnorm mul exch Ynorm mul VecAdd
    } ifelse
  } ifelse
  DebugEnd
} bind def
/ReflectVec {
  (ReflectVec) DebugBegin
  /Ynorm ED /Xnorm ED NormalizeVec /Yin ED /Xin ED
  /costheta1 Xnorm Ynorm Xin neg Yin neg DotProd def
  Xin Yin 2 costheta1 mul dup Xnorm mul exch Ynorm mul VecAdd
  DebugEnd
} bind def
/ReflectGratVec {
  (ReflectGratVec) DebugBegin
  /Ynorm ED /Xnorm ED NormalizeVec /Yin ED /Xin ED
  /costheta1 Xnorm Ynorm Xin neg Yin neg DotProd def
  Xin Yin -2 costheta1 mul dup Xnorm mul exch Ynorm mul VecAdd
  DebugEnd
} bind def
/CurvedInterface {
  (CurvedInterface) DebugBegin
  2 copy /Yr ED /Xr ED
  tx@Dict begin Pyth end /radius ED /Yp ED /Xp ED
  /X0n X0 Xp sub def /Y0n Y0 Yp sub def
  tx@EcldDict begin
    X0n Y0n 2 copy 2 copy Xin 3 -1 roll add Yin 3 -1 roll add
    2 copy 6 2 roll EqDr radius InterLineCircle
  end
  4 copy
  0 eq 3 {exch 0 eq and} repeat {
    missed
  } {
    4 copy
    Xr neg Yr neg 2 copy
    8 -2 roll @ABDist
    5 1 roll @ABDist
    gt {
      4 2 roll
    } if pop pop
    Xp Yp VecAdd
    2 copy Xp Yp 4 2 roll @ABVect exch neg Xin Yin 4 2 roll NormalVec
    Xin Yin 4 2 roll
    mode trans eq {
      n1 n2 RefractVec
      2 copy 0 eq exch 0 eq and { tir } { ok } ifelse
    } {
      ReflectVec ok
    } ifelse /n1 n2 def
    5 -2 roll 2 copy 7 2 roll X0 Y0 @ABVect Xin Yin DotProd 0 lt
    PN 1 gt and {
      pop missed
    } if
  } ifelse
  DebugEnd
} bind def
/PlainInterface {%
  (PlainInterface) DebugBegin
  /dYp ED /dXp ED /Yp ED /Xp ED
  Xp Yp Xp dXp add Yp dYp add X0 Y0 X0 Xin add Y0 Yin add
  @InterLines missed eq {
    0 0 missed
  } {
    Xin Yin Xin Yin dXp dYp
    mode refltrans eq {
      neg exch NormalVec ReflectVec ok
    } {
      NormalVec
      mode trans eq {
        n1 n2 RefractVec
        2 copy 0 eq exch 0 eq and { tir } { ok } ifelse
      } {
        ReflectVec ok
      } ifelse
    } ifelse
    /n1 n2 def
    5 -2 roll 2 copy 7 2 roll X0 Y0 @ABVect Xin Yin DotProd 0 lt
    PN 1 gt and {
      pop missed
    } if
  } ifelse
  DebugEnd
} bind def
/PathInterface {
  (PathInterface) DebugBegin
  [ [X0 Y0] [X0 Xin add Y0 Yin add] ] exch
  tx@IntersectDict begin IntersectLinePath end % [pathseg] t [isect]
  dup length 0 eq {
    pop pop pop 0 0 missed
  } {
    aload pop
    Xin Yin Xin Yin
    8 -2 roll exch % I.x I.y Xin Yin Xin Yin t [pathseg]
    exch dup 9 1 roll exch % t I.x I.y Xin Yin Xin Yin t [pathseg]
    dup length 2 eq { % a line
      exch pop
      aload pop aload pop 3 -1 roll aload pop VecSub % t I.x I.y Xin Yin Xin Yin dXp dYp
    } {
      exch dup cvi sub DeriveCurve
    } ifelse
    % the following part is copied from /PlainInterface
    NormalVec
    mode trans eq {
      n1 n2 RefractVec
      2 copy 0 eq exch 0 eq and { tir } { ok } ifelse
    } {
      ReflectVec ok
    } ifelse
    /n1 n2 def
    5 -2 roll 2 copy 7 2 roll X0 Y0 @ABVect Xin Yin DotProd 0 lt
    PN 1 gt and {
      pop missed
    } if
    % t X0' Y0' Xout Yout status
  } ifelse
  DebugEnd
} bind def
/TransformRefIndex {
  dup bgRefIndex eq { pop 1 } if
} bind def
/GetRefIndex {
  cvn load /n get /nbeam load exch
  EvalRefIndex
} bind def
/EvalRefIndex {
  dup bgRefIndex eq not {
    1 dict begin
      /n ED
      exec
    end
  } if
} bind def
/Sellmaier {
  dup mul
  dup dup 1.03961212 mul exch 6000.69867 sub div
  exch dup dup 0.231792344 mul exch 20017.9144 sub div
  exch dup 1.01046945 mul exch 103.560653e6 sub div
  add add 1 add sqrt
} bind def
/TangentCrosspoint {
    4 copy 4 copy 14 -2 roll 2 copy
    6 2 roll @ABVect neg exch
    6 2 roll @ABVect neg exch
    8 -2 roll VecAdd 10 2 roll VecAdd
    @InterLines pop
} bind def
/NearestNodeTmp {
  exch /NodeB ED
  /dist -1 def
  dup cvn load /N get dup 1 eq {
    [ exch (N) ]
  } {
    [ exch 1 1 3 -1 roll { } for ]
  } ifelse
  {
    2 copy pop
    GetIfcCenterCorr 2 copy
    NodeB @ABDist
    dist 0 lt {
      /dist ED
      ToVec /node ED
    } {
      dup dist lt {
        /dist ED
        ToVec /node ED
      } {
        pop pop pop
      } ifelse
    } ifelse
  } forall
  pop dist /node load
} bind def
/NearestNode {
  (NearestNode) DebugBegin
  dup xcheck not { nametostr } if /CompB ED
  dup xcheck not {
    nametostr /CompA ED
    /CompB load dup xcheck not {
      /mindist -1 def
      [ exch false GetInternalNodeNames ]
      { @GetCenter ToVec
        CompA NearestNodeTmp
        exch dup mindist ge mindist 0 ge and {
          pop pop
        }{
          /mindist ED /minnodeA ED
        } ifelse
      } forall
      minnodeA
    } {
      CompA NearestNodeTmp exch pop exec
    } ifelse
  } {
    exec
  } ifelse
  DebugEnd
} bind def
/RelConnAngle {
  (RelConnAngle) DebugBegin
  /fiberalign ED
  dup xcheck not { nametostr } if /CompB ED
  dup xcheck not { nametostr } if /CompA ED
  /CompA load xcheck {
    /CompB load xcheck {
      @ABVect exch atan
    } {
      4 copy @ABVect 6 2 roll pop pop 2 copy
      CompB (Center) NodeName @GetCenter
      4 2 roll @ABVect 4 2 roll
      CompB
      fiberalign center eq {
        RelConnAngle@center
      }{
        3 1 roll pop pop
        RelConnAngle@ref
      } ifelse
      2 copy exch atan
      7 3 roll 2 copy 9 -2 roll
      DotProd 0 gt 5 1 roll DotProd 0 gt xor { 180 add } if
    } ifelse
  } {
    4 2 roll pop pop 2 copy
    CompA (Center) NodeName @GetCenter
    4 2 roll @ABVect 4 2 roll
    CompA fiberalign center eq {
      RelConnAngle@center
    }{
      3 1 roll pop pop
      RelConnAngle@tref
    } ifelse
    2 copy exch atan
    5 1 roll DotProd 0 gt { 180 add } if
  } ifelse
  DebugEnd
} bind def
/RelConnAngle@ref {
  dup (A) NodeName exch (B) NodeName
  @GetCenter 3 -1 roll @GetCenter @ABVect
} bind def
/RelConnAngle@tref {
  dup (TrefA) NodeName exch (TrefB) NodeName
  @GetCenter 3 -1 roll @GetCenter @ABVect
} bind def
/RelConnAngle@center {
  (Center) NodeName @GetCenter 4 2 roll @ABVect
} bind def
/GetIfcOrNodeCoord {
  (GetIfcOrNodeCoord) DebugBegin
  dup xcheck {
    exch pop exec
  } {
    nametostr exch nametostr exch GetIfcCenter
  } ifelse
  DebugEnd
} bind def
/connectInterfaces {
  /relAngleTmp ED
  PN 2 eq {
    pop @ABVect NormalizeVec 4 2 roll VecAngle /relAngleTmp ED
  } if
  PN 3 ge {
    trans eq {
      @ABVect NormalizeVec 4 2 roll pop pop % remove Vec from stack
      relAngleTmp matrix rotate dtransform
      4 2 roll pop pop
    } {
      @ABVect NormalizeVec 4 2 roll VecAngle /relAngleTmp ED
    } ifelse
  } if
  relAngleTmp
} bind def
/GetCompRange {
  2 copy gt { 1 }{ -1 } ifelse 3 -1 roll
  { exch dup 3 -1 roll inttostr strcat exch} for
  pop
} bind def
/CorrectDipoleIfc {
  (CorrectDipoleIfc) DebugBegin
  dup dup 3 copy
  8 -1 roll dup 9 1 roll NodeName exch 7 -1 roll dup 7 1 roll NodeName
  gsave
    tx@Dict begin
      STV CP T
      exch @GetCenter 3 -1 roll @GetCenter
    end
  grestore
  4 copy @ABDist 1e-7 lt {
    6 -1 roll
    gsave
      tx@Dict begin
        STV CP T
        (TrefA) NodeName @GetCenter 7 -1 roll
        (TrefB) NodeName @GetCenter
      end
    grestore
    @ABVect NormalizeVec 2 copy
    8 -2 roll abs exch abs mymax -1e-6 mul VecScale
    8 -2 roll cvn load begin
      IfcName load begin
        X Y VecAdd /YCorr exch def /XCorr exch def
      end
    end
    4 2 roll abs exch abs mymax 1e-6 mul VecScale
    4 2 roll cvn load begin
      IfcName load begin
        X Y VecAdd /YCorr exch def /XCorr exch def
      end
    end
  } {
    10 { pop } repeat
  } ifelse
  DebugEnd
} bind def
/ClipFadeValue {
  dup 0 lt { pop 0 }{ dup 1 gt { pop 1 } if } ifelse
} bind def
/fadeto@white {
  FadeFunc ClipFadeValue @S mul @H exch @B sethsbcolor
} bind def
/fadeto@black {
  FadeFunc ClipFadeValue @B mul @H exch @S exch sethsbcolor
} bind def
/fadeto@transparency {
  FadeFunc ClipFadeValue @T mul .setopacityalpha
} bind def
/fadefunc@linear {
  neg 1 add
} bind def
/fadefunc@squared {
  dup mul neg 1 add
} bind def
/fadefunc@gauss {
  0.4 div dup mul neg Euler exch exp
} bind def
/fadefunc@exp {
  -6 mul Euler exch exp
} bind def
/FadeStroke {
  /FadeFunc ED /FadeToColor ED /@T ED
  PathLength dup /@L ED exch div /@dl ED
  mark
  { false counttomark 3 roll }
  { true counttomark 3 roll }
  {} {} pathforall
  currenthsbcolor /@B ED /@S ED /@H ED
  newpath /currL 0 def
  counttomark 3 idiv 1 1 3 -1 roll {
    pop
    { % lineto
      /y2 ED /x2 ED  x2 x1 sub y2 y1 sub 2 copy
      dup mul exch dup mul add sqrt dup  @L div exch
      @dl div 1 add floor dup dup
      4 2 roll div 5 1 roll
      1 1 3 -1 roll {
        5 copy 4 copy 2 copy eq not { fadecorrect add } if exch div VecScale
        6 2 roll 1 sub dup 0 eq not { fadecorrect sub } if exch div VecScale
        x1 y1 VecAdd moveto x1 y1 VecAdd lineto
        mul currL add FadeToColor
        stroke
      } for
      4 1 roll pop pop mul currL add /currL ED
      /y1 y2 def /x1 x2 def
    } { % moveto
      /y1 ED /x1 ED
    } ifelse
  } for
  pop
} def
/TransformPath {
  mark [ 3 -1 roll aload pop
  counttomark 1 add counttomark 1 add exch 1 roll
  {
    counttomark 1 eq { cleartomark exit } if
    dup /curvetype eq {
      7 1 roll
      3 { CompMtrx transform CM itransform 7 2 roll } repeat
      counttomark -1 roll dup counttomark 1 roll
      7 roll
    } {
      3 1 roll CompMtrx transform CM itransform 3 -1 roll
      counttomark -1 roll dup counttomark 1 roll
      3 roll
    } ifelse
  } loop
  ]
} bind def
/DeriveCurve {
  (DeriveCurve) DebugBegin
  exch dup length 4 eq not {
    pop pop 0 0
  } {
    aload pop 5 -1 roll
    dup 1 exch sub dup mul -3 mul exch % P0 P1 P2 P3 C0=(-3(1-t)^2) t
    dup dup -4 mul 1 add exch dup mul 3 mul add 3 mul exch % P0 P1 P2 P3 C0 C1=(3(3t^2-4t+1)) t
    dup dup 2 mul exch dup mul -3 mul add 3 mul exch % P0 P1 P2 P3 C0 C1 C2=(3(2t-3t^2)) t
    dup mul 3 mul % P0 P1 P2 P3 C0 C1 C2 C3=3t^2
    8 copy
    0 6 -1 3 { -1 roll 0 get 3 -1 roll mul add } for
    9 1 roll
    0 6 -1 3 { -1 roll 1 get 3 -1 roll mul add } for
  } ifelse
  DebugEnd
} bind def
/GetBezierDeriv {  % t on stack
  10 dict begin % hold all local
  /t ED
  /t1 1 t sub def % t1=1-t
  dup length /BezierOrder exch def
  /Points exch def
  /Coeff tx@FuncDict begin Pascal end BezierOrder get def % get the coefficients
    0 0 % initial values for x y
    BezierOrder -1 0 { % BezierOrder,...,2,1,0
      /I ED % I=BezierOrder,...,2,1,0
      /J BezierOrder I sub def % J=0,1,2,...,BezierOrder
      I 0 eq {
        0
      }{
        I t I 1 sub exp mul t1 J exp mul        %  i*t^{i-1}*(1-t)^{n-i}
      } ifelse
      J 0 eq {
        0
      } {
        J t I exp mul t1 J 1 sub exp mul    % -(n-i)t^i(1-t)^{n-i-1}
      } ifelse
      sub Coeff J get mul
      Points I get aload pop 3 -1 roll VecScale VecAdd
    } for % x y on stack
  end
} bind def
tx@IntersectDict begin
/IntersectLinePath {
  3 dict begin
    PreparePath dup length /n exch def
    2 copy ElongateLine exch 3 -1 roll pop
    /isect [] def
    /t -1 def
    {
      /n n 1 sub def
      2 copy IntersectBeziers
      dup 5 1 roll LoadIntersectionPoints
      dup length 0 gt {
        /isect exch def
        0 get dup type /arraytype eq {
          aload pop add 0.5 mul
        } if n add /t exch def
        exch pop
        exit
      } {
        pop pop pop
      } ifelse
    } forall
    t isect
  end
} bind def
end
/GetCoordinatePair {%
  2 mul -2 roll counttomark 1 add 2 roll cleartomark
} bind def
/GetFirstInputCoordinatePair { 1 GetCoordinatePair } bind def
/GetLastInputCoordinatePair { counttomark 2 idiv 1 sub GetCoordinatePair } bind def
/mymax {
  2 copy lt { exch } if pop
} bind def
/debug {
  /@N ED count dup @N gt @N 0 ge and { pop @N } if
  copy @N { == } repeat
} bind def
/debugComp {
  dup (debug comp ") exch strcat ("===============) strcat ==
  cvn load {
    dup type /dicttype eq {
      (plane----------------) ==
      { == == } forall
      (-----------done) ==
      } { == } ifelse
      ==
  } forall
  (================== done) ==
} bind def
end % tx@OptexpDict
