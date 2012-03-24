"""-------------------------------------------------
		Este programa analiza una colección
		de ICDs y resume información relevante
-------------------------------------------------"""



import glob

"""-------------------------------------------------
                  Lista de ficheros ICD
-------------------------------------------------"""
rootDirname = "D:\\Phyton61850\\ICD\\ICD_files\\"
moreDir = "*\\\\"
dirName = rootDirname + moreDir

icds = []
for i in range(5):
    dirName
    tempIcds = glob.glob(dirName + "*.icd")
    tempIcds
    icds.extend(tempIcds)
    dirName += moreDir
print icds
print len(icds)



"""
    Servicios soportados por los ICDs analizados
"""

from xml.dom import minidom
allServices = {}
allLNs = {}
for icd in icds:
    scl = minidom.parse(icd)
    services = scl.getElementsByTagName("Services")[0]
    lns = scl.getElementsByTagName("LN")
    for ln in lns:
        if(ln.localName):
            try:
                allLNs[ ln.getAttribute("lnClass") ] += 1
            except:
                allLNs[ ln.getAttribute("lnClass") ] = 1
    
    for service in services.childNodes:
        if(service.localName):
            try:
                allServices[service.localName] += 1
            except (KeyError):
                allServices[service.localName] = 1
            """print service.localName"""
    """print allServices.items()"""

sum = 0
for key in allLNs.values():
    sum = sum + key
print "Total de LNs"
print sum

texScript1 =  """
\\begin{center}    
\\begin{tabular}{|l|l|}
    \hline
    \multicolumn{2}{|c|}{\cellcolor[gray]{0.8} \\textbf{IED - Servicios implementados en el mercado}  } \\\\
        \hline
        \\textbf{Servicio ACSI} & \\textbf{Cantidad de IEDs que lo implementan} \\\\
        \hline """
servicesLatexScript = ""
for (k, v) in allServices.items():
    servicesLatexScript = servicesLatexScript + """
        %s & %s \\\\
        \hline""" % (k, v)

texScript1 = texScript1 + servicesLatexScript + """
\end{tabular}
\end{center}"""


texScript2 =  """
\\begin{center}    
\\begin{tabular}{|l|l|}
    \hline
    \multicolumn{2}{|c|}{\cellcolor[gray]{0.8} \\textbf{IED - Servicios implementados }  } \\\\
        \hline
        \\textbf{Servicio ACSI} & \\textbf{Cantidad de IEDs que lo implementan} \\\\
        \hline """
lnsLatexScript = ""
for (kLN, vLN) in allLNs.items():
    lnsLatexScript = lnsLatexScript + """
        %s & %s \\\\
        \hline""" % (kLN, vLN)

texScript2 = texScript2 + lnsLatexScript  + """
\end{tabular}
\end{center}"""


latexScript = texScript1 + texScript2


outList = open("servicesTable.tex","w")
outList.write(latexScript)
outList.close()

    
