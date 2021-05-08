filename = '../matrixes/G3_circuit.mtx';
[A, rows, cols, entries] = mmread(filename);
disp(strcat("run ", filename));
sizeA = size(A,1);
xe = ones(sizeA,1);
b = A*xe;

try
    profile clear;
    profile('-memory','on');
    setpref('profiler','showJitLines',1);
    
    x = A\b;

    erel = norm(x-xe) / norm(xe);
            
    profilerInfo = profile('info');
            
    functionNames = {profilerInfo.FunctionTable.FunctionName};
    functionRow = find(strcmp(functionNames(:), 'main'));

    t = profilerInfo.FunctionTable(functionRow).TotalTime; 
    mem = profilerInfo.FunctionTable(functionRow).TotalMemAllocated; 
            
    res = [filename sizeA t mem erel];
    catch exception
        disp(exception.message);
        res = [filename sizeA "N/A" "N/A" "N/A"];
end