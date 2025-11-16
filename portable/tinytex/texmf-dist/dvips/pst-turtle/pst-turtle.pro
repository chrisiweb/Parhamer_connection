% turtle.ps -- graphics turtle.
% @author Eric Laroche
% @version @(#)$Id: pst-turtle.pro 1092 2019-10-01 20:19:35Z herbert $
%
% turtle.ps -- graphics turtle.
% Copyright (C) 1997-2001 Eric Laroche.
%
% This program is free software;
% you can redistribute it and/or modify it.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
%
% the '(graphics) turtle' is a 'cursor' that has a position (x and y
% coordinate), a heading and a pen up/down state.  procedures as
% forward, left, etc. are used as drawing idioms.
%
% the turtle object consists of: cx cy phi penstate.  cx and cy are the
% initialial coordinates, established when creating the turtle, they are
% the turtles zero coordinates.  phi is the turtle heading, zero means
% in x direction (i.e. to the right), 90 means in the y direction (i.e.
% up).  penstate is a boolean indicating whether the pen is down (true)
% or up (false).
% implicit to the turtle object is: currentpoint.
%
% note that using path constructing operators moveto, rmoveto, lineto,
% rlineto, arc, etc. will affect the turtle's state in a way that the
% turtle's current point is changed together with the postscript vm's
% current point by these operators.  contrary the turtle's heading
% isn't affected by these operators.
%
% the turtle procedures indicate syntaxes using <turtle> (an array
% containing the turtle state) as abstract turtle object.
%
% no syntax is indicated with the abbreviated function names.
%
% these procedures are not handling newpath, closepath,
% setlinewidth, setlinejoin, setlinecap, stroke, fill, etc.
%
% a current point must be set before using the turtle object and after
% starting a new path.  i.e. a typical initialization sequence would be
% e.g. 'newpath 200 200 moveto turtle 90 setheading'.
%
% create a turtle object.
% this saves the current point as zero point to return to by 'home'.
% a turtle object is an array of: [cx cy phi penstate].
% - turtle -> <turtle>
%
% on stack: { x y } boolean N@name type InitXnode

/tx@TurtleDict 50 dict def
tx@TurtleDict begin
%
/nodeCounter 0 def
/nodeCnt++ { nodeCounter 1 add /nodeCounter exch def }  def

%/saveNode {
%  { currentpoint } 
%  false
%  (N@Turtle) nodeCounter 2 string cvs concatstrings 32 rightTrim cvn 
%  10
%  {InitPnode}
%  tx@NodeDict begin NewNode end
%  nodeCnt++
%} def

/saveNode {
  tx@Dict begin
  (Turtle) nodeCounter 2 string cvs concatstrings 32 rightTrim cvn { currentpoint } def 
  end
} def
%
/turtle {
	% get initial position.
	% initial position is current point.
	2 setlinejoin
	currentpoint
	% phi and penstate
	0 true
	% note: not doing any newpath.
	4 array astore
} bind def

% destroy a turtle object.
% note: this procedure serves for compatibility
% to older turtle formats.
% <turtle> unturtle -> -
/unturtle {
	% return to turtle object's initial position.
	dup 0 get
	1 index 1 get % <turtle> cx cy
	moveto
	% note: not doing any newpath.
	pop % -
} bind def

% return turtle object size.
% note: this procedure serves for compatibility
% to older turtle formats.
% - turtlesize -> 1
/turtlesize {
	% 1 entry on the stack (an array with cx cy phi penstate).
	1
} bind def

% normalize direction.  phi must be >= 0 and < 360.
% <turtle> normalizephi -> <turtle>
/normalizephi {
	dup 2 get % <turtle> phi
	% note: denormalized typically by less than two circles,
	% so the loops won't take too long.
	% cut while larger or equal 2 pi.
	{
		dup 360 % <turtle> phi phi 360
		lt {
			exit
		} if
		360 sub
	} loop
	% increment while less zero.
	{
		dup 0 % <turtle> phi phi 0
		ge {
			exit
		} if
		360 add
	} loop
	exch dup 2
	4 -1 roll
	put % <turtle>
} bind def

% relatively move to, action depending on penstate.
% <turtle> dx dy pmoveto -> <turtle>
/pmoveto {
	% move or draw, depending on penstate
	2 index 3 get {
		rlineto
	} {
		rmoveto
	} ifelse
} def

% where we are, from initial point (in setxy coordinates).
% <turtle> xy -> <turtle> x y
/xy {
	currentpoint % <turtle> x' y'
	exch 2 index 0 get sub % <turtle> y' x
	exch 2 index 1 get sub % <turtle> x y
} bind def

% calculate relative movements from setxy coordinates.
% <turtle> x y rxy -> <turtle> x' y'
/rxy {
	3 -1 roll % x y <turtle>
	xy % x y <turtle> x'' y''
	5 -2 roll % <turtle> x'' y'' x y
	exch 4 -1 roll sub
	exch 3 -1 roll sub % <turtle> x' y'
} bind def


% logo language turtle functions

% put penstate in 'up' position.
% logo language turtle function
% <turtle> penup -> <turtle>
/penup {
	% false means 'up'.
	dup 3 false put
} bind def

% put penstate in 'down' position.
% logo language turtle function
% <turtle> pendown -> <turtle>
/pendown {
	% true means 'down'.
	dup 3 true put
} bind def

% advance in current direction.
% logo language turtle function
% <turtle> d forward -> <turtle>
/forward {
	% dx is d cos phi.
	1 index 2 get cos 1 index mul % <turtle> d dx
	% dy is d sin phi.
	2 index 2 get sin 3 -1 roll mul % <turtle> dx dy
	pmoveto
	saveNode
} def

% back up in current direction.
% logo language turtle function
% <turtle> d back -> <turtle>
/back {
	neg
	forward
} bind def

% change direction to the left (counterclockwise, positive direction).
% logo language turtle function
% <turtle> omega left -> <turtle>
/left {
	1 index 2 get % <turtle> omega phi
	add % <turtle> phi'
	1 index 2 3 -1 roll put
	normalizephi
} bind def

% change direction to the right (clockwise, negative direction).
% logo language turtle function
% <turtle> omega right -> <turtle>
/right {
	neg
	left
} bind def

% move to a specified point.
% logo language turtle function
% <turtle> x y setxy -> <turtle>
/setxy {
	rxy % <turtle> x' y'
	pmoveto % <turtle>
} bind def

% move to a specified point (only x changes).
% logo language turtle function
% <turtle> x setx -> <turtle>
/setx {
	0 rxy % <turtle> x' y'
	pop 0 pmoveto % <turtle>
} bind def

% move to a specified point (only y changes).
% logo language turtle function
% <turtle> y sety -> <turtle>
/sety {
	0 exch rxy % <turtle> x' y'
	exch pop 0 exch pmoveto % <turtle>
} bind def

% set the heading.
% logo language turtle function
% <turtle> phi' setheading -> <turtle>
/setheading { 1 index 2 3 -1 roll put normalizephi } bind def

% set heading towards a point.
% logo language turtle function
% <turtle> x y towards -> <turtle>
/towards {
	rxy % <turtle> x' y'
	% check if both zero.
	1 index 0 eq 1 index 0 eq and {
		% set heading to zero.
		pop pop 0
	} {
		exch atan
	} ifelse
	setheading
} bind def

% go home; heading to zero.
% logo language turtle function
% <turtle> home -> <turtle>
/home { 0 dup setxy 0 setheading } bind def

% get x coordinate.
% logo language turtle function
% <turtle> xcor -> cx <turtle> x
/xcor { xy pop } bind def

% get y coordinate.
% logo language turtle function
% <turtle> ycor -> <turtle> y
/ycor { xy exch pop } bind def

% get heading.
% logo language turtle function
% <turtle> heading -> <turtle> phi
/heading { dup 2 get } bind def

% get pen state.
% logo language turtle function
% note: only the turtle relevant stuff given.
% <turtle> drawstate -> <turtle> penstate
/drawstate { dup 3 get } bind def
%
% logo language turtle function abbreviations
%
/bk { back } bind def
/fd { forward } bind def
/lt { left } bind def
/pd { pendown } bind def
/pu { penup } bind def
/rt { right } bind def
/seth { setheading } bind def
%
end
% end of pst-turtle.pro

