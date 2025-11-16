%% $Id: pst-feyn.pro 826 2018-09-27 09:21:43Z herbert $
%%
%% This is file `pst-feyn.pro',
%% It is based on the old axodraw package from Jos Vermaseren
%%
%% IMPORTANT NOTICE:
%%
%% Package `pst-feyn.tex'
%%
%% Herbert Voss <hvoss _at_ tug.org>
%%
%% This program can be redistributed and/or modified under the terms
%% of the LaTeX Project Public License Distributed from CTAN archives
%% in directory macros/latex/base/lppl.txt.
%%
%% DESCRIPTION:
%%   `pst-feyn' is a PSTricks package to draw 3d curves and graphical objects
%%
%%
%% version 0.01 / 2018-09-26  Herbert Voss <hvoss _at_ tug.org>
%%            
%
/tx@FeynDict 100 dict def
tx@FeynDict begin
%
/ED { exch def } def
/SLW { setlinewidth } def
/p1 {/y1 ED /x1 ED } def
/p2 {/y2 ED /x2 ED } def 
/abox{ newpath x1 y1 moveto x1 y2 lineto x2 y2 lineto x2 y1 lineto closepath } def 
%
%
/arrowdown{
    /nwidth { CLW 1 add } def
    newpath
        0 nwidth 1.5 mul neg moveto         % Arrow is a triangle
        nwidth 1.2 mul nwidth 3 mul rlineto
        nwidth 2.4 mul neg 0 rlineto
        nwidth 1.2 mul nwidth 3 mul neg rlineto
    closepath fill                          % and it is filled
} def 
%
/arrowup{
    /nwidth { CLW 1 add } def
    newpath
        0 nwidth 1.5 mul moveto             % Arrow is a triangle
        nwidth 1.2 mul nwidth 3 mul neg rlineto
        nwidth 2.4 mul neg 0 rlineto
        nwidth 1.2 mul nwidth 3 mul rlineto
    closepath fill                          % and it is filled
} def 
%
/arrowright{
    /nwidth { CLW 1 add } def
    newpath
        nwidth 1.5 mul 0 moveto             % Arrow is a triangle
        nwidth 3 mul neg nwidth 1.2 mul rlineto
        0 nwidth 2.4 mul neg rlineto
        nwidth 3 mul nwidth 1.2 mul rlineto
    closepath fill                          % and it is filled
} def 
%
/gluon{
    %dup scale /width ED width SLW 
    /num ED /ampi ED /y2 ED /x2 ED /y1 ED /x1 ED

    /dy y2 y1 sub def /dx x2 x1 sub def
%
%   We have a 'head' and a 'tail' and inbetween the 'body'
%   The head + tail is 2 windings. The body is num-1 windings.
%
    /dr dx dx mul dy dy mul add sqrt def
%
    x1 y1 translate dy dx atan rotate
%
    /num num 0.5 sub round def
    /inc dr num 2 mul 2 add div def         % increment per half winding
    /amp8 ampi 0.9 mul def
    amp8 0 lt {/amp8 amp8 neg def} if
%
    /x1 inc 2 mul def
%
    newpath
        0 0 moveto
        inc 0.1 mul ampi 0.5 mul inc 0.5 mul ampi inc 1.4 mul ampi curveto
        x1 amp8 add dup ampi exch ampi neg dup x1 exch curveto
%
        2 1 num {
            pop
            x1 amp8 sub dup ampi neg exch ampi dup x1 inc add exch curveto
            /x1 x1 inc dup add add def
            x1 amp8 add dup ampi exch ampi neg dup x1 exch curveto
        } for
%
        x1 amp8 sub dup ampi neg exch ampi dup x1 inc 0.6 mul add exch curveto
        x1 inc 1.5 mul add ampi dr inc 0.1 mul sub ampi 0.5 mul dr 0 curveto
%    stroke
%
} def 
%
/photon{
%
%   Draws a photon from x1,y1 to x2,y2 with amplitude A and n wiggles
%
%    gsave dup scale /width ED width SLW 
    /num ED /ampi ED p2 p1
    /dy y2 y1 sub def /dx x2 x1 sub def
    /dr dx dx mul dy dy mul add sqrt def
%
    x1 y1 translate
    dy dx atan rotate
    /num num 2 mul 0.5 sub round def
    /x2 dr num div def
    /pi 3.141592 def
    /sign 1 def
    1 1 num {
        pop
        newpath
        0 0 moveto
        4 3 div x2 mul pi div dup neg x2 add
        4 3 div ampi sign mul mul dup 3 1 roll
        x2 0 curveto
        stroke
        /sign sign neg def
        x2 0 translate
    } for
%
%    grestore
} def 
%
/zigzag{
%
%   Draws a zigzag line from x1,y1 to x2,y2 with amplitude A and n zigzags
%
%    gsave dup scale /width ED width SLW 
    /num ED /ampi ED p2 p1
    /dy y2 y1 sub def /dx x2 x1 sub def
    /dr dx dx mul dy dy mul add sqrt def
%
    x1 y1 translate
    dy dx atan rotate
    /num num 2 mul 0.5 sub round def
    /x2 dr num div def
    /pi 3.141592 def
    /sign 1 def
    1 1 num {
        pop
        newpath
        0 0 moveto
        x2 2 div ampi sign mul lineto
        x2 0 lineto
        stroke
        /sign sign neg def
        x2 0 translate
    } for
%
%    grestore
} def 
%
/photonarc{
%
%   Draws a photonarc center at x1,y1, radius arcstart,arcend, amplitude
%       number of wiggles,  width, scale
%
%    gsave dup scale /width ED width SLW 
    /num ED /ampli ED /arcend ED /arcstart ED /radius ED
%
    translate       % The center of the circle is now the origin
%
    /num num 2 mul round def    % number of half wiggles
    arcend arcstart lt { /arcend arcend 360 add def } if
    /arcend arcend arcstart sub num div def    % phi
    arcstart rotate
    /arcstart arcend 2 div def                 % phi/2
    /cp arcend cos def
    /sp arcend sin def
    /cp2 arcstart cos def
    /sp2 arcstart sin def
%
    newpath
    1 1 num {
        pop
        radius 0 moveto
        /beta radius arcend mul 180 ampli mul div def
        /tt sp cp beta mul sub cp sp beta mul add div def
        /amp1 radius ampli add 8 mul beta cp2 mul sp2 sub mul beta 4 cp add mul
            tt cp mul 3 mul sp 4 mul sub add radius mul sub
            beta tt sub 3 mul div def           % this is x2
        radius ampli add 8 mul cp2 mul 1 cp add radius mul sub 3 div amp1 sub
            dup radius sub beta mul             % x1,y1
        amp1 dup radius cp mul sub tt mul radius sp mul add     % x2,y2
        radius cp mul radius sp mul             % x3 y3
                curveto
        /ampli ampli neg def
        arcend rotate
    } for
%    stroke
%
%    grestore
} def
%
/gluearc{
%
%   Draws a gluon on an arcsegment
%   radius,stat_angle,end_angle,gluon_radius,num
%   in which num is the number of windings of the gluon.
%   Method:
%   1:  compute length of arc.
%   2:  generate gluon in x and y as if the arc is a straight line
%   3:  x' = (radius+y)*cos(x*const)
%       y' = (radius+y)*sin(x*const)
%
    gsave %dup scale /width ED width SLW 
    /num ED 
    /ampi ED 
    /arcend ED 
    /arcstart ED 
    /radius ED
%
    arcstart rotate                         % segment starts at zero
    /darc arcend arcstart sub def           % argsegment
    /dr darc 180 div 3.141592 mul radius mul def  % length of segment.
    /const darc dr div def                  % conversion constant
%
    /num num 0.5 sub round def
    /inc dr num 2 mul 2 add div def         % increment per half winding
%
    /amp8 ampi 0.9 mul def
    /amp1 radius ampi add def
    /amp2 radius ampi sub def
    /amp3 radius ampi 2 div add def
    /amp4 amp1 inc amp8 add const mul cos div def
    /amp5 amp2 amp8 const mul cos div def
    /amp6 amp1 inc 0.6 mul amp8 add const mul cos div def
    /amp7 amp1 inc 0.9 mul const mul cos div def
    amp8 0 lt {/amp8 amp8 neg def} if
%
    /x1 inc 2 mul def
%
    newpath
        radius 0 moveto
%
        inc 0.1 mul const mul dup cos amp3 mul exch sin amp3 mul
        inc 0.5 mul const mul dup cos amp7 mul exch sin amp7 mul
        inc 1.4 mul const mul dup cos amp1 mul exch sin amp1 mul
            curveto
        x1 amp8 add const mul dup cos amp6 mul exch sin amp6 mul
        x1 amp8 add const mul dup cos amp5 mul exch sin amp5 mul
        x1 const mul dup cos amp2 mul exch sin amp2 mul
            curveto
%
        2 1 num {
            pop
            x1 amp8 sub const mul dup cos amp5 mul exch sin amp5 mul
            x1 amp8 sub const mul dup cos amp4 mul exch sin amp4 mul
            x1 inc add const mul dup cos amp1 mul exch sin amp1 mul
                curveto
            /x1 x1 inc dup add add def
            x1 amp8 add const mul dup cos amp4 mul exch sin amp4 mul
            x1 amp8 add const mul dup cos amp5 mul exch sin amp5 mul
            x1 const mul dup cos amp2 mul exch sin amp2 mul
                curveto
        } for
%
        x1 amp8 sub const mul dup cos amp5 mul exch sin amp5 mul
        x1 amp8 sub const mul dup cos amp6 mul exch sin amp6 mul
        x1 inc 0.6 mul add const mul dup cos amp1 mul exch sin amp1 mul
            curveto
        x1 inc 1.5 mul add const mul dup cos amp7 mul exch sin amp7 mul
        dr inc 0.1 mul sub const mul dup cos amp3 mul exch sin amp3 mul
        dr const mul dup cos radius mul exch sin radius mul
        curveto
    stroke
%
    grestore
} def 
%
/arrowarc{
%
%   Draws an anticlockwise arc with an arrow in the middle
%   The arc is   x_center, y_center, radius, start_angle, end_angle
%
%    gsave dup scale /width ED width SLW 
    /arcend ED /arcstart ED /radius ED
%
    translate                               % x and y are still on stack
    newpath 0 0 radius arcstart arcend arc stroke
    arcstart arcend gt {
        /arcend arcend 360 add def } if
    arcstart arcend add 2 div rotate        % middle of arc
    radius 0 translate                      % move to it
    arrowup
%    grestore
} def 
%
/longarrowarc{
%
%   Draws an anticlockwise arc with an arrow at the end
%   The arc is   x_center, y_center, radius, start_angle, end_angle
%
%    gsave dup scale /width ED width SLW 
    /arcend ED /arcstart ED /radius ED
%
    translate                               % x and y are still on stack
    arcstart arcend gt {
        /arcend arcend 360 add def } if
    /arcmid 540 CLW 1 add mul 3.14159 div radius div def
                                            % discount for arrow
%    newpath 0 0 radius arcstart arcend arcmid sub arc stroke
    arcend arcmid 2 div sub rotate          % middle of arrow
    radius 0 translate                      % move to it
    arrowup
%    grestore
} def 
%
/dasharrowarc{
%
%   Draws a dashed anticlockwise arc with an arrow in the middle
%   The arc is   x_center, y_center, radius, start_angle, end_angle dsize
%
    gsave dup scale /width ED width SLW /dsize ED /arcend1 ED /arcstart1 ED /radius ED
%
    translate                               % x and y are still on stack
%
    arcend1 arcstart1 lt { /arcend1 arcend1 360 add def } if
    /arcmid1 arcend1 arcstart1 add 2 div def
%
    0 0 radius arcstart1 arcmid1 dsize width 1 dashcarc
    0 0 radius arcmid1 arcend1 dsize width 1 dashcarc
    arcmid1 rotate
    radius 0 translate
    arrowup
    grestore
} def 
%
/arrowarcn{
%
%   Draws a clockwise arc with an arrow in the middle
%   The arc is   x_center, y_center, radius, start_angle, end_angle
%
%    gsave dup scale /width ED width SLW 
    /arcend ED /arcstart ED /radius ED
%
    translate                               % x and y are still on stack
    newpath 0 0 radius arcstart arcend arcn stroke
    arcstart arcend lt {
        /arcstart arcstart 360 add def } if
    arcstart arcend add 2 div rotate        % middle of arc
    radius 0 translate                      % move to it
    arrowdown
%    grestore
} def
%
/longarrowarcn{
%
%   Draws a clockwise arc with an arrow in the end
%   The arc is   x_center, y_center, radius, start_angle, end_angle
%
    gsave dup scale /width ED width SLW /arcend ED /arcstart ED /radius ED
%
    translate                               % x and y are still on stack
    arcstart arcend lt {
        /arcstart arcstart 360 add def } if
    /arcmid 540 width 1 add mul 3.14159 div radius div def
                                            % correction for arrow
    newpath 0 0 radius arcstart arcend arcmid add arcn stroke
    arcend arcmid 2 div add rotate          % middle of arrow
    radius 0 translate                      % move to it
    arrowdown
    grestore
} def 
%
/dasharrowarcn{
%
%   Draws a dashed clockwise arc with an arrow in the middle
%   The arc is   x_center, y_center, radius, start_angle, end_angle
%
    gsave dup scale /width ED width SLW /dsize ED /arcend1 ED /arcstart1 ED /radius ED
%
    translate                               % x and y are still on stack
    arcstart1 arcend1 lt {
        /arcstart1 arcstart1 360 add def } if
    /arcmid1 arcstart1 arcend1 add 2 div def
    0 0 radius arcmid1 arcstart1 dsize width 1 dashcarc
    0 0 radius arcend1 arcmid1 dsize width 1 dashcarc
    arcmid1 rotate
    radius 0 translate
    arrowdown
    grestore
} def 
%
/arrowline{
%
%   Draws a straight line with an arrow in the middle
%   x1,y1,x2,y2
%
    %gsave dup scale /width ED width SLW 
    p2 p1
    /dx x2 x1 sub def /dy y2 y1 sub def
    /dr dx dx mul dy dy mul add sqrt def
%
    x1 y1 translate
%    newpath
%        0 0 moveto
%        dx dy rlineto
%    stroke
    dy dx atan rotate
    dr 2.0 div 0 translate
    arrowright
%    grestore
} def 
%
/longarrow{
%
%   Draws a straight line with an arrow at the end
%   x1,y1,x2,y2
%
    gsave dup scale /width ED width SLW p2 p1
    /dx x2 x1 sub def /dy y2 y1 sub def
    /dr dx dx mul dy dy mul add sqrt def
%
    x1 y1 translate
    dy dx atan rotate
    newpath
        0 0 moveto
        dr width 3 mul sub 0 rlineto
    stroke
    dr width 1.5 mul sub 0 translate
    arrowright
    grestore
} def 
%
/dasharrowline{
%
%   Draws a straight dashed line with an arrow in the middle
%   x1,y1,x2,y2
%
%   The pattern is ideally [dsize dsize] 0 setdash
%   but we want to have (2*n+1)/2 patterns, so dsize must be rounded
%   Actually we want the center to be black too so that the arrow
%   fits in nice. This means that n must be odd. So
%   r = dsize*(4*m+3)
%
    gsave dup scale /width ED width SLW /dsize ED p2 p1
    /dx x2 x1 sub def /dy y2 y1 sub def
    /dr dx dx mul dy dy mul add sqrt 2 div def
%
    x1 y1 translate
    dy dx atan rotate
%
    0 0 dr 0 dsize width 1 dashline
    dr 0 translate
    0 0 dr 0 dsize width 1 dashline
    arrowright
    grestore
} def 
%
/carc{
%
%   Draws an anti-clockwise arc segment:
%   x_center, y_center, radius, start_angle, end_angle
%
    %dup scale /width ED width SLW 
    /arcend ED /arcstart ED /radius ED
%
    translate                               % x and y are still on stack
    newpath 0 0 radius arcstart arcend arc 
%    stroke
%    grestore
} def 
%
/dashcarc{
%
%   Draws an anti-clockwise arc segment:
%   x_center, y_center, radius, start_angle, end_angle, dsize
%
    gsave dup scale /width ED width SLW /dsize ED /arcend ED /arcstart ED /radius ED
%
    translate                               % x and y are still on stack
%
%   Compute the length of the line
%
    /dr arcend arcstart sub dup 0 lt { 360 add } if
        3.14159 mul 180 div radius mul def
    /dsize dr dsize 2 mul div 0.5 sub round dup 0 le { pop 0 } if 2 mul 1 add
    dr exch div def
    [dsize dsize] 0 setdash
%
    newpath 0 0 radius arcstart arcend arc stroke
    grestore
} def 
%
/bcirc{
%
%   Draws an anti-clockwise blanked circle:
%   x_center, y_center, radius
%
    gsave dup scale /width ED width SLW /radius ED
%
    translate                               % x and y are still on stack
%
    gsave
    1 setgray
    newpath 0 0 radius 0 360 arc fill
    grestore
    newpath 0 0 radius 0 360 arc stroke
    grestore
} def 
%
/gcirc{
%
%   Draws an anti-clockwise blanked gray circle:
%   x_center, y_center, radius, grayscale
%
    gsave dup scale /width ED width SLW /gcolor ED /radius ED
%
    translate                               % x and y are still on stack
%
    1 setgray
    newpath 0 0 radius 0 360 arc fill
    gcolor setgray
    newpath 0 0 radius 0 360 arc fill
    0 setgray
    newpath 0 0 radius 0 360 arc stroke
    grestore
} def 
%
/ccirc1{
%
%   Draws an anti-clockwise circle :
%   x_center, y_center, radius
%   Part 1: the contents in background color
%
    gsave dup scale /width ED width SLW /radius ED
%
    translate                               % x and y are still on stack
%
    newpath 0 0 radius 0 360 arc fill
    grestore
} def 
%
/ccirc2{
%
%   Draws an anti-clockwise circle :
%   x_center, y_center, radius
%   Part 1: the contents in background color
%
    gsave dup scale /width ED width SLW /radius ED
%
    translate                               % x and y are still on stack
%
    newpath 0 0 radius 0 360 arc stroke
    grestore
} def 
%
%
/pathlength{
    flattenpath
    /dist 0 def
    { /yfirst ED /xfirst ED /ymoveto yfirst def /xmoveto xfirst def }
    { /ynext ED /xnext ED /dist dist ynext yfirst sub dup mul
        xnext xfirst sub dup mul add sqrt add def
        /yfirst ynext def /xfirst xnext def }
    {}
    {/ynext ymoveto def /xnext xmoveto def
        /dist ynext yfirst sub dup mul
              xnext xfirst sub dup mul add sqrt add def
        /yfirst ynext def /xfirst xnext def }
    pathforall
    dist
} def 
%
/centerdash{
    /pathlen pathlength def
    /jj pathlen dsize div 2.0 div cvi def
    /ddsize pathlen jj 2.0 mul div def
    [ddsize] ddsize 2 div setdash
} def 
%
/logaxis{
%
%   Draws an axis from x1,y1 to x2,y2 with nl log divisions
%   size of the hashes hs, offset F
%   and width W. The stack looks like
%   x1,y1,x2,y2,nl,hs,F,W,scale
%   After the rotation the hash marks are on top if nl is positive and
%   on the bottom if nl is negative
%
%    gsave dup scale /width ED width SLW 
    /offset ED /hashsize ED /nlogs ED p2 p1
    x1 y1 translate
    /y2 y2 y1 sub def /x2 x2 x1 sub def
    y2 x2 atan rotate
    /rr x2 dup mul y2 dup mul add sqrt def
    offset 0 ne { /offset offset ln 10 ln div def } if
    /offset offset dup cvi sub def
    newpath
        0 0 moveto
        rr 0 lineto
    /lsize rr nlogs div def
    0 1 nlogs { /x2 ED
        x2 offset ge {
            /y2 x2 offset sub lsize mul def
            y2 rr le {
                y2 0 moveto
                y2 hashsize 1.2 mul lineto
            } if
        } if
    } for
    stroke
    CLW 0.6 mul setlinewidth
    newpath
    0 1 nlogs { /x2 ED
        2 1 9 {
            ln 10 ln div x2 add
            /xx2 ED
            xx2 offset ge {
                /y2 xx2 offset sub lsize mul def
                y2 rr le {
                    y2 0 moveto
                    y2 hashsize 0.8 mul lineto
                } if
            } if
        } for
    } for
%    stroke
%    grestore
} def 
%
/linaxis{
%
%   x1,y1,x2,y2,num_decs,per_dec,hashsize,offset,width,scale
%
    %gsave dup scale /width ED width SLW 
    /offset ED /hashsize ED /perdec ED /numdec ED p2 p1
    x1 y1 translate
    /y2 y2 y1 sub def /x2 x2 x1 sub def
    y2 x2 atan rotate
    /rr x2 dup mul y2 dup mul add sqrt def
    newpath
        0 0 moveto
        rr 0 lineto
    /x1 rr numdec perdec mul div def
    /y1 rr numdec div def
    /offset offset x1 mul def 
    0 1 numdec { y1 mul offset sub
        dup 0 ge {
            dup rr le {
                dup 0 moveto
                hashsize 1.2 mul lineto
            } if
        } if
    } for
    stroke
    CLW 0.6 mul setlinewidth
    newpath
    offset cvi 1 numdec perdec mul offset add {
        x1 mul offset sub
        dup 0 ge {
            dup rr le {
                dup 0 moveto
                hashsize 0.8 mul lineto
            } if
        } if 
    } for
    stroke
    %grestore
} def 
%
end % tx@FeynDict
%