function plot_topoD()
% PLOT_TOPO plots the topo from file FNAME


close all;

% Top of the cinder cone.  Pass these values into plot_feature
% to get the height of the feature. 
 xp = 3.0206e+03;
 yp = 1.1689e+04;

c = 'w';  % Color of the topo
[p1,ax1,bx1,ay1,by1] = plot_feature('TetonDamLargeLowRes.topo2',c);
hold on;
[p2,ax2,bx2,ay2,by2] = plot_feature('TetonDamBigNorth.topo2',c);
hold on;
[p3,ax3,bx3,ay3,by3] = plot_feature('tetontopo',c);

%fprintf('Height at input location : %12.4f\n',hp);

daspect([1,1,1]);

axis([ax1 bx1 ay1 by1]);

camlight;

view(2);


end

function [p,ax,bx,ay,by] = plot_feature(fname,c,xp,yp)

fid = fopen(fname);

ncols = fscanf(fid,'%d',1); fscanf(fid,'%s',1);
nrows = fscanf(fid,'%d',1); fscanf(fid,'%s',1);
xll = fscanf(fid,'%g',1); one = fscanf(fid,'%s',1);
yll = fscanf(fid,'%g',1); two = fscanf(fid,'%s',1);
dx = fscanf(fid,'%g',1);    fscanf(fid,'%s',1);
nodata = fscanf(fid,'%g',1); fscanf(fid,'%s',1);
T = fscanf(fid,'%g',nrows*ncols);
fclose(fid);

ax = xll;
ay = yll;
bx = ax + dx*ncols
by = ay + dx*nrows

x = linspace(ax,bx,ncols);
y = linspace(ay,by,nrows);

NT(1:nrows,1:ncols) = 0;

for m = 1:nrows;
    for n = ncols:-1:1;
                NT(m,n) = T((m-1)*ncols + n); 
    end
end

%NT = reshape(T,[ncols,nrows]);

[xm,ym] = meshgrid(x,y);

tf = strcmp(fname, 'tetontopo');
p = surf(x,y,NT);

%if tf
 %   set(p,'facecolor','red');
  %  set(p,'edgecolor','red');
%else
set(p,'facecolor',c);
set(p,'edgecolor','none');
%end

%set(p,'facecolor',c);
%set(p,'edgecolor','none');

bigxll = -111.960983;
bigyll = 43.794393;
smallxll = -111.684952;
smallyll = 43.889109;
distx = smallxll  - bigxll;
disty = smallyll - bigyll;

bignorthdx = 0.0012458729166666535;
bignorthdy = 0.0008993236659597745;
lowresdx = 0.0006229441195123567;
lowresdy = 0.00044966183297988723;
tetontopodx = 0.0003743605139906295;
tetondopody = 0.0002697985826184408;

rows = (distx/lowresdx)*100;
cols = (disty/lowresdy)*100;

end