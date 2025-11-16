%!
% PostScript prologue for pst-eucl.tex.
% Version 1.04 2020/09/29
% For distribution, see pstricks.tex.
%
/tx@EcldDict 40 dict def tx@EcldDict begin
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Prcision
/epsilon 1E-5 def
/epsilonMin 1E-6 def
/epsilonMax 1E-3 def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Pi
/Pi 3.14159265359 def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% e
/E 2.718281828459045 def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x -> true (if |x| < epsilonMin)
/ZeroEq { abs epsilonMin lt } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x1 y1 x2 y2 -> a b c (ax-by+c=0 with a^2+b^2=1)
/EqDr {
  4 copy 3 -1 roll sub 7 1 roll exch sub 5 1 roll 4 -1 roll
  mul 3 1 roll mul exch sub
  2 index dup mul 2 index dup mul add sqrt
  4 -1 roll 1 index div exch
  4 -1 roll 1 index div exch
  4 -1 roll 1 index div exch pop
} bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% orthogonal projection of M1 onto (OM2)
%% x1 y1 x2 y2 -> x3 y3
/Project {
  2 copy dup mul exch dup mul add 5 1 roll 2 copy 5 -1 roll mul exch
  5 -1 roll mul add 4 -1 roll div dup 4 -1 roll mul exch 3 -1 roll mul
} bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% a b c (ax2+bx+c=0) -> x1 y1
/SolvTrin {
  /c exch def /b exch def /a exch def
  b dup mul a c mul 4 mul sub dup 0 lt
  { pop 0 0 } %% no solutions
  {sqrt dup b neg add a 2 mul div exch b add neg 2 a mul div }
  ifelse } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x1 y1 x2 y2 -> Dist
/ABDist { 3 -1 roll sub dup mul 3 1 roll sub dup mul add sqrt } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x1 y1 x2 y2 -> x2-x1  y2-y1
/ABVect { 3 -1 roll exch sub 3 1 roll sub exch } bind def
%/ABVect { 3 -1 roll sub 3 1 roll exch sub exch } bind def  %% wrong version
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x1 y1 x2 y2 x3 y3 x4 y4 -> x y
/InterLines {
  EqDr /D1c exch def /D1b exch def /D1a exch def
  EqDr /D2c exch def /D2b exch def /D2a exch def
  D1a D2b mul D1b D2a mul sub dup ZeroEq
%   { pop pop pop 0 0 } %% parallel lines  % --- hv 20110714
   { pop 0 0 } %% parallel lines             --- hv 20110714
   {
    /Det exch def
    D1b D2c mul D1c D2b mul sub Det div
    D1a D2c mul D2a D1c mul sub Det div
   } ifelse  } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% a b c R -> x1 y1 x2 y2
/InterLineCircle {
  /CR exch def /Dc exch def neg /Db exch def /Da exch def
  ABVect /Vy exch def /Vx exch def
  %% Dc==0 then O belong to the line
  %% First project O on the line -> M (-ca;-cb)
  %% l'abscisse de M sur (OM) divisee par R donne le cosinus
  %Dc neg dup Db mul exch Da mul 2 copy 0 0
  %ABDist dup CR gt { pop pop pop 0 0 0 0 }
  %{ ZeroEq { pop pop Db Da } if Atan /alpha exch def
  Dc abs CR gt { 0 0 0 0 }
  { Db neg Da neg Atan /alpha exch def
  Dc CR div dup dup mul 1 exch sub sqrt exch Atan /beta exch def
  alpha beta add dup cos CR mul exch sin CR mul
  alpha beta sub dup cos CR mul exch sin CR mul
  4 copy ABVect Vy mul 0 le exch Vx mul 0 le and
  { 4 2 roll } if } ifelse
 } def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% R R' OO' -> x1 y1 x2 y2
/InterCircles {
  /OOP exch def /CRP exch def /CR exch def
  OOP dup mul CRP dup mul sub CR dup mul add OOP div 2 div
  dup dup mul CR dup mul exch sub dup
  0 lt { pop pop 0 0 0 0 } { sqrt 2 copy neg } ifelse
} bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x y theta -> x' y' (rotation of theta)
/Rotate {
  dup sin /sintheta exch def cos /costheta exch def /y exch def /x exch def
  x costheta mul y sintheta mul sub
  y costheta mul x sintheta mul add
} def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% N -> x y
/GetNode {
  tx@NodeDict begin
    tx@NodeDict 1 index known { load GetCenter } { pop 0 0 } ifelse
  end
} bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x -> ch(x)
/ch { dup Ex exch neg Ex add 2 div } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x -> sh(x)
/sh { dup Ex exch neg Ex sub 2 div } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x -> e^(x)
/Ex { E exch exp } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% x f g -> x y n
/NewtonSolving {
  /g exch def /f exch def 0
  { %%% STACK: x0 n
    1 add exch %% one more loop
    dup ZeroEq
    { dup 0.0005 add fgeval
      1 index 0.0005 sub fgeval sub .001 div }
    { dup 1.0005 mul fgeval
      1 index 0.9995 mul fgeval sub .001 2 index mul div } ifelse  %%% STACK: n x0 fg'(x0)
    %%% compute x1=x0-fg(x0)/fg'(x0)
    1 index fgeval exch div dup 4 1 roll sub exch %% stack: dx x0 n
    3 -1 roll ZeroEq              %% exit if root found
    1 index 100 eq or { exit } if %% or looping for more than 100 times
  } loop
  dup 100 lt { exch dup /x exch def f } { pop 0 0 } ifelse
  3 -1 roll
} def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
/fgeval { /x exch def f g sub } bind def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% calculate the line coefficents Ax+By+C=0
%% x1 y1 x2 y2 -> A B C
/LineCoefABC {
  0 index 3 index sub % A=y2-y1
  4 index 3 index sub % B=x1-x2
  3 index 5 index mul 6 index 4 index mul sub % C=x2y1-x1y2
  7 3 roll pop pop pop pop
} def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% calculate the 2-order determinant
%% |a11 a12|
%% |a21 a22|
%% a11 a12, a21 a22 -> X
/DeterminantTwo {
  4 1 roll mul 3 1 roll mul exch sub
} def
%% calculate the 3-order determinant
%% |a11 a12 a13|
%% |a21 a22 a23|
%% |a31 a32 a33|
%%   8   7   6    5   4   3    2   1   0
%% a11 a12 a13, a21 a22 a23, a31 a32 a33 -> X
/DeterminantThree {
  % |a22 a23, a32 a33| * (-1)^(1+1)a11
  8 index abs epsilon lt { %a11=0
    0
  } {
    4 index 4 index 3 index 3 index DeterminantTwo
    9 index mul
  } ifelse
  % |a12 a13, a32 a33| * (-1)^(1+2)a21
  6 index abs epsilon lt { %a12=0
    0 sub
  } {
    8 index 8 index 4 index 4 index DeterminantTwo
    7 index mul sub
  } ifelse
  % |a12 a13, a22 a23| * (-1)^(1+3)a31
  3 index abs epsilon lt { %a13=0
    0 add
  } {
    8 index 8 index 7 index 7 index DeterminantTwo
    4 index mul add
  } ifelse
  10 1 roll pop pop pop pop pop pop pop pop pop
} def
%% calculate the 4-order determinant
%% |a11 a12 a13 a14|
%% |a21 a22 a23 a24|
%% |a31 a32 a33 a34|
%% |a41 a42 a43 a44|
%%  15  14  13  12   11  10   9   8    7   6   5   4    3   2   1   0
%% a11 a12 a13 a14, a21 a22 a23 a24, a31 a32 a33 a34, a41 a42 a43 a44 -> X
/DeterminantFour {
  % |a22 a23 a24, a32 a33 a34, a42 a43 a44| * (-1)^(1+1)a11
  15 index abs epsilon lt { %a11=0
    0
  } {
    10 index 10 index 10 index 9 index 9 index 9 index 8 index 8 index 8 index DeterminantThree
    16 index mul
  } ifelse
  % |a12 a13 a14, a32 a33 a34, a42 a43 a44| * (-1)^(1+2)a21
  12 index abs epsilon lt { %a21=0
    0 sub
  } {
    15 index 15 index 15 index 10 index 10 index 10 index 9 index 9 index 9 index DeterminantThree
    13 index mul sub
  } ifelse
  % |a12 a13 a14, a22 a23 a24, a42 a43 a44| * (-1)^(1+3)a31
  8 index abs epsilon lt { %a31=0
    0 add
  } {
    15 index 15 index 15 index 14 index 14 index 14 index 9 index 9 index 9 index DeterminantThree
    9 index mul add
  } ifelse
  % |a12 a13 a14, a22 a23 a24, a32 a33 a34| * (-1)^(1+4)a41
  4 index abs epsilon lt { %a41=0
    0 sub
  } {
    15 index 15 index 15 index 14 index 14 index 14 index 13 index 13 index 13 index DeterminantThree
    5 index mul sub
  } ifelse
  17 1 roll pop pop pop pop pop pop pop pop
  pop pop pop pop pop pop pop pop
} def
%% calculate the 5-order determinant
%% |a11 a12 a13 a14 a15|
%% |a21 a22 a23 a24 a25|
%% |a31 a32 a33 a34 a35|
%% |a41 a42 a43 a44 a45|
%% |a51 a52 a53 a54 a55|
%%  24  23  22  21  20   19  18  17  16  15   14  13  12  11  10    9   8   7   6   5    4   3   2   1   0
%% a11 a12 a13 a14 a15, a21 a22 a23 a24 a25, a31 a32 a33 a34 a35, a41 a42 a43 a44 a45, a51 a52 a53 a54 a55-> X
/DeterminantFive {
  % |a22 a23 a24 a25, a32 a33 a34 a35, a42 a43 a44 a45, a52 a53 a54 a55| * (-1)^(1+1)a11
  24 index abs epsilon lt { %a11=0
    0
  } {
    18 index 18 index 18 index 18 index 17 index 17 index 17 index 17 index 16 index 16 index 16 index 16 index 15 index 15 index 15 index 15 index DeterminantFour
    25 index mul
  } ifelse
  % |a12 a13 a14 a15, a32 a33 a34 a35, a42 a43 a44 a45, a52 a53 a54 a55| * (-1)^(1+2)a21
  20 index abs epsilon lt { %a21=0
    0 sub
  } {
    24 index 24 index 24 index 24 index 18 index 18 index 18 index 18 index 17 index 17 index 17 index 17 index 16 index 16 index 16 index 16 index DeterminantFour
    21 index mul sub
  } ifelse
  % |a12 a13 a14 a15, a22 a23 a24 a25, a42 a43 a44 a45, a52 a53 a54 a55| * (-1)^(1+3)a31
  15 index abs epsilon lt { %a31=0
    0 add
  } {
    24 index 24 index 24 index 24 index 23 index 23 index 23 index 23 index 17 index 17 index 17 index 17 index 16 index 16 index 16 index 16 index DeterminantFour
    16 index mul add
  } ifelse
  % |a12 a13 a14 a15, a22 a23 a24 a25, a32 a33 a34 a35, a52 a53 a54 a55| * (-1)^(1+4)a41
  10 index abs epsilon lt { %a41=0
    0 sub
  } {
    24 index 24 index 24 index 24 index 23 index 23 index 23 index 23 index 22 index 22 index 22 index 22 index 16 index 16 index 16 index 16 index DeterminantFour
    11 index mul sub
  } ifelse
  % |a12 a13 a14 a15, a22 a23 a24 a25, a32 a33 a34 a35, a42 a43 a44 a45| * (-1)^(1+5)a51
  5 index abs epsilon lt { %a51=0
    0 add
  } {
    24 index 24 index 24 index 24 index 23 index 23 index 23 index 23 index 22 index 22 index 22 index 22 index 21 index 21 index 21 index 21 index DeterminantFour
    6 index mul add
  } ifelse
  26 1 roll pop pop pop pop pop pop pop pop pop pop
  pop pop pop pop pop pop pop pop pop pop
  pop pop pop pop pop
} def

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Conic Intersections
% The following macros implements the conic intersectionpoints in Asymptote
% module geometry.asy provided by Philippe IVALDI.
% http://www.piprime.fr/files/asymptote/geometry/modules/geometry.asy.html
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% num len [array] numIsInArray -> bool 
/numIsInArray {
  /arr ED /len ED /num ED
  /res false def
  0 1 len 1 sub {
    /idx ED
    /val arr idx get def
    num val sub abs epsilonMax lt {
      /res true def
      exit 
    } if
  } for
  res
} def

% find the real roots of quadratic equation ax^2+bx+c=0
% a b c -> [roots] nroots
/QuadraticRealRoots {
15 dict begin % all variables are local
  /Coefc ED /Coefb ED /Coefa ED
  /nroots 0 def /roots 2 array def
  %[ Coefa Coefb Coefc ] ==
  Coefa abs epsilonMin lt {
    Coefb abs epsilonMin gt {
      roots 0 Coefc Coefb div neg put
      /nroots 1 def
    }
  }{
    /delta Coefb Coefb mul 4 Coefc Coefa mul mul sub def
    delta abs epsilon lt {
      roots 0 Coefb 2 Coefa mul div neg put
      /nroots 1 def
    }{
      delta 0.0 gt {
        /delta delta sqrt def
        roots 0 Coefb neg delta add 2 Coefa mul div put
        roots 1 Coefb neg delta sub 2 Coefa mul div put
        /nroots 2 def
      } if
    } ifelse
  } ifelse
  roots nroots % push the roots on stack.
end} def

% find the real roots of cubic equation a*x^3+b*x^2+c*x+d=0
% a b c d CubicRealRoots -> [roots] nroots
/CubicRealRoots {
15 dict begin % all variables are local
  /Coefd ED /Coefc ED /Coefb ED /Coefa ED
  % [ Coefa Coefb Coefc Coefd ] ==
  /nroots 0 def /roots 3 array def
  Coefa abs epsilonMin lt { % quadratic case
    Coefb Coefc Coefd QuadraticRealRoots
    /nroots ED roots copy pop
  }{% true cubic
    % normalize to x^3+bx^2+cx+d=0
    /Coefb Coefb Coefa div def
    /Coefc Coefc Coefa div def
    /Coefd Coefd Coefa div def
    % let x=y-b/3, we have
    % y^3+py+q=0
    % where p=(3c-b^2)/3,q=(27d-9bc+2b^3)/27
    % let y=u+v, where uv=-p/3, then
    % u^3+v^3=-q, u^3v^3=-p^3/27
    % then u^3=-q/2-\sqrt(q^2/4+p^3/27)
    %      u^3=-q/2+\sqrt(q^2/4+p^3/27)
    % http://eqworld.ipmnet.ru/en/solutions/ae/ae0103.pdf
    Coefb abs epsilonMin lt {
      /bthird 0 def
      /p Coefc def
      /q Coefd def
    }{
      /bthird Coefb 3 div def 
      /p 3 Coefc mul Coefb Coefb mul sub 3 div def
      /q 27 Coefd mul 9 Coefb mul Coefc mul sub 2 Coefb mul Coefb mul Coefb mul add 27 div def
    } ifelse
    /ppp p dup dup mul mul def
    /qq q dup mul def
    /delta qq 4 div ppp 27 div add def
    % p = q = delta =
    delta abs epsilon lt {
      q abs epsilon lt {
        /nroots 1 def
        roots 0 bthird neg put
      }{
        /nroots 2 def
        q 0.0 gt {
          /r1 q 2 div 1 3 div exp def
        }{
          /r1 q 2 div neg 1 3 div exp neg def
        } ifelse
        /r2 r1 -2 mul def
        roots 0 r1 bthird sub put
        roots 1 r2 bthird sub put
      } ifelse
    }{
      delta 0.0 gt {
        /nroots 1 def
        /qhalfneg q 2 div neg def
        /deltasqrt delta sqrt def
        /pthirdneg p 3 div neg def
        p abs epsilon lt {
          /tu qhalfneg deltasqrt add def
          /tv qhalfneg deltasqrt sub def
          tu abs epsilon lt {
            /u 0.0 def
          }{
            tu 0.0 gt {
              /u tu 1 3 div exp def
            }{
              /u tu neg 1 3 div exp neg def
            } ifelse
          } ifelse
          tv abs epsilon lt {
            /v 0.0 def
          }{
            tv 0.0 gt {
              /v tv 1 3 div exp def
            }{
              /v tv neg 1 3 div exp neg def
            } ifelse
          } ifelse
        }{
          /tu qhalfneg deltasqrt add def
          tu 0.0 gt {
            /u tu 1 3 div exp def
          }{
            /u tu neg 1 3 div exp neg def
          } ifelse
          /v pthirdneg u div def
        } ifelse
        /r1 u v add def
        roots 0 r1 bthird sub put
      }{
        /nroots 3 def
        /qhalfneg q 2 div neg def
        /pthirdnegsqrt p 3 div neg sqrt def
        /argalpha qhalfneg pthirdnegsqrt dup dup mul mul div Acos 3 div def
        /r1 pthirdnegsqrt 2 mul argalpha cos mul def
        /r2 pthirdnegsqrt -2 mul argalpha 60 add cos mul def
        /r3 pthirdnegsqrt -2 mul argalpha 60 sub cos mul def
        roots 0 r1 bthird sub put
        roots 1 r2 bthird sub put
        roots 2 r3 bthird sub put
      } ifelse
    } ifelse
  } ifelse
  roots nroots % push the roots on stack.
end} def

% find the real roots of quartic equation a*x^4+b*x^3+c*x^2+dx+e=0
% a b c d e QuarticRealRoots -> [roots] nroots
/QuarticRealRoots {
15 dict begin % all variables are local
  /Coefe ED /Coefd ED /Coefc ED /Coefb ED /Coefa ED
  /nroots 0 def /roots 4 array def
  Coefa abs epsilonMin lt { % cubic case
    Coefb Coefc Coefd Coefe CubicRealRoots
    /nroots ED roots copy pop
  }{
    Coefe abs epsilonMin lt { % cubic case
      Coefa Coefb Coefc Coefd CubicRealRoots
      /nroots ED roots copy pop
      roots nroots 0.0 put
      /nroots nroots 1 add def
    }{ % true quartic
      % normalize to x^4+bx^3+cx^2+dx+e=0
      /Coefb Coefb Coefa div def
      /Coefc Coefc Coefa div def
      /Coefd Coefd Coefa div def
      /Coefe Coefe Coefa div def
      /qeval { 
        /vx ED
        1 vx mul Coefb add vx mul Coefc add vx mul Coefd add vx mul Coefe add % x(x(x(ax+b)+c)+d)+e
      } def
      % [1 Coefb Coefc Coefd Coefe ] ==
      % x^4+bx^3+cx^2+dx+e=0
      % (x^2+b/2x)^2=(b^2/4-c)x^2-dx-e
      % add (x^2+b/2x)y+y^2/4 in each side,
      % (x^2+b/2x+y/2)^2=(b^2/4+y-c)x^2+(by/2-d)x+(y^2/4-e)
      % choose y such that
      % (by/2-d)^2-4(b^2/4+y-c)(y^2/4-e)=0
      % i.e,
      % y^3-cy^2+(bd-4e)y-eb^2+4ec-d^2=0
      % let t=sqrt(b^2/4+y-c), then
      % (x^2+b/2x+y/2)^2=(tx+(by/2-d)/(2t))^2
      % we have
      % x^2+(b/2+t)x+y/2+(by/2-d)/(2t)=0
      % x^2+(b/2-t)x+y/2-(by/2-d)/(2t)=0
      1 Coefc neg Coefb Coefd mul 4 Coefe mul sub 4 Coefc Coefe mul mul Coefb Coefb Coefe mul mul sub Coefd Coefd mul sub
      CubicRealRoots /CubicNumRoots ED /CubicRoots ED
      %CubicNumRoots = CubicRoots ==
      0 1 CubicNumRoots 1 sub {
        /idx ED
        /y0 CubicRoots idx get def
        /delta y0 Coefc sub Coefb Coefb mul 4 div add def
        % [ idx y0 delta ] ==
        delta abs epsilonMax lt {
          /squareval y0 y0 mul 4 div Coefe sub def
          squareval abs epsilon lt {
            % x^2+b/2x+y/2=0
            %[squareval (squareval=0) ] ==
            1 Coefb 2 div y0 2 div QuadraticRealRoots
            /nroots1 ED /roots1 ED %nroots1 = roots1 == 
            0 1 nroots1 1 sub {
              /idx ED
              /rv roots1 idx get def
              rv qeval abs epsilonMax lt {
                rv nroots roots numIsInArray not {
                  roots nroots rv put
                  /nroots nroots 1 add def
                } if
              } if
            } for
          }{
            squareval 0.0 gt {
              %[squareval (squareval>0) ] ==
              % x^2+b/2x+y/2\pm\sqrt(y^2/4-e)=0
              /squareval squareval sqrt def
              1 Coefb 2 div y0 2 div squareval add QuadraticRealRoots
              /nroots1 ED /roots1 ED %nroots1 = roots1 == 
              1 Coefb 2 div y0 2 div squareval sub QuadraticRealRoots
              /nroots2 ED /roots2 ED %nroots2 = roots2 ==
              nroots1 0 gt nroots2 0 gt or {
                0 1 nroots1 1 sub {
                  /idx ED
                  /rv roots1 idx get def
                  rv qeval abs epsilonMax lt {
                    rv nroots roots numIsInArray not {
                      roots nroots rv put
                      /nroots nroots 1 add def
                    } if
                  } if
                } for
                0 1 nroots2 1 sub {
                  /idx ED
                  /rv roots2 idx get def
                  rv qeval abs epsilonMax lt {
                    rv nroots roots numIsInArray not {
                      roots nroots rv put
                      /nroots nroots 1 add def
                    } if
                  } if
                } for
              } if
            } if
          } ifelse
        }{
          delta 0.0 gt {
            %[delta (delta>0) ] ==
            /sqrtdelta delta sqrt def
            /Coefp Coefb 2 div sqrtdelta add def
            /Coefq y0 2 div y0 Coefb mul 2 div Coefd sub sqrtdelta div 2 div add def
            1 Coefp Coefq QuadraticRealRoots /nroots1 ED /roots1 ED %nroots1 = roots1 == 
            /Coefp Coefb 2 div sqrtdelta sub def
            /Coefq y0 2 div y0 Coefb mul 2 div Coefd sub sqrtdelta div 2 div sub def
            1 Coefp Coefq QuadraticRealRoots /nroots2 ED /roots2 ED %nroots2 = roots2 ==
            nroots1 0 gt nroots2 0 gt or {
              0 1 nroots1 1 sub {
                /idx ED
                /rv roots1 idx get def
                rv qeval abs epsilonMax lt {
                  rv nroots roots numIsInArray not {
                    roots nroots rv put
                    /nroots nroots 1 add def
                  } if
                } if
              } for
              0 1 nroots2 1 sub {
                /idx ED
                /rv roots2 idx get def
                rv qeval abs epsilonMax lt {
                  rv nroots roots numIsInArray not {
                    roots nroots rv put
                    /nroots nroots 1 add def
                  } if
                } if
              } for
            } if
          } if
        } ifelse
        nroots 4 eq {
          exit
        } if
      } for
    } ifelse
  } ifelse
  roots nroots % push the roots on stack.
end} def

% SortInters
% sort the intersections from smallest to largest abscissa.
% [Inters] nInters SortInters -> [Inters] nInters
/SortInters {
  /nInters ED /Inters ED
  nInters 1 gt {
    /PairCmp {
      /PairB ED /PairA ED
      PairA 0 get PairB 0 get sub
    } def
    /PairSwap {
      /PairB ED /PairA ED /IdxB ED /IdxA ED
      Inters IdxA PairB put
      Inters IdxB PairA put
    } def
    0 1 nInters 2 sub {
      /Idx ED
      0 1 nInters 2 sub Idx sub {
        /Bubidx ED
        /PairA Inters Bubidx get def
        /PairB Inters Bubidx 1 add get def
        PairA PairB PairCmp 0 gt {
          Bubidx Bubidx 1 add
          PairA PairB PairSwap
        } if
      } for
    } for
  } if
  Inters nInters % push the intersections on stack.
} def

% ConicCircleInter
% find all intersections of conic $cc(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% circle $c(x,y)=(x-x0)^2+(y-y0)^2=r^2$.
%
% a b c d e f  x0 y0 r ConicCircleInter -> [Inters] nInters
/ConicCircleInter {
15 dict begin % all variables are local
  /cr ED /cy0 ED /cx0 ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  %[ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /m 2 cca mul cx0 mul ccb cy0 mul add ccd add def
  /n 2 ccc mul cy0 mul ccb cx0 mul add cce add def
  /s cx0 cy0 cceval def
  /p s cr div ccc cr mul add def
  /t cca cr mul ccc cr mul sub def
  % [ m n s p t ] ==
  /Qqa ccb ccb mul cr mul cr mul t t mul add def
  /Qqb 2 t mul m mul 2 n mul ccb mul cr mul add def
  /Qqc m m mul n n mul add 2 t mul p mul add ccb ccb mul cr mul cr mul sub def
  /Qqd 2 m mul p mul 2 n mul ccb mul cr mul sub def
  /Qqe p p mul n n mul sub def
  %[ Qqa Qqb Qqc Qqd Qqe ] ==
  Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nroots ED /roots ED
  %nroots = roots ==
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  0 1 nroots 1 sub {
    /idx ED
    /cosx roots idx get def
    /sinx 1.0 cosx cosx mul sub sqrt def
    /x cr cosx mul cx0 add def
    /y cr sinx mul cy0 add def
    /ccxy x y cceval def
    % [idx 0 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
    /y cr sinx mul neg cy0 add def
    /ccxy x y cceval def
    % [idx 1 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def

% ConicEllipseInter
% find all intersections of conic $cc(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% ellipse $e(x,y): (x-x0)^2/m^2+(y-y0)^2/n^2=1$.
%
% a b c d e f  x0 y0 m n ConicEllipseInter -> [Inters] nInters
/ConicEllipseInter {
15 dict begin % all variables are local
  /en ED /em ED /ey0 ED /ex0 ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  %[ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /p 2 cca mul em mul ex0 mul ccb em mul ey0 mul add ccd em mul add def
  /q 2 ccc mul en mul ey0 mul ccb en mul ex0 mul add cce en mul add def
  /r ex0 ey0 cceval def
  /s r ccc en mul en mul add def
  /t cca em mul em mul ccc en mul en mul sub def
  % [ p q r s t ] ==
  /Qqa t t mul ccb ccb mul em mul em mul en mul en mul add def
  /Qqb 2 t mul p mul 2 q mul ccb mul em mul en mul add def
  /Qqc p p mul q q mul add 2 t mul s mul add ccb ccb mul em mul em mul en mul en mul sub def
  /Qqd 2 p mul s mul 2 q mul ccb mul em mul en mul sub def
  /Qqe s s mul q q mul sub def
  %[ Qqa Qqb Qqc Qqd Qqe ] ==
  Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nroots ED /roots ED
  %nroots = roots ==
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  0 1 nroots 1 sub {
    /idx ED
    /cosx roots idx get def
    /sinx 1.0 cosx cosx mul sub sqrt def
    /x em cosx mul ex0 add def
    /y en sinx mul ey0 add def
    /ccxy x y cceval def
    % [idx 0 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
    /y en sinx mul neg ey0 add def
    /ccxy x y cceval def
    % [idx 1 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def

% ConicHyperbolaInter
% find all intersections of conic $cc(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% hyperbola $h(x,y): (x-x0)^2/m^2-(y-y0)^2/n^2=1$.
%
% a b c d e f  x0 y0 m n ConicHyperbolaInter -> [Inters] nInters
/ConicHyperbolaInter {
15 dict begin % all variables are local
  /hn ED /hm ED /hy0 ED /hx0 ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  %[ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /p 2 cca mul hm mul hx0 mul ccb hm mul hy0 mul add ccd hm mul add def
  /q 2 ccc mul hn mul hy0 mul ccb hn mul hx0 mul add cce hn mul add def
  /r hx0 hy0 cceval def
  /s r ccc hn mul hn mul sub def
  /t cca hm mul hm mul ccc hn mul hn mul add def
  % [ p q r s t ] ==
  /Qqe t t mul ccb ccb mul hm mul hm mul hn mul hn mul sub def
  /Qqd 2 t mul p mul 2 q mul ccb mul hm mul hn mul sub def
  /Qqc p p mul q q mul sub 2 t mul s mul add ccb ccb mul hm mul hm mul hn mul hn mul add def
  /Qqb 2 p mul s mul 2 q mul ccb mul hm mul hn mul add def
  /Qqa s s mul q q mul add def
  %[ Qqa Qqb Qqc Qqd Qqe ] ==
  Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nroots ED /roots ED
  % nroots = roots ==
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  0 1 nroots 1 sub {
    /idx ED
    /cosx roots idx get def
    /sinx 1.0 cosx cosx mul sub sqrt def
    /x hm cosx div hx0 add def
    /y hn sinx mul cosx div hy0 add def
    /ccxy x y cceval def
    % [idx 0 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
    /y hn sinx mul cosx div neg hy0 add def
    /ccxy x y cceval def
    % [idx 1 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def

% ConicIHyperbolaInter
% find all intersections of conic $cc(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% conjugate hyperbola $h(x,y): (y-y0)^2/m^2-(x-x0)^2/n^2=1$.
%
% a b c d e f  x0 y0 m n ConicIHyperbolaInter -> [Inters] nInters
/ConicIHyperbolaInter {
15 dict begin % all variables are local
  /hn ED /hm ED /hy0 ED /hx0 ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  % [ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /p 2 ccc mul hm mul hy0 mul ccb hm mul hx0 mul add cce hm mul add def
  /q 2 cca mul hn mul hx0 mul ccb hn mul hy0 mul add ccd hn mul add def
  /r hx0 hy0 cceval def
  /s r cca hn mul hn mul sub def
  /t cca hn mul hn mul ccc hm mul hm mul add def
  % [ p q r s t ] ==
  /Qqe t t mul ccb ccb mul hm mul hm mul hn mul hn mul sub def
  /Qqd 2 t mul p mul 2 q mul ccb mul hm mul hn mul sub def
  /Qqc p p mul q q mul sub 2 t mul s mul add ccb ccb mul hm mul hm mul hn mul hn mul add def
  /Qqb 2 p mul s mul 2 q mul ccb mul hm mul hn mul add def
  /Qqa s s mul q q mul add def
  %[ Qqa Qqb Qqc Qqd Qqe ] ==
  Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nroots ED /roots ED
  %nroots = roots ==
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  0 1 nroots 1 sub {
    /idx ED
    /cosx roots idx get def
    /sinx 1.0 cosx cosx mul sub sqrt def
    /x hn sinx mul cosx div hx0 add def
    /y hm cosx div hy0 add def
    /ccxy x y cceval def
    % [idx 0 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
    /x hn sinx mul cosx div neg hx0 add def
    /ccxy x y cceval def
    % [idx 1 cosx sinx x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def

% ConicParabolaInter
% find all intersections of conic $cc(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% parabola $p(x,y): (x-x0)^2=2p(y-y0)$.
%
% a b c d e f  x0 y0 p ConicParabolaInter -> [Inters] nInters
/ConicParabolaInter {
15 dict begin % all variables are local
  /pp ED /py0 ED /px0 ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  % [ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /Qqa ccc 4 pp pp mul mul div def
  /Qqb ccb 2 pp mul div def
  /Qqc cca ccb px0 mul 2 pp mul div add ccc py0 mul pp div add cce 2 pp mul div add def
  /Qqd 2 cca px0 mul mul ccb py0 mul add ccd add def
  /Qqe px0 py0 cceval def
  Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nroots ED /roots ED
  %nroots = roots ==
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  0 1 nroots 1 sub {
    /idx ED
    /argt roots idx get def
    /x argt px0 add def
    /y argt argt mul 2 pp mul div py0 add def
    /ccxy x y cceval def
    % [idx 0 argt x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def

% ConicIParabolaInter
% find all intersections of conic $cc(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% conjugate parabola $p(x,y): (y-y0)^2=2p(x-x0)$.
%
% a b c d e f  x0 y0 p ConicIParabolaInter -> [Inters] nInters
/ConicIParabolaInter {
15 dict begin % all variables are local
  /pp ED /py0 ED /px0 ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  % [ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /Qqa cca 4 pp pp mul mul div def
  /Qqb ccb 2 pp mul div def
  /Qqc ccc ccb py0 mul 2 pp mul div add cca px0 mul pp div add ccd 2 pp mul div add def
  /Qqd 2 ccc py0 mul mul ccb px0 mul add cce add def
  /Qqe px0 py0 cceval def
  Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nroots ED /roots ED
  % nroots = roots ==
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  0 1 nroots 1 sub {
    /idx ED
    /argt roots idx get def
    /y argt py0 add def
    /x argt argt mul 2 pp mul div px0 add def
    /ccxy x y cceval def
    % [idx 0 argt x y ccxy ] ==
    ccxy abs epsilonMax lt {
      x y SaveInter
    } if
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def

% ConicInter
% find all intersections of conic $cc1(x,y)=ax^2+bxy+cy^2+dx+ey+f=0$ and
% $cc2(x,y)=a'x^2+b'xy+c'y^2+d'x+e'y+f'=0$.
%
% a b c d e f  a' b' c' d' e' f' ConicInter -> [Inters] nInters
/ConicInter {
15 dict begin % all variables are local
  /cxf ED /cxe ED /cxd ED /cxc ED /cxb ED /cxa ED
  /ccf ED /cce ED /ccd ED /ccc ED /ccb ED /cca ED
  % [ cxa cxb cxc cxd cxe cxf ] ==
  % [ cca ccb ccc ccd cce ccf ] ==
  % x y cceval -> cc(x,y)
  /cceval {
    /ty ED /tx ED
    cca tx mul tx mul
    ccb tx mul ty mul add
    ccc ty mul ty mul add
    ccd tx mul add
    cce ty mul add
    ccf add
  } def
  /cxeval {
    /ty ED /tx ED
    cxa tx mul tx mul
    cxb tx mul ty mul add
    cxc ty mul ty mul add
    cxd tx mul add
    cxe ty mul add
    cxf add
  } def
  /nInters 0 def /Inters 4 array def
  /SaveInter {
    /tty ED /ttx ED
    nInters 4 lt {
      Inters nInters [ttx tty] put
      /nInters nInters 1 add def
    } if
  } def
  cca cxa sub abs epsilon gt
  ccb cxb sub abs epsilon gt
  ccc cxc sub abs epsilon gt or or {
    /Qqa -2 cca ccc cxa cxc mul mul mul mul
            cca ccc cxb cxb mul mul mul add
            cca ccb cxc cxb mul mul mul sub
            ccb ccb cxa cxc mul mul mul add
            ccc ccb cxa cxb mul mul mul sub
            cca cca cxc cxc mul mul mul add
            ccc ccc cxa cxa mul mul mul add def
    /Qqb    ccc ccb cxa cxe mul mul mul neg
            ccc cce cxa cxb mul mul mul sub
            ccb ccd cxc cxb mul mul mul sub
          2 cca ccc cxb cxe mul mul mul mul add
            cca ccb cxc cxe mul mul mul sub
            ccb ccb cxc cxd mul mul mul add
          2 ccc ccd cxa cxc mul mul mul mul sub
          2 cca ccc cxc cxd mul mul mul mul sub
            ccc ccd cxb cxb mul mul mul add
            ccc ccb cxb cxd mul mul mul sub
          2 ccb cce cxa cxc mul mul mul mul add
          2 ccc ccc cxa cxd mul mul mul mul add
            cca cce cxc cxb mul mul mul sub
          2 cca ccd cxc cxc mul mul mul mul add def
    /Qqc    ccd cce cxc cxb mul mul mul neg
            ccc ccf cxb cxb mul mul mul add
            ccb ccf cxc cxb mul mul mul sub
            ccb ccd cxc cxe mul mul mul sub
            ccb ccb cxc cxf mul mul mul add
          2 ccc ccd cxc cxd mul mul mul mul sub
          2 ccc ccc cxa cxf mul mul mul mul add
          2 cca ccf cxc cxc mul mul mul mul add
            ccd ccd cxc cxc mul mul mul add
          2 ccc ccf cxa cxc mul mul mul mul sub
          2 ccb cce cxc cxd mul mul mul mul add
            ccc cce cxb cxd mul mul mul sub
          2 cca ccc cxc cxf mul mul mul mul sub
            ccc ccc cxd cxd mul mul mul add
          2 ccc ccd cxb cxe mul mul mul mul add
            ccc cce cxa cxe mul mul mul sub
            cce cce cxa cxc mul mul mul add
            ccc ccb cxd cxe mul mul mul sub
            ccc ccb cxb cxf mul mul mul sub
            cca cce cxc cxe mul mul mul sub
            cca ccc cxe cxe mul mul mul add def
    /Qqd    cce ccf cxc cxb mul mul mul neg
            ccc ccd cxe cxe mul mul mul add
          2 ccd ccf cxc cxc mul mul mul mul add
            ccc ccb cxe cxf mul mul mul sub
            ccc cce cxd cxe mul mul mul sub
          2 ccc ccc cxd cxf mul mul mul mul add
          2 ccc ccd cxc cxf mul mul mul mul sub
            ccd cce cxc cxe mul mul mul sub
          2 ccc ccf cxc cxd mul mul mul mul sub
            ccc cce cxb cxf mul mul mul sub
          2 ccb cce cxc cxf mul mul mul mul add
            ccb ccf cxc cxe mul mul mul sub
            cce cce cxc cxd mul mul mul add
          2 ccc ccf cxb cxe mul mul mul mul add def
    /Qqe -2 ccc ccf cxc cxf mul mul mul mul
            cce cce cxc cxf mul mul mul add
            ccf ccf cxc cxc mul mul mul add
            cce ccf cxc cxe mul mul mul sub
            ccc ccf cxe cxe mul mul mul add
            ccc ccc cxf cxf mul mul mul add
            ccc cce cxe cxf mul mul mul sub def
    % [ Qqa Qqb Qqc Qqd Qqe ] ==
    Qqa Qqb Qqc Qqd Qqe QuarticRealRoots /nQRoots ED /QRoots ED
  } {
    cce cxe sub abs epsilon gt {
      /D cxe cce sub dup mul def
      /Qda cca cxe cxe mul mul
           ccb ccd mul ccb cxd mul sub 2 cca cce mul mul mul sub cxe mul add
           ccc cxd cxd mul mul add
           ccb cce mul 2 ccc ccd mul mul sub cxd mul add
           cca cce cce mul mul add
           ccb ccd cce mul mul sub
           ccc ccd ccd mul mul add D div def
      /Qdb ccb cxe mul 2 ccc cxd mul mul sub ccb cce mul sub 2 ccc ccd mul mul add cxf mul
           ccd cxe cxe mul mul sub
           cce cxd mul ccb ccf mul sub ccd cce mul add  cxe mul add
           2 ccc ccf mul mul cce cce mul sub cxd mul add
           ccb cce mul 2 ccc ccd mul mul sub ccf mul add
           D div neg def
      /Qdc ccc ccf cxf sub dup mul mul D div
           cce ccf cxf sub mul cxe cce sub div add ccf add def
      Qda Qdb Qdc QuadraticRealRoots /nQRoots ED /QRoots ED
    } {
      ccd cxd sub abs epsilon gt {
        /D cxd ccd sub def
        /Qda ccc def
        /Qdb ccb cxf mul neg cce cxd mul add ccb ccf mul add ccd cce mul sub D div def
        /Qdc cca ccf cxf sub dup mul mul D dup mul div ccd ccf cxf sub mul D div add ccf add def
        Qda Qdb Qdc QuadraticRealRoots /nDRoots ED /DRoots ED
        0 1 nDRoots 1 sub {
          /DIdx ED
          /DVal DRoots DIdx get def
          /Qea cca def
          /Qeb ccb DVal mul ccd add def
          /Qec ccc DVal dup mul mul cce DVal mul add ccf add def
          Qea Qeb Qec QuadraticRealRoots /nERoots ED /ERoots ED
          0 1 nERoots 1 sub {
            /EIdx ED
            /XVal ERoots EIdx get def
            /ccxy XVal DVal cceval def
            /cxxy XVal DVal cxeval def
            ccxy abs epsilonMax lt cxxy abs epsilonMax lt and {
              XVal DVal SaveInter
            } if
          } for
        } for
        Inters nInters SortInters% push the intersections on stack.
        exit
      } {
        ccf cxf sub abs epsilon lt {
          (cannot find intersection of identical conics) =
          exit
        } if
      } ifelse
    } ifelse
  } ifelse
  0 1 nQRoots 1 sub {
    /QIdx ED
    /QVal QRoots QIdx get def
    /Qea ccc def
    /Qeb ccb QVal mul cce add def
    /Qec cca QVal dup mul mul ccd QVal mul add ccf add def
    Qea Qeb Qec QuadraticRealRoots /nERoots ED /ERoots ED
    0 1 nERoots 1 sub {
      /EIdx ED
      /YVal ERoots EIdx get def
      /ccxy QVal YVal cceval def
      /cxxy QVal YVal cxeval def
      ccxy abs epsilonMax lt cxxy abs epsilonMax lt and {
        QVal YVal SaveInter
      } if
    } for
  } for
  Inters nInters SortInters% push the intersections on stack.
end} def
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end
% END ps-euclide.pro
