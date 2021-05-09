listing = dir('../matrixes');

csv_file = fopen('../reports/matlab.csv','w');
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
        profile clear;
        profile('-memory','on');
        setpref('profiler','showJitLines',1);
        
        spparms('spumoni', 2);
        x = my_solve(A,b);

        erel = norm(x-xe) / norm(xe);

        profilerInfo = profile('info');

        functionNames = {profilerInfo.FunctionTable.FunctionName};
        functionRow = find(strcmp(functionNames(:), 'my_solve'));

        t = profilerInfo.FunctionTable(functionRow).TotalTime; 
        %convert from kb to MB
        mem = (profilerInfo.FunctionTable(functionRow).PeakMem)/8000; 
        
        C={listing(file_index).name, sizeA, t, mem, erel};
        fprintf(csv_file,formatSpec,C{:});
        
        catch exception
            disp(exception.message);
            res = [listing(file_index).name sizeA "N/A" "N/A" "N/A"];
    end
end
fclose(csv_file);