# VibrationMatlabCode

> **Navigation:** [Home](../Beauchamp/index.md) | [Publications](../Beauchamp/Publications.md) | [Resources](../Beauchamp/DataSharing.md)

```
% MATLAB code for finding best fit. As before, you could probably find a more elegant way to do this.  Or, you could copy and 
paste and move on with your day. ;-)
```

```
% R = ratio to fit
% X_grad = G(:,1); 
% G=scaled gradients, column-wise X Y Z 

a_ind=0;
b_ind=0;

if mean(R(abs(X_grad)>800)) > mean(R(abs(X_grad)<300))+std(R(abs(X_grad)<300))
   t_flip=1;
else
   t_flip=0;
end

clear err_ss
for a= 0:.001:1  %.  <--- I found this to be pretty quick, but you can 
                 % nonetheless start wide with a range of something like
                 % 0:.1:1 and focus in after a few runs. 

   a_ind=a_ind+1;
   a_keep(a_ind) = a;
   b_ind=0;
   
   for b=0:.01:15  % <--- same.
       b_ind=b_ind+1;
       b_keep(b_ind) = b;

       for ind=1:length(R);
           if abs(X_grad(ind)) < 1000*a
               t(ind)= 1;
           elseif abs(X_grad(ind)) <= 1000*(a+b);
               t(ind)=  cos(((abs(X_grad(ind)/1000)-a)*pi)/(2*b))^2; 
           else
               t(ind)=0;
           end
       end
       
       if t_flip==1;
           t=2-t;
       end
             
       err_ss(a_ind,b_ind)=sum(sqrt((R-t').^2));
       
   end
end
     
close all

% imagesc(1-err_ss);
[i,j]=find(err_ss ==min(min(err_ss))); 

a=a_keep(i);
b=b_keep(j);

% disp(['a=' num2str(a_keep(i))])
% disp(['b=' num2str(b_keep(j))])

a=a_keep(i); b=b_keep(j);
for ind=1:length(R);
   if abs(X_grad(ind)) < 1000*a
       t(ind)= 1;
   elseif abs(X_grad(ind)) <= 1000*(a+b);
       t(ind)=  cos(((abs(X_grad(ind)/1000)-a)*pi)/(2*b))^2; 
   else
       t(ind)=0;
   end
end

if t_flip==1;
   t=2-t;
end


       
%  figure; 
%  g_nice=sortrows([X_grad, t']);
%  plot(X_grad, R, 'o'); 
%  hold on
%  plot(g_nice(:,1), g_nice(:,2), '--')

%  fid=fopen('tukey_correction.txt', 'w');
%  
%  % print out tukey correction values, add in b=0 volumes.  We're going to
%  % apply this to the DMC-corrected DWI.nii 
% 
clear tukey_correction
b0=[1 11 21 31 41 51 61 71];
t_ind=1;
for full_ind=1:79;
   if max(full_ind==b0)==1
       fprintf(fid, '1\n');
%      tukey_correction(full_ind)=1;
   else
       fprintf(fid, '%.4f\n', t(t_ind));
%      tukey_correction(full_ind) = t(t_ind);
       t_ind=t_ind+1;
   end
end
```
