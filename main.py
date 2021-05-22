import os
import csv
import sys

def spumoni_to_csv(lang = 'matlab', command = 'touch exec.sh'):
    ## Function to parse spumoni

    # Generate out file
    filename = 'diary'
    out = os.path.join('./' + lang, filename)

    # Command to exec
    if lang == 'matlab':
        command = 'cd ' + lang + ';' + command + ' > /dev/null 2> /dev/null' + ';cd ..;'
    elif lang == 'octave':
        command = 'cd ' + lang + ';' + command + ' > diary 2>&1' + ';cd ..;'


    # Remove old not-removed out
    try:
        os.remove(out)
    except:
        pass

    # Execute the program 
    os.system(command)

    # Read the result file
    with open(out) as f:
        content = f.readlines()

    # Init 
    data = []
    index = 0
    # Grep useful content line by line.
    for line in content:

        # Start
        if "[OUTPUT] START" in line:

            # Init 
            filename = 'unknown'
            is_cholesky = 'unknown'
            memory = 'unknown'
            erel = 'unknown'
            nnz = 'unknown'
            size = 'unknown'

        # Get size
        if "[OUTPUT] MATRIX" in line:
            templist = line.split(':')
            templist = [item for item in templist if item != '']
            templist = templist[len(templist)-1].split('/')
            templist = [item for item in templist if item != '']
            filename = templist[len(templist)-1].strip()
        # Get size
        if "number rows and columns" in line:
            templist = line.split('  ')
            templist = [item for item in templist if item != '']
            size = templist[1].strip()
        # Get if isCholesky
        if "candidate for Cholesky" in line:
            if "yes." in line:
                is_cholesky = True
            elif "no." in line:
                is_cholesky = False
        # Get memory
        if "peak memory usage (M" in line:
            templist = line.split('  ')
            templist = [item for item in templist if item != '']
            memory = templist[1].strip()
        # Get time
        if "[OUTPUT] TIME" in line:
            templist = line.split(':')
            time = templist[1].strip()
        # Get erel
        if "[OUTPUT] EREL" in line:
            templist = line.split(':')
            erel = templist[1].strip()
        # Get NNZ
        if "[OUTPUT] NNZ" in line:
            templist = line.split(':')
            nnz = templist[1].strip()
        # Save on end
        if "[OUTPUT] END" in line:
            data_row = []
            # Save data row
            data_row.append(filename)
            data_row.append(nnz)
            data_row.append(time)
            data_row.append(memory)
            data_row.append(erel)
            data_row.append(is_cholesky)
            # and append it to data
            data.append(data_row)

    # Save to CSV
    with open('./reports/' + lang + '.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        # Set csv header 
        writer.writerow(["Matrix", "NNZ", "Time", "Memory", "RelError", "isCholesky"])
        # Save data
        for i in range(0, len(data)):
            writer.writerow(data[i])

    # Delete the log file
    try:
        # Fede ❤️ Data Persistence
        # os.remove(out)
        pass
    except:
        pass


# Exec MATLAB
print('Running MATLAB...')
spumoni_to_csv('matlab', 'matlab -nodisplay -nojvm -nosplash -nodesktop -r "run(\'main.m\'); exit;"')
# Exec OCTAVE
print('Running OCTAVE...')
spumoni_to_csv('octave', 'octave --no-gui --eval "run(\'main.m\'); exit;"')
# Exec PYTHON
print('Running PYTHON...')
if sys.platform == "linux" or sys.platform == "linux2":
    # Linux
    os.system('cd python; python3 main_linux.py > /dev/null;cd ..')
elif sys.platform == "win32":
    # Windows
    os.system('cd python; python3 main_win.py > /dev/null;cd ..')
elif sys.platform == "darwin":
    # OS X
    # Ehm... do nothing
    pass
print('E vissero felici e contenti.')