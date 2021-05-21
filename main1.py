import os
import csv

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

    # Init data
    data = []
    for filename in os.listdir('./matrixes/'):
        if filename.endswith(".mtx"):
            data_row = []
            data_row.append(filename)
            data.append(data_row)

    # Init 
    is_cholesky = 'unknown'
    memory = 'unknown'
    erel = 'unknown'
    size = 'unknown'

    index = 0
    # Grep useful content line by line.
    for line in content:
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
        if "out-time:" in line:
            templist = line.split(':')
            time = templist[1].strip()
        # Get erel
        if "out-erel:" in line:
            templist = line.split(':')
            erel = templist[1].strip()
            # Then...
            # Save data
            data[index].append(size)
            data[index].append(time)
            data[index].append(memory)
            data[index].append(erel)
            data[index].append(is_cholesky)
            is_cholesky = 'unknown'
            memory = 'unknown'
            erel = 'unknown'
            size = 'unknown'
            # Last useful info for this item
            index = index + 1

    print(data)

    # Save to CSV
    with open('./reports/' + lang + '.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        # Set csv header 
        writer.writerow(["Matrix", "Size", "Time", "Memory", "RelError", "isCholesky"])
        # Save data
        for i in range(0, len(data)):
            writer.writerow(data[i])


    # Delete the log file
    try:
        # TODO io nel dubbio li terrei fino alla run successiva
        #os.remove(out)
        pass
    except:
        pass




# Exec
#spumoni_to_csv('matlab', 'matlab -nodisplay -nojvm -nosplash -nodesktop -r "run(\'main.m\'); exit;"')
spumoni_to_csv('octave', 'octave --no-gui --eval "run(\'main.m\'); exit;"')
##TODO eseguiamo qui anche il codice py?
