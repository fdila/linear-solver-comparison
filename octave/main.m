listing = dir('../matrixes');

csv_file = fopen('../reports/octave.csv','w');
C={'Matrix', 'Size', 'Time' ,'Memory','RelError'};
fprintf(csv_file,'%s,%s,%s,%s,%s\n',C{:});
formatSpec = '%s,%d,%f,%f,%e\n';

for file_index = 3:length(listing)
    filename = strcat('../matrixes/', listing(file_index).name);
    
    disp(strcat("import ", filename));
    [A, rows, cols, entries] = mmread(filename);
    
    disp(strcat("run ", filename));
    sizeA = size(A,1);
    xe = ones(sizeA,1);
    b = A*xe;

    try 
        spparms('spumoni', 2);
        
        tic;
        x = my_solve(A,b);
        tempo = toc;

        erel = norm(x-xe) / norm(xe);
        
        C={listing(file_index).name, sizeA, tempo, 0, erel};
        fprintf(csv_file,formatSpec,C{:});
        
        catch exception
            disp(exception.message);
    end
end
fclose(csv_file);
%quit;
