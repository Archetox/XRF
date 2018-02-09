clear
% Importing relevant data files
normfilename = 'currentminiion.txt';            % set to correct mini ion name (different for CLS and NSLS data

element = input('Enter element of interest (atomic symbol):','s');
e = upper(element);

% Assigning atomic symbols to correct data files (must be all-caps)
if e == 'AR' 
    datafile = importdata('detsum_Ar_K.txt');
elseif e == 'AS' 
    datafile = importdata('detsum_As_K.txt');
elseif e == 'CA' 
    datafile = importdata('detsum_Ca_K.txt');
elseif e == 'CL' 
    datafile = importdata('detsum_Cl_K.txt');
%elseif e == 'COMPTON' 
%    datafile = importdata('detsum_compton.txt');
elseif e == 'CR' 
    datafile = importdata('detsum_Cr_K.txt');
%elseif e == 'ELASTIC' 
%    datafile = importdata('detsum_elastic.txt');
elseif e == 'FE'
    datafile = importdata('detsum_Fe_K.txt');
elseif e == 'NI'
    datafile = importdata('detsum_Ni_K.txt');
elseif e == 'P'
    datafile = importdata('detsum_P_K.txt');
elseif e == 'S'
    datafile = importdata('detsum_S_K.txt');
elseif e == 'SI'
    datafile = importdata('detsum_Si_K.txt');
elseif e == 'W'
    datafile = importdata('detsum_W_L.txt');
elseif e == 'ZN'
    datafile = importdata('detsum_Zn_K.txt');
else
    disp("Cannot determine element type! Edit script to ensure element file is assigned!")
    return
end

normfile = importdata(normfilename);
normdata = datafile ./ normfile;

% Determining x and y steps from matrix datafiles
xpos = importdata('x_pos.txt');
ypos = importdata('y_pos.txt');
xposmean = mean(xpos,1);                        % determines mean value in each column (indicated by "1")
x = transpose(xposmean);                        % transposes mean values in colums to row format
y = mean(ypos,2);                               % determines mean value in each row (indicated by "2")

% Histogram analysis
binnum = input('Enter number of bins you want for the histogram analysis:');
[N,edges]=histcounts(normdata(:),binnum,'Normalization','probability');
histodata = horzcat(transpose(edges(:,1:end-1)),N(:));
histosum = cumsum(histodata(:,2));
histosum = histosum*100;
histodata = horzcat(histodata,histosum);

clear element xpos ypos normfile normfilename xposmean datafile N edges binnum histosum
