listing = dir('../matrixes');

for file_index = 3:length(listing)
    filename = strcat('../matrixes/', listing(file_index).name);
    disp(strcat("import ", filename));
    [A, rows, cols, entries] = mmread(filename);
    disp(strcat("run ", filename));
    sizeA = size(A,1);
    xe = ones(sizeA,1);
    b = A*xe;

    try 
        diary on
        fprintf(1, filename)
        fprintf(1, '\n')
        spparms('spumoni', 2);
        
        tic;
        x = my_solve(A,b);
        
        tempo = toc;
        
        erel = norm(x-xe) / norm(xe);

        fprintf('out-time: %e\n', tempo);
        fprintf('out-erel: %e\n', erel);

        diary off
        
       
        catch exception
            disp(exception.message);
    end
end
