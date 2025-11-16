%% $Id: pst-antiprism.pro 522 2017-08-23 09:03:52Z herbert $
%% PostScript prologue for pst-antiprism.tex.
%%
%% Version 0.02, 2018/02/12
%%
%% For distribution, see pst-antiprism.tex.
%%
%% 
/ps@antiprism { 12 dict begin
  /n exch def        	% cotè du polygone
  /a exch def 		% length on the antiprism side
  /angle 360 n div def
  % hauteur entre les 2 plans
  /h a 1 1 angle 4 div cos 2 mul dup mul div sub sqrt mul 2 div def
  % rayon du cercle circonscrit au polygone
  /r a 2 div angle 2 div sin div def
  % Les sommets des polygones réguliers supérieur et inférieur, alternativement
  % inscrit dans un cercle de rayon 1
  /sommets [ % 0->2n-1
    0 1 n 1 sub {
      /k exch def
      angle k mul cos r mul
      angle k mul sin r mul
      h
      k 0.5 add angle mul cos r mul
      k 0.5 add angle mul sin r mul
      h neg
    } for
    meshbases {         % les centres de 2 faces polygonales
      0 0 h      % né 2n
      0 0 h neg  % né 2n+1
    } if
  ] def
  % les faces
  /faces [
    /i 0 def
    n {
       [0 i add 1 i add 2 i add ]
      /i i 2 add def
    } repeat
  /i 0 def
  n {
    [1 i add 3 i add 2 i add ]
    /i i 2 add def
  } repeat
  meshbases {
    % les faces sup et inf en triangles
    /i 0 def
    n 1 sub {
      [2 n mul 0 i add 2 i add ]
      /i i 2 add def
    } repeat
    [2 n mul 2 n mul 2 sub 0 ]
    /i 0 def
    n 1 sub {
      [2 n mul 1 add 3 i add 1 i add ]
      /i i 2 add def
    } repeat
    [2 n mul 1 add 1 2 n mul 1 sub ]
  }{  % face polygonale sup
    [ 0 2 2 n mul 2 sub {} for ]
	% face polygonale inf
    [ 1 2 2 n mul 1 sub {} for ]
  } ifelse
  ] def
  faces n 1 sub get 2 0 put
  faces 2 n mul 1 sub get 1 1 put 
  faces 2 n mul 1 sub get 2 0 put 
  % dans le cas oé les bases ne sont pas étoilées
  % base sup = 2n
  % base inf = 2n+1
  %facessup faces 2 n mul get
  %facesinf faces 2 n mul 1 get
  %facestemp faces 0 2 n 1 sub getintervall
  %
  meshbases {}{
    /faces1 faces faces length 2 sub 2 getinterval def
    /faces2 faces 0 faces length 2 sub getinterval def
    /faces [faces1 aload pop faces2 aload pop] def
  } ifelse
  sommets faces generesolid
end
}  def
%
/ps@antiprism-fan {
  10 dict begin
  /n exch def
  % coté du polygone
  /a exch def % length on the antiprism side
  /angle 360 n div def
  % hauteur entre les 2 plans
  /h a
   1
   1
   angle 4 div cos 2 mul dup mul div sub sqrt mul 2 div def
% rayon du cercle circonscrit au polygone
/r a 2 div angle 2 div sin div def
% Les sommets des polygones r�guliers sup�rieur et inf�rieur, alternativement
% inscrit dans un cercle de rayon r
/sommets [ % 0->2n-1
0 1 n 1 sub {/k exch def
    angle k mul cos r mul
    angle k mul sin r mul
    h
    k 0.5 add angle mul cos r mul
    k 0.5 add angle mul sin r mul
    h neg
    } for
% les centres de 2 faces polygonales
 0 0 h      % n� 2n
 0 0 h neg  % n� 2n+1
 ] def
% les faces
/faces [
0 2 n 2 mul 3 sub {/i exch def
[
 i
 i 1 add
 2 n mul 1 add
 2 n mul
 ]
[
 i 1 add
 i 2 add
 2 n mul
 2 n mul 1 add
 ]
} for
[
 2 n mul
 2 n mul 2 sub 2 n mul 1 sub 2 n mul 1 add
]
[
 2 n mul 1 sub
 0
 2 n mul
 2 n mul 1 add
] 
] def
sommets faces generesolid
end
}  def
%
/pst-antiprism-fan {
   a n@ ps@antiprism-fan
   gere_pstricks_opt
} def
%
/pst-antiprism {
   a n@ ps@antiprism
   gere_pstricks_opt
} def
%
%