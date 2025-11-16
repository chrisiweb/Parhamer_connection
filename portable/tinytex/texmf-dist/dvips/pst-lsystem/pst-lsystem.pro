%% pst-lsystem.pro (c) sep 22, 2018 Herbert Voss
%% version 0.01 2018/09/22  
%
% based on the work of Michel Charpentier
%
/tx@lsystemDict 6 dict def
tx@lsystemDict begin

/fast? true def % choice between faster or nicer

/D { Element 0 rlineto } bind def

/B [ % quite dirty, but it works...
  fast? { {currentpoint stroke moveto} aload pop } if
  {gsave} aload pop
  { dup color } aload pop 
] cvx bind def

%/B { currentpoint stroke moveto gsave } bind def
/E { stroke grestore } bind def
/- { angle neg rotate } def % rotation to the right 
/+ { angle rotate } def % rotation to the left
%

end

