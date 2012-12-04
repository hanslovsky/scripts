# written by Philipp Hanslovsky

import numpy as np

def numpy2tex(array,
              filename = '',
              caption = '',
              label = '',
              columns = '',
              columnTitles = [],
              rowTitles = [],
              upperLeft = ''):
    """convert numpy 2D array to tex table
    If filename is specified, the tex table will be written to that file; otherwise the string is returned."""

    # convert any 2D iterable to np.array
    array = np.array(array)
    m, n = array.shape
    # add titles for Columns, Rows and upper left cell, if given/neccessary
    cTitles = False
    if columnTitles:
        array = np.append(np.array(columnTitles)[np.newaxis, :], array, axis = 0)
        cTitles = True
    if rowTitles:
        if cTitles:
            rowTitles = np.append([upperLeft], rowTitles)[:, np.newaxis]
        array = np.append(rowTitles, array, axis = 1)

    # convert to tex string
    texString = \
        "\\begin{table}[h!]\n" + \
        "\\centering\n" + \
        "\\begin{tabular}{" + columns + "}\n\\hline\n"
    for line in array:
        for el in line[:-1]:
            texString += el + " & "
        texString += line[-1] + " \\\\\\hline\n"
    texString += \
        "\\end{tabular}\n" + \
        "\\caption{" + caption + "}\n" + \
        "\\label{tab:" + label + "}\n" + \
        "\\end{table}"
    # write to file if specified and return string
    if filename:
        with open(filename, 'w') as f:
            f.write(texString)
    return texString
    
    
if __name__ == "__main__":
    arr = np.zeros((3,3))
    filename = ""
    print numpy2tex(arr, filename, columnTitles = ['c1', 'c2', 'c3'],
                    rowTitles = ['r1', 'r2', 'r3'], upperLeft = 'ul',
                    caption = "blablacaption", label = "label1",
                    columns = '|c|c|c|c|')
