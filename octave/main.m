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
        fprintf("\n\n[OUTPUT] START");
        fprintf("\n[OUTPUT] MATRIX: ");
        fprintf(filename);
        fprintf('\n');

        spparms('spumoni', 2);
        
        tic;
        x = my_solve(A,b);
        tempo = toc;

        erel = norm(x-xe) / norm(xe);

        fprintf('[OUTPUT] TIME: %e\n', tempo);
        fprintf('[OUTPUT] EREL: %e\n', erel);
        fprintf('[OUTPUT] NNZ: %e\n', entries);

        fprintf("\n[OUTPUT] END\n\n");
        
        catch exception
            disp("Error:")
            disp(exception.message);
    end
end
quit;
