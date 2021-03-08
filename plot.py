import category as cat
import character as char
import tracery
import random
from noc import triples, initial_bookends, closing_bookends, idioms, connectors

def getTriple(accion_inicial : str) -> list:
    possible_triples = [tl for tl in triples if accion_inicial in tl["BMP"]]
    if (not possible_triples):
        return None
    return random.choice(possible_triples)

def getActionList( tl : list, point : str) -> list:
    if (point == "BMP"):
        return tl["BMP"]
    if (point == "MP"):
        return tl["MP"]
    if (point == "AMP"):
        return tl["AMP"]
    return None

def getInitialBookend(accion_inicial : str) -> str:
    for pair in initial_bookends:
        if(pair["action"] == accion_inicial):
            return random.choice(pair["renderings"])
    return None

def getClosingBookend(accion_final : str) -> str:
    for pair in closing_bookends:
        if  (pair["action"] == accion_final):
            return random.choice(pair["renderings"])
    return None

def getIdiom(accion : str) -> str:
    for pair in idioms:
        if  (pair["action"] == accion):
            return random.choice(pair["renderings"])
    return None

def plot(accion_inicial : str, size : int, direct_antagonist = True) -> dict:
    story = {}
    used_triples = set()
    sel_actions = set()
    opening = accion_inicial
    plot = "A" + accion_inicial + "B"

    ################# Load Category and Characters ####################
    category = cat.getCategory(accion_inicial)
    protagonist= char.getProg(category)
    A = protagonist["Name"]
    report = 0
    story["A"] = A
    story["Category"] = category
    if (direct_antagonist == True):
        B = char.getOpp_by_simple(protagonist)
        report = "Se escogió a B como un rival directo de A"
        if (B == None):
            direct_antagonist = False
    if (direct_antagonist == False):
        B = char.getOpp_by_world(protagonist)
        report = "Se escogió a B por ser del mismo mundo que A"
        if (B == None):
            B = char.getOpp_by_politics(protagonist)
            report = "Se escogió a B por la oposición de posturas políticas con A"
            if (B == None):
                B = char.getOpp_by_domain(protagonist)
                report = "Se escogió a B ya que es del mismo dominio que A"
                if (B == None):
                    B = char.getOpp_by_group(protagonist)
                    report = "Se escogió a B ya que forma parte del mismo grupo que A"
                    if (B == None):
                        B = char.getOpp_by_actor(protagonist)
                        report = "Se escogió a B como antagonista de A ya que comparten al mismo actor o actriz"
                        if (B == none):
                            while (True):
                                B = char.getProg(category)
                                if (B != A):
                                    report = "Se escogió a B al azar"
                                    break
    story["report"] = report
    story["B"] = B
    ##################Plot creation#########################
    as_beginning = True

    for x in range(0,size):
        while (True):
            tp = getTriple(accion_inicial)
            if (tp == None):
                as_beginning = False
                break
            triple_index = triples.index(tp)
            if (triple_index not in used_triples):
                break
        if (as_beginning == False):
            break
        used_triples.add(triple_index)

        midpoints_list = getActionList(tp, "MP")
        afterpoints_list = getActionList(tp, "AMP")

        rules = {
            "origin": [",A#MP#B,A#AMP#B"],
            "MP" : midpoints_list,
            "AMP" : afterpoints_list
            }

        grammar = tracery.Grammar(rules)
        mid_after_points = grammar.flatten("#origin#")
        accion_inicial = mid_after_points.split(",")[2][1:-1] ## next first action
        midpoint = mid_after_points.split(",")[1][1:-1]
        sel_actions.add(accion_inicial)
        sel_actions.add(midpoint)
        plot += mid_after_points.replace(",",". ")
        
        action_pair = {'before': midpoint, 'after': accion_inicial}
        for conn in connectors:
            if (action_pair == conn['pair']):
                if (conn['link'] == "and"):
                    plot = plot.replace("A"+ midpoint + "B.", "A"+ midpoint + "B" + conn['link'])
                else:
                    plot = plot.replace("A"+ midpoint + "B.", "A"+ midpoint + "B" + ", " + conn['link'])
      #  plot = plot.replace(",",". ")

    story["plot"] = plot
    
    ######################Printing############################
    closing = accion_inicial
    opening_idiom = getInitialBookend(opening)
    closing_idiom = getClosingBookend(closing)
    if opening_idiom == None:
        opening_idiom = getIdiom(opening)
    if closing_idiom == None:
        closing_idiom = getIdiom(closing)

    plot = plot.replace("A"+opening+"B", opening_idiom).replace("A"+closing+"B", closing_idiom)

    for action in sel_actions:
        if ('*' in action):
            replacement = getIdiom(action.strip('*'))
            if (replacement != None):
                plot = plot.replace("A"+action+"B", replacement.replace("A", "$").replace("B", "#").replace("$", "B").replace("#","A"))
        else:
            replacement = getIdiom(action)
            if (replacement != None):
                plot = plot.replace("A"+action+"B", replacement)
    story["story"] = plot.replace("A", "$").replace("B", "#").replace("$", A).replace("#",B)

    return story  
