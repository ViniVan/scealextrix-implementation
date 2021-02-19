import openpyxl
import random

def loadCategoryList() -> list:
    triples = []
    triple = {}
    actions = []
    
    path = "C:\\Users\\Vandré\\Documents\\UAM\Materias\\perez2\\PT\\DATA\\Category.xlsx"
    wb_obj = openpyxl.load_workbook(path, read_only=True)#, data_only=True)
    sheet_obj = wb_obj.active

    for row in sheet_obj.iter_rows(min_row = 2, min_col = 2, max_col = 4 , max_row = 400):
        for cell in row:
            actions.append([x.strip() for x in cell.value.split(',')])
        triple["Category"] = actions[0][0]
        triple["Subject"] = actions[1] 
        triple["Object"] = actions[2] 
        triples.append(triple.copy())
        triple.clear()
        actions.clear()
    return triples

def getCategory(catlist : list, accion_inicial : str) -> str:   #solo como sujeto de la acción
    possible_cats = [dic["Category"] for dic in catlist if accion_inicial in dic["Subject"]]
    if (not possible_cats):
        return None
    return random.choice(possible_cats)
    
######################ONLY FOR DEBUGGING############################
##rows = loadCategoryList()
##print (getCategory(rows,"preach_to"))
