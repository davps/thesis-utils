from xml.dom import minidom
scl = minidom.parse("DataTypeTemplates.xml")
lNodeTypes = scl.getElementsByTagName("LNodeType")
for lNodeType in lNodeTypes:
    lnClass = lNodeType.attributes["lnClass"]
    id = lNodeType.attributes["id"]
    try:
        desc = lNodeType.attributes["desc"]
    except (NameError, KeyError):
        desc.value = " "    
    lNodeTypeList = "%s = %s" % (lnClass.value, desc.value)
    print lNodeTypeList
    name = id.value + ".tex"
    outp = open(name,"w")
    latexScript =  """
\\begin{tabular}{|l|l|p{5cm}|}
	\hline
	\multicolumn{3}{|c|}{\cellcolor[gray]{0.8} \\textbf{%s}  - %s} \\\\
    	\hline
    	Attribute Name & Attr. Type & Explanation \\\\ \hline
        \multirow{4}{*}{Defenders} & Pos & INC \\\\
         & DC & Michael Duberry \\\\
         & DC & Dominic Matteo \\\\
         & RB & Didier Domi \\\\ \hline
        \multirow{3}{*}{Midfielders} & MC & David Batty \\\\
         & MC & Eirik Bakke \\\\
         & MC & Jody Morris \\\\ \hline
        Forward & FW & Jamie McMaster \\\\ \hline
        \multirow{2}{*}{Strikers} & ST & Alan Smith \\\\
         & ST & Mark Viduka \\\\
        \hline
    \end{tabular}


    """ % (lnClass.value, desc.value)
    
    outp.write(latexScript)
    outp.close()

