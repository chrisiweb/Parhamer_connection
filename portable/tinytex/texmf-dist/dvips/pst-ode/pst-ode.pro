%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% PostScript prologue for pst-ode.tex.
% Version 0.19, 2024/01/04
%
% Alexander Grahn (C) 2012--today
%
% This program can be redistributed and/or modified under the terms
% of the LaTeX Project Public License
%
% http://www.latex-project.org/lppl.txt
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
/tx@odeDict 1 dict def
tx@odeDict begin
/ode@@dict 1 dict def
/ode@dict {ode@@dict begin} bind def
ode@dict
  %some constants for step size calculation
  /sfty 0.9 def /pgrow -0.2 def /pshrink -0.25 def
  %helper functions
  /addvect { % [1 2 3] [4 5 6] addvect => [5 7 9]
    ode@dict
      aload pop xlength1 -1 roll {xlength1 -1 roll add} forall
      xlength array astore
    end
  } bind def
  /subvect { % [1 2 3] [4 5 6] subvect => [-3 -3 -3]
    ode@dict
      aload pop xlength1 -1 roll {xlength1 -1 roll sub} forall
      xlength array astore
    end
  } bind def
  /mulvect { % [1 2 3] 4 mulvect => [4 8 12]
    ode@dict /mul cvx 2 array astore cvx forall xlength array astore end
  } bind def
  /edivvect { % [1 2 3] [4 5 6] edivvect => [0.25 0.4 0.5]
    ode@dict
      aload pop xlength1 -1 roll {xlength1 -1 roll div} forall
      xlength array astore
    end
  } bind def
  /eabsvect { % [-1 2 -3] eabsvect => [1 2 3]
    ode@dict {abs} forall xlength array astore end
  } bind def
  %/revstack { % (a) (b) (c) (d) 3 revstack => (a) (d) (c) (b)
  %  -1 2 {dup 1 sub neg roll} for
  %} bind def
  /min { 2 copy gt { exch } if pop } bind def
  /max { 2 copy lt { exch } if pop } bind def
  %coefficient table (Butcher table) of RKF45
  /c2 1 4 div def /c3 3 8 div def /c4 12 13 div def /c6 1 2 div def
  /a21 1 4 div def /a31 3 32 div def /a32 9 32 div def
  /a41 1932 2197 div def /a42 7200 2197 div neg def /a43 7296 2197 div def
  /a51 439 216 div def /a52 8 neg def /a53 3680 513 div def
  /a54 845 4104 div neg def /a61 8 27 div neg def /a62 2 def
  /a63 3544 2565 div neg def /a64 1859 4104 div def /a65 11 40 div neg def
  /b1 16 135 div def /b3 6656 12825 div def
  /b4 28561 56430 div def /b5 9 50 div neg def
  /b6 2 55 div def
  /b1* 25 216 div def /b3* 1408 2565 div def
  /b4* 2197 4104 div def /b5* 1 5 div neg def
end
%Runge-Kutta-Fehlberg (RKF45) method
%performs one integration step over tentative step size ddt
%[state vector x(t)] RKF45 => [x(t)] [x(t+ddt) by RKF4] errmax
/RKF45 {
  dup
  /t ode@dict tcur end def
  ODESET
  ode@dict
    ddt mulvect /k1 exch def
    dup k1 a21 mulvect addvect
    tcur ddt c2 mul add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k2 exch def
    dup k1 a31 mulvect addvect k2 a32 mulvect addvect
    tcur ddt c3 mul add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k3 exch def
    dup k1 a41 mulvect addvect k2 a42 mulvect addvect k3 a43 mulvect addvect
    tcur ddt c4 mul add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k4 exch def
    dup k1 a51 mulvect addvect k2 a52 mulvect addvect k3 a53 mulvect addvect
    k4 a54 mulvect addvect
    tcur ddt add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k5 exch def
    dup k1 a61 mulvect addvect k2 a62 mulvect addvect k3 a63 mulvect addvect
    k4 a64 mulvect addvect k5 a65 mulvect addvect
    tcur ddt c6 mul add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k6 exch def % => [x(t)]
    %fourth order solution (increment dx)
    dup dup k1 b1* mulvect k3 b3* mulvect addvect k4 b4* mulvect addvect
      k5 b5* mulvect addvect dup
      % => [x(t)] [x(t)] [x(t)] [dx by RKF4] [dx by RKF4]
    %fifth order solution (abs. error)
    k1 b1 mulvect k3 b3 mulvect addvect k4 b4 mulvect addvect
      k5 b5 mulvect addvect k6 b6 mulvect addvect subvect
      % => [x(t)] [x(t)] [x(t)] [dx by RKF4] [err]
    5 1 roll addvect 4 -2 roll % => [x(t)] [x(t+ddt) by RKF4] [err] [x(t)]
    %scaling vector for step size adjustment (Numerical Recipies)
    eabsvect k1 eabsvect addvect {1e-30 add} forall xlength array astore
    % => [x(t)] [x(t+ddt) by RKF4] [err] [xscale]
    edivvect eabsvect 1e-30 exch {max} forall %maximum rel. error
    % => [x(t)] [x(t+ddt) by RKF4] errmax
  end
} bind def
%classical Runge-Kutta (RK4) method
%one integration step over step size ddt; no error estimate
%[state vector x(t)] RK4 => [x(t+ddt) by RK4]
/RK4 {
  dup
  ode@dict tcur end /t exch def
  ODESET
  ode@dict
    ddt mulvect /k1 exch def
    dup k1 0.5 mulvect addvect
    tcur ddt 2 div add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k2 exch def
    dup k2 0.5 mulvect addvect
  end
  ODESET
  ode@dict
    ddt mulvect /k3 exch def
    dup k3 addvect
    tcur ddt add
  end
  /t exch def
  ODESET
  ode@dict
    ddt mulvect /k4 exch def % => [x(t)]
    k1 k2 k3 addvect 2 mulvect addvect k4 addvect 1 6 div mulvect addvect
    % => [x(t+ddt) by RK4]
  end
} bind def
/ODEINT { % performs integration over output step [t,t+dt]
          % [ state vector x(t) ] ODEINT => [ state vector x(t+dt) ]
  rk4 {
    RK4 (o) odeprint
    ode@dict
      /tcur tout def
      /outStepCnt outStepCnt 1 add def
      /tout tStart dt outStepCnt mul add def
    end
  }{
    %decrease overshooting step size
    ode@dict
      tout tcur sub dup abs ddt abs lt {/ddt exch def}{pop} ifelse
    end
    RKF45
    ode@tol div dup 1 gt {
      %failed step -> reduce step size
      ode@dict
        exch pop pshrink exp 0.1 max sfty mul ddt mul /ddt exch def
        tcur ddt add tcur eq {
          % error: step size underflow in ODEINT
          (! t=) odeprint tcur odeprint
          % print & remove previous state vector
          (, x=[) odeprint /ode@spc () def
          {ode@spc odeprint /ode@spc ( ) def odeprint} forall (]) odeprint
          true
        }{
          (-) odeprint
          false
        } ifelse
      end
      % on step size underflow, leave loop over output steps (pst-ode.tex)
      {exit} if
      ODEINT %repeat step with new ddt
    }{
      %success
      3 -1 roll pop % remove previous state vector
      ode@dict
        /tcur tcur ddt add def
        dup 0 ne {pgrow exp 5 min sfty mul ddt mul /ddt exch def}{pop} ifelse
        %output step completed?
        tcur tout sub
      end
      0 eq {
        (o) odeprint
        ode@dict
          /tcur tout def
          /outStepCnt outStepCnt 1 add def
          /tout tStart dt outStepCnt mul add def
        end
      }{
        (+) odeprint ODEINT %continue integration
      } ifelse
    } ifelse
  } ifelse
} bind def
/writeresult { %write output vector to file
  /loopproc load forall
  statefile (\n) writestring
} bind def
/loopproc {
  0 cvs statefile exch writestring
  statefile ( ) writestring
} bind def
/loopproc load 0 256 string put
/assembleresult { %assembles state vector for building table of results
  {
    dup (t) eq {
      pop ode@dict tcur end
    }{
      ode@laststate exch get
    } ifelse
  } forall
} bind def
end
