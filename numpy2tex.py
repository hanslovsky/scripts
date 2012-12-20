# written by Philipp Hanslovsky

import numpy as np

def numpy2tex(array,
              filename = '',
              caption = '',
              label = '',
              columns = '',
              columnTitles = [],
              rowTitles = [],
              upperLeft = '',
              dataType = '|S100'):
    """convert numpy 2D array to tex table
    If filename is specified, the tex table will be written to that file; otherwise the string is returned."""

    # convert any 2D iterable to np.array. Array content needs to be convertable to string
    array = np.array(array, dtype=dataType)
    if len(array.shape) != 2:
        print "Works only for 2D Arrays. If you want to print an array of iterables (such as array of tuples)" + \
            " to table, please convert it to an array of strings first."
        raise Exception()
    m, n = array.shape
    # todo: if array is 3D (e.g. when input array is 2D array of tuples), convert third dimension to
    # string and reshape to 2D
    # add titles for Columns, Rows and upper left cell, if given/neccessary
    cTitles = False
    if columnTitles:
        array = np.append(np.array(columnTitles)[np.newaxis, :], array, axis = 0)
        cTitles = True
    if rowTitles:
        if cTitles:
            rowTitles = np.append([upperLeft], rowTitles)[:, np.newaxis]
        columns = '|c' + columns
        array = np.append(rowTitles, array, axis = 1)

    # convert to tex string
    texString = \
        "\\begin{table}[h!]\n" + \
        "\\centering\n" + \
        "\\begin{tabular}{" + columns + "}\n\\hline\n"
    for line in array:
        for el in line[:-1]:
            texString += str(el) + " & "
        texString += str(line[-1]) + " \\\\\\hline\n"
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
    arr = np.zeros((3,3))+1.0/3.0
    filename = ""
    print numpy2tex(arr, filename, columnTitles = ['c1', 'c2', 'c3'],
                    rowTitles = ['r1', 'r2', 'r3'], upperLeft = 'ul',
                    caption = "blablacaption", label = "label1",
                    columns = '|c|c|c|c|', dataType = '|S5')
    
