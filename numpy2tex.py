import numpy as np

def numpy2tex(array,
              filename = '',
              caption = '',
              label = '',
              columns = '',
              columnTitles = [],
              rowTitles = [],
              upperLeft = ''):
    m, n = array.shape
    cTitles = False
    if columnTitles:
        array = np.append(np.array(columnTitles)[np.newaxis, :], array, axis = 0)
        cTitles = True
    if rowTitles:
        if cTitles:
            rowTitles = np.append([upperLeft], rowTitles)[:, np.newaxis]
        array = np.append(rowTitles, array, axis = 1)
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
    if filename:
        with open(filename, 'w') as f:
            f.write(texString)
    else:
        return texString
    
    
if __name__ == "__main__":
    arr = np.zeros((3,3))
    filename = ""
    print numpy2tex(arr, filename, columnTitles = ['c1', 'c2', 'c3'],
                    rowTitles = ['r1', 'r2', 'r3'], upperLeft = 'ul',
                    caption = "blablacaption", label = "label1",
                    columns = '|c|c|c|c|')
