import openpyxl
import tracery


def createTripleList() -> list:
    triples = []
    triple = {}
    actions = []

    path = "C:\\Users\\Vandré\\Documents\\UAM\Materias\\perez2\\PT\\DATA\\Midpoints.xlsx"
    wb_obj = openpyxl.load_workbook(path, read_only=True)#, data_only=True)
    sheet_obj = wb_obj.active

    for row in sheet_obj.iter_rows(min_row = 2, max_col = 3, max_row = 2200):
        for cell in row:
            actions.append([x.strip() for x in cell.value.split(',')])
        triple["BMP"] = actions[0] 
        triple["MP"] = actions[1] 
        triple["AMP"] = actions[2] 
        triples.append(triple.copy())
        triple.clear()
        actions.clear()

    return triples


#Buscar acción
def findTriple(accion_inicial : str, triples : list) -> list:
    for tl in triples:
        if(accion_inicial in tl["BMP"]):
            return tl
    return None

def findActionList( tl : list, point : str) -> list:
    if (point == "BMP"):
        return tl["BMP"]
    if (point == "MP"):
        return tl["MP"]
    if (point == "AMP"):
        return tl["AMP"]
    return None

#############Main#######################
repetitions = set()
triples = createTripleList()
accion_inicial = "alienate"
tripleta =accion_inicial

for x in range(0,10):
    
    while (True):
        tp = findTriple(accion_inicial, triples)
        repetition_index = triples.index(tp)
        print(repetition_index)
        print(repetitions)
        if (repetition_index not in repetitions or tp != None):
            break
    if tp == None:
        break
    repetitions.add(repetition_index)
    BMP = accion_inicial
    MPs = findActionList(tp, "MP")
    AMPs = findActionList(tp, "AMP")

    
    rules = {
        "origin": [",#MP#,#AMP#"],
        "MP" : MPs,
        "AMP" : AMPs
        }

    grammar = tracery.Grammar(rules)
    Mpamp = grammar.flatten("#origin#")
    tripleta += Mpamp
    #print(BMP+Mpamp)
    accion_inicial = Mpamp.split(",")[2]
print(tripleta)

#in veales category actions look for the first action and find a category,
#then find the first character in noc list either subject or object
#(6 opciones para instanciar al menos)

