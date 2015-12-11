function [  ] = TetonDamDischarge( ng )
%UNTITLED2 Summary of this function goes here
% This function will plot the outflow of the teton dam in 
% cubic feet per second vs. time in hours. The outflow is calculated
% using a simplified form of the continuity equation, Q=A*u, where A is
% the A is the cross-sectional area of the portion of the channel occupied
% by the flow (units^2), U is the averate flow velocity (units/s) and Q is
% the discharge (units^3/s). 

% Calculate A 
% Note: at 43.910597 degrees latitude, one degree of longitude is
% 80326.50282681343 meters or 263537.8679975282 feet. 

west_edge = -111.542215;
east_edge = -111.539842;
length = abs(east_edge - west_edge)*80326.50282681343; %convert to meters;
partition = length / ng;
yvelocity = importdata('yvelocity.txt','%g',0);
height = importdata('height.txt','%g',0);

[c,~] = size(height)
time_steps = c/ng
Q = zeros(1,time_steps*ng);
QT = zeros(1,time_steps);
A = zeros(1,round(c/ng));

%Find the cross-sectional area by integrating using Simpson's Rule. 
%(b-a)/6*(f(a) +4*f((a+b)/2)+f(b)), where b-a = length
%for i = 1:ng:c
 %   A(i) = (length/6)*(height(i+1)+4*height(round((i+1+ng)/2))+height(ng));
%end
    

%Find the mean velocity

%We only use the y-velocity here since the x-velocity is parallel to
%the boundary we are considering
for j = 1:time_steps;
    for k = 1:ng;
        %Find the flux for each area and convert to feet. 
        Q(k+ng*(j-1)) = -1*partition*height(k+(j-1)*ng)*yvelocity(k+(j-1)*ng)*(3.28084)^3; 
        %Rectangle rule
        %QT(j) = QT(j)+Q(k+(j-1)*6);
    end
    %Simpson's rule is a method of numerical integration. The equation for 
    %Simpson's rule is (b-a)/6*(f(a) +4*f((a+b)/2)+f(b)) 
    %using Simpson's rule (more accurate):
    QT(j) = (length/6)*(Q((j-1)*ng+1)+4*Q(round(((j-1)*ng+1+(j-1)*ng+ng)/2))+Q((j-1)*ng+ng));
    
    %The Trapezoidal Rule is another method of numerical integration. The
    %equation for the Trapezoidal rule is (b-a)*[(f(a)+f(b))/2]. Using the
    %Trapezoidal Rule:
    %QT(j) = length*[(Q((j-1)*ng+1)+Q((j-1)*ng+ng))/2];
end 



%Calculate total discharge
[peak,index] = max(QT);
%Simpson's rule on the lower half
lower_area = ((index-0)/6)*(QT(1) +4*QT(round(index/2))+QT(index))
upper_area = ((time_steps - index)/6)*(QT(index) +4*QT(round((index+time_steps)/2))+QT(time_steps))
p = lower_area + upper_area


[~,b] = size(QT)
%b/120
%floor(b/120)
%if b > 240
 %   QTH = zeros(1,floor(b/120));
  %  for k = 1:floor(b/120);
   %     QTH(k) = QT(k*120);
    %end
    %t = 1:floor(b/120);
    %label = 'Time In Hours';
%if b > 60
 %   QTH = zeros(1,floor(b/60));
  %   for j = 1:floor(b/60);
   %     QTH(j) = QT(j*60);
    % end
    %t = 1:floor(b/60);
    %label = 'Time In Minutes';
%else
   % QTH = zeros(1,b);
    %QTH = QT;
    %t = 1:b;
    %label = 'Time In Seconds';
%end

%Plot the actual

t=1:time_steps;  
label = 'Time In Seconds';

clf

img = imread('TetonDam--Predicted and observed breach outflow hydrograph and breach properties..PNG');
imagesc([1:18000],[1:peak],flipud(img)); 
hold on

plot(t,QT,'b-','linewidth',1.5);

set(gca, 'ydir', 'normal');

legend('Cubic Feet Per Second');
title('Hydrograph of GeoClaw Simulation of Teton Dam');
xlabel(label);
ylabel('Cubic Feet Per Second (CFS)');
%annotation('textbox', [0.2 0.5 0.3 0.3],'String',sprintf('%s%f\n%s%f',' Total Discharge: ',p, ' Peak Discharge: ',peak))


end

