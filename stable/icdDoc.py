# -*- coding: cp1252 -*-
from xml.dom import minidom
import glob
import re

scl = minidom.parse("c:\\python-61850\\thesis\\ICDs\\IED_RV.xml") #1 - iedE
##scl = minidom.parse("c:\\python-61850\\thesis\\ICDs\\IED_MAIN_TNK.xml") #2 - iedA
##scl = minidom.parse("c:\\python-61850\\thesis\\ICDs\\IED_air-oil_PRS_TNK.xml") #3 - iedB
##scl = minidom.parse("c:\\python-61850\\thesis\\ICDs\\IED_compressed_air_plant.xml") #4 - iedC
##scl = minidom.parse("c:\\python-61850\\thesis\\ICDs\\IED_rot_sensor.xml") #5 - iedD

##scl = minidom.parse("SEL2411.ICD")
##scl = minidom.parse("j:\\MRV\\DataTypeTemplates.xml")

integrado_a_mi_tesis= True
pathThesis = ""
if integrado_a_mi_tesis:
    pathThesis = "chapters/model/iedE/"


"""El elemento LN es del tag IED"""
lNs = scl.getElementsByTagName("LN")
iedSCL = scl.getElementsByTagName("IED")
iedName = iedSCL[0].attributes["name"].value



def lNodeTypeFromSCLdocumentator(params):
    lNodeTypes = scl.getElementsByTagName("LNodeType")
    doTypes = scl.getElementsByTagName("DOType")
    lNodeTypeList = []
    latexScript_list = ""
    desc = ""
    for lNodeType in lNodeTypes:
        lnClass = lNodeType.attributes["lnClass"]
        id = lNodeType.attributes["id"]
        try:
            auxValue = lNodeType.attributes["desc"]
            desc = auxValue.value
        except (NameError, KeyError):
            desc = " "
        lNodeTypeList.append( "%s = %s" % (lnClass.value, desc) )
        referenciaTablaLnInst = "table:lnInst%s" % id.value
        referenciaTablaLNType = "table:lnType%s" % id.value
        latexScriptIED_LNs = """
\\subsection{Nodo l\\'ogico: \t\t\t %s}
""" % (lnClass.value)
        
        """el tabular inicial era de 4.7cm, con eso encaja perfecto para un doc independiente"""
        latexScriptIED_LNs +=  """
    \subsubsection{Instancias del nodo l\\'ogico %s}
    \\begin{table}[H]
    \\begin{center}
    \\begin{tabular}{|l|l|p{6.8cm}|}
            \hline
            \multicolumn{3}{|c|}{\cellcolor[gray]{0.8} \\textbf{IED Logical Nodes} } \\\\
            \hline
            \\textbf{LN Name} & \\textbf{Logical Device Allocation} & \\textbf{Code and description} \\\\
            \hline""" % (lnClass.value)
        latexScriptIED_LNsrc = ""
        for ln in lNs:
            try:
                if(ln.attributes["lnType"].value == id.value):
                    latexScriptIED_LNsrc = latexScriptIED_LNsrc + ln.toxml() + "\n" 
                    auxLN1 = ln.attributes["prefix"].value.replace("_", "\\_") + ln.attributes["lnClass"].value + ln.attributes["inst"].value
                    latexScriptIED_LNs += """
            %s & %s & %s \\\\
            \hline""" % (auxLN1, ln.parentNode.attributes["ldName"].value, ln.attributes["desc"].value)
            except:
                latexScriptIED_LNs
        outLNName = "ied%s.xml" % id.value
        outLNType = open(outLNName,"w")
        outLNType.write(latexScriptIED_LNsrc) 
        outLNType.close()
        latexScriptIEDSrc = """
    \lstinputlisting[label=code:sclied%s,
            caption=Instancias %s representadas en SCL
            ]{%s%s}
    """ % (lnClass.value, lnClass.value, pathThesis, outLNName)

        
        latexScriptIED_LNs += """
    \end{tabular}
    \caption{Instancias %s en el IED %s}
    \label{%s}
    \end{center}
    \end{table}
    """ % (lnClass.value, iedName, referenciaTablaLnInst) + latexScriptIEDSrc
###        print lNodeTypeList[-1]
        name = id.value + ".tex"
        outp = open(name,"w")
        if not (lnClass.value == "LLN0"):
            latexScript_list =  latexScript_list + "\input{" + pathThesis + id.value + "} \n  \n  \n"
        
        """el tabular inicial era de 6.2cm, con eso encaja perfecto para un doc independiente"""
        latexScript =  """
    \subsubsection{DataTypeTemplate}
    \\begin{table}[H]
    \\begin{center}
    \\begin{tabular}{|l|l|p{8.5cm}|}
            \hline
            \multicolumn{3}{|c|}{\cellcolor[gray]{0.8} \\textbf{ %s}  - %s} \\\\
            \hline
            \\textbf{Attribute Name} & \\textbf{Attr. Type} & \\textbf{Explanation} \\\\
            \hline """  % (lnClass.value, desc)

        outLNTypeName = "%s.xml" % lnClass.value
        outLNType = open(outLNTypeName,"w")
        outLNType.write(lNodeType.toxml())
        outLNType.close()
        latexScriptSrc = """
    \lstinputlisting[label=code:scl%s,
            caption=%s - %s - Representaci\\'on en SCL
            ]{%s%s}
    """ % (lnClass.value, lnClass.value, desc, pathThesis, outLNTypeName)
            
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
    \caption{Plantilla %s del IED %s}
    \label{%s}
    \end{center}
    \end{table}
    """ % (lnClass.value, iedName, referenciaTablaLNType) + latexScriptSrc
        finalScript = latexScriptIED_LNs + latexScript

        outp.write(finalScript)
        outp.close()

    """
        with open("hello2.txt") as f:
            for line in f:
                print line % ("aaaaaaaaaa", "bbbbbbbbbbbbbbb")
    """

    """
    lNodeType = lNodeTypes[0]
    a =  lNodeType.attributes["lnClass"]
    print a.name
    print a.value
    """

    outList = open("main_LNodeTypes.tex","w")
    outList.write(latexScript_list)
    outList.close()

    outMain = open("main.tex", "w")
    outMain.write("""
    \documentclass{article}
    \usepackage{multirow}


    \usepackage{listings}
    \usepackage{courier}
    \lstset{
             basicstyle=\\footnotesize\\ttfamily,
             numberstyle=\\tiny,
             numbersep=5pt,
             tabsize=2,
             extendedchars=true,
             breaklines=true,
             keywordstyle=\color{red},
                    frame=b,         
             stringstyle=\color{white}\\ttfamily,
             showspaces=false,
             showtabs=false,
             xleftmargin=17pt,
             framexleftmargin=17pt,
             framexrightmargin=5pt,
             framexbottommargin=4pt,
             showstringspaces=false
     }
    \lstloadlanguages{XML, Java}
    \usepackage{caption}
    \DeclareCaptionFont{white}{\color{white}}
    \DeclareCaptionFormat{listing}{\colorbox[cmyk]{0.43, 0.35, 0.35,0.01}{\parbox{\textwidth}{\hspace{15pt}#1#2#3}}}
    \captionsetup[lstlisting]{format=listing,labelfont=white,textfont=white, singlelinecheck=false, margin=0pt, font={bf,footnotesize}}



    \usepackage[table]{xcolor}
    \\begin{document}
    \section{Nodos l\\'ogicos del IED}
    \input{main_LNodeTypes}
    \end{document}
    """ ) 
    outMain.close()
    outMain.close()

    dirName = "c:\\python-61850\\thesis\\"
    xmlSnippets = glob.glob(dirName + "*.xml")
    for i in xmlSnippets:
        out = open(i)
        lnOld = out.read()
        out.close()
        out = open(i, "w")
        out.write(lnOld.replace("\\'a", "a").replace("\\'e", "e").replace("\\'i", "í").replace("\\'o", "o").replace("\\'u", "u"))
        out.close()

        

if __name__ == "__main__":
    lNodeTypeFromSCLdocumentator("")
    
    
