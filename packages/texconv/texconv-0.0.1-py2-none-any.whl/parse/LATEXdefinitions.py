import os
import subprocess
import datetime

date = datetime.date.today()
ss_date = date.strftime("%Y-%m-%d")

greek_dic = {'alpha':fr'\alpha', 
             'beta':fr'\beta', 
             'gamma':fr'\gamma',
             'delta':fr'\delta',
             'epsilon':fr'\varepsilon',
             'zeta':fr'\zeta',
             'eta':fr'\eta',
             'theta':fr'\theta',
             'lambda':fr'\lamda',
             'mu':fr'\mu',
             'pi':fr'\pi',
             'nabla':fr'\nabla',
             'theta':fr'\theta'}

ss_dir = ""

#get a greek letter from the dictionary
def greek(name):
    return greek_dic.get(name)

def cos():
    return fr"\cos"

def sin(string):
    return fr"\sin"

def give_infinity():
    infinity = "\infty"
    return infinity

def create(name):
    global fl
    global tex_name
    tex_name = name
    fl = open("{file_name}.tex".format(file_name = name), 'a')

def clear():
    with open(f"{tex_name}.tex", "w") as k:
        pass 

def texcurl(string):
    return "{" + string + "}"

#initial header/setup
def preamble(type, title, author):
    fl.write(fr"\documentclass" + texcurl(fr"{type}") + "\n")
    fl.write(fr"\title" + texcurl(fr"{title}") + "\n")
    fl.write(fr"\author" + texcurl(fr"{author}") + "\n")
    fl.write(fr"\usepackage{{graphicx}}" + "\n")
    fl.write(fr"\graphicspath" + "{" + texcurl(fr"{ss_dir}") + "}" + "\n")
    fl.write("\n")

#add a list of figures in the notes and then do a pagebreak for formatting purposes
def figure_index():
    fl.write(fr"\listoffigures" + "\n")
    fl.write(fr"\pagebreak" + "\n")

#adds a list of topics and sections/subsections within the doc
def topic_index():
    fl.write(fr"\tableofcontents" + "\n")

#ong_bruh lets begin
def ong_bruh():
    fl.write(fr"\begin{{document}}" + "\n")
    fl.write(fr'\maketitle' + "\n")


#line has function searching; similar to implicit concat
#no need for splitting up the string
def line(string, double):
    retstring = ""
    if ";" in string:
        split_list = string.split(";")
        for element in split_list:
            if "'" in element:
                retstring += str(eval(element))
            else:
                retstring += element
        if double == False:
            fl.write(retstring + "\n")
        elif double == True:
            fl.write(retstring + "\\\\" + "\n")
            fl.write("\n")
    else:
        if double == False:
            fl.write(string + "\n")
        elif double == True:
            fl.write(string + "\\\\" + "\n")

def d_partial(x, y):
    return fr"\frac{{\partial {y}}}{{\partial {x}}}"

def equation(left, right):
    fl.write("\n")
    fl.write(fr"\begin{{equation}}" + "\n")
    fl.write(left + " = " + right)
    fl.write("\n")
    fl.write(fr"\end{{equation}}" + "\n")

#math formatting (math italics)
def math(string):
    return "$" + string + "$"

#time must be in hh.mm and 12 hour time not 24
def image(time, capt):
    for filename in os.listdir(ss_dir):
        if str(time) in filename:
            fl.write("\n")

            #format it so that it fits the text flow
            fl.write(fr"\begin{{figure}}[h]" + "\n")
            fl.write(fr"\caption" + texcurl(fr"{capt}") + "\n")
            fl.write(fr"\centering" + "\n")
            fl.write(fr"\includegraphics" + "[width=5cm, height=5cm]" + texcurl(fr"{filename}") + "\n")
            fl.write(fr"\end{{figure}}" + "\n")

#use this for new topic or slide
def topic(string):
    fl.write("\n")
    fl.write(fr"\subsection" + texcurl(fr"{string}") + "\n")

#use this for an example problem
def example(string):
    fl.write("\n")
    fl.write(fr"\subsubsection" + texcurl(fr"{string}") + "\n")

#definite and indefinite single integrals
def integral(func, var, lower = None, upper = None):
    if lower != None and upper != None:
        return (fr"\(\int_" + texcurl(fr"{lower}") + "^" + texcurl(fr"{upper}") + fr" {func} \," + fr"d{var} \)")
    else:
        return (fr"\(\int" + fr" {func} \," + fr"d{var} \)")  

#sqrt function    
def sqrt(string):
    return fr"\sqrt{string}"

#end the script
def gahzamn():
    fl.write(fr"\end{{document}}")

#compile the python script and open it in Texshop file
def compile():
    subprocess.run(["open", "-a", "TeXShop", f"{tex_name}.tex"])



