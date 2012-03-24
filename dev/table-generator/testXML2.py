from xml.dom import minidom
scl = minidom.parse("DataTypeTemplates.xml")

lNodeTypes = scl.getElementsByTagName("LNodeType")
doTypes = scl.getElementsByTagName("DOType")
lNodeTypeList = []
latexScript_list = ""
desc = lNodeType.attributes["id"]
for lNodeType in lNodeTypes:
    lnClass = lNodeType.attributes["lnClass"]
    id = lNodeType.attributes["id"]
    try:
        desc = lNodeType.attributes["desc"]
    except (NameError, KeyError):
        desc.value = " "    
    lNodeTypeList.append( "%s = %s" % (lnClass.value, desc.value) )
    print lNodeTypeList[-1]
    name = id.value + ".tex"
    outp = open(name,"w")
    latexScript_list =  latexScript_list + "\input{" + id.value + "} \n  \n  \n"
    latexScript =  """
\\begin{center}    
\\begin{tabular}{|l|l|p{7.5cm}|}
	\hline
	\multicolumn{3}{|c|}{\cellcolor[gray]{0.8} \\textbf{%s}  - %s} \\\\
    	\hline
    	\\textbf{Attribute Name} & \\textbf{Attr. Type} & \\textbf{Explanation} \\\\
    	\hline """  % (lnClass.value, desc.value)

    
    do_latexScript = ""
    dos = lNodeType.getElementsByTagName("DO")
    for do in dos:
        do_Name = do.attributes["name"]
        do_type = do.attributes["type"]
        do_cdcType = "-"
        doType_desc = "-"
        for doType in doTypes:
            doType_id = doType.attributes["id"]
            if (doType_id.value == do_type.value ):
                do_cdcType = doType.attributes["cdc"].value
                try:
                    doType_desc = doType.attributes["desc"].value
                except (NameError, KeyError):
                    doType_desc = " "    
                """doType_desc = doType.attributes["desc"].value"""
                """print do_cdcType"""
        do_latexScript = """
        %s & %s & %s \\\\
        \hline""" % (do_Name.value, do_cdcType, doType_desc)
        latexScript = latexScript + do_latexScript 
    latexScript = latexScript + """
\end{tabular}
\end{center}"""

    outp.write(latexScript)
    outp.close()


outList = open("main_LNodeTypes.tex","w")
outList.write(latexScript_list)
outList.close()

outMain = open("main.tex", "w")
outMain.write("""
\documentclass{article}
\usepackage{multirow}
\usepackage[table]{xcolor}
\\begin{document}
\section{DataTypeTemplate}
\input{main_LNodeTypes}
\end{document}
""")
outMain.close()
outMain.close()
