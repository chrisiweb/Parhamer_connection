%% $Id: pst-shell.pro 364 2016-12-23 17:09:10Z herbert $
%%
%% This is file `pst-shell.pro',
%%
%% IMPORTANT NOTICE:
%%
%% Package `pst-shell'
%%
%% Manuel Luque <manuel.luque27@gmail.com> (France)
%% Herbert Voss <hvoss@tug.org> (Germany)
%%
%% This program can be redistributed and/or modified under the terms
%% of the LaTeX Project Public License Distributed from CTAN archives
%% in directory macros/latex/base/lppl.txt.
%%
%% DESCRIPTION:
%%   `pst-shell' is a PSTricks package to plot sea shells
%%
%%
%% version 0.01 / 2016-12-23  Herbert Voss
%
/tx@ShellDict 20 dict def
tx@ShellDict begin
%
/gtheta {
  360 shell@N div
  shell@N u mul 360 div
  shell@N u mul 360 div truncate
  sub
  mul
} def
/Radius {
  1
  v cos shell@a div dup mul
  v sin shell@b div dup mul
  add sqrt div
} def
%
/Rw {
  shell@Wi shell@Wii mul shell@N mul 0 eq
    {0}
    {
      shell@L
      Euler
      2 v shell@P sub shell@Wi div mul dup mul neg
      gtheta
      shell@Wii div 2 mul dup mul neg add
      exp
      mul
    } ifelse
} def
/hstheta { Radius Rw add } def
/Expo { Euler u DegtoRad shell@alpha tan div exp } def
/xShell {
  shell@D
  shell@A shell@beta sin mul u cos mul
  hstheta
  v shell@phi add cos u shell@Omega add cos mul
  shell@mu sin v shell@phi add sin mul u shell@Omega add sin mul
  sub
  mul
  add
  Expo mul
  mul
} def
/yShell {
  shell@A neg shell@beta sin mul u sin mul
  hstheta
  v shell@phi add cos u shell@Omega add sin mul
  shell@mu sin v shell@phi add sin mul u shell@Omega add cos mul
  add
  mul
  sub
  Expo mul
} def
/zShell {
  shell@A neg shell@beta cos mul
  hstheta
  v shell@phi add sin
  shell@mu cos mul
  mul add
  Expo mul
} def
%
end
%%