# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response

class Question:

    def __init__(self,task,points,id,visited=False):
        self.task = task
        self.points = points
        self.visited = visited
        self.id = id

    def __str__(self):
        return str(self.task) + " " +str(self.points)

class Team:

    def __init__(self,name,points):
        self.name=name
        self.points = points


def emptyTeams():
    return [['Červení diabli',0],['Ninja go',0],['Jastrabi',0]]



def DB():
    q=[
     [  'Zvieratá',
        'Koľko nôh má kôň ?',
        'Koľko bodiek má lienka ?',
        'Ako sa volá mláďa koňa?',
        'Ktoré vtáky lietajú nízko keď bude pršať ?',
        'Koľko dní sedí sliepka na vajciach kým sa nevyliahnú kuriatka (tolerancia 5 dní)?'

    ],
     [  'Náboženstvo',
        'Ako ss volali prví ľudia ?',
        'Koľko tajomstiev má jeden ruženec ?',
        'Čo postavil Noe ?',
        'Čo symbolizuje blikajúce červené svetielko v kostole ?',
        'Vymenuj desatoro'

    ],
     [
     'Zemepis',
     'V ktorej krajine žijeme ?',
     'Aké je naše hlavné mesto ?',
     'V ktorej časi Slovenska sa nachádzjú Bánovce ? Východ alebo západ ?',
     'Vymenuj aspoň 3 susedné štáty Slovenska',
     'Ako sa volá najvyšší vrch Slovenska ?'
     ],

     [
         'Rôzne',
         'Koľko má deň hodín ?',
         'Môžeš stretnúť ťavu v Antarktíde ? Prečo ?',
         'Keď predbehneš posledného koľký budeš ?',
         'Čo znamená červená farba na semafore ?',
         'Ktora hviedza je najbližšie k Zemi ?'


     ],
     [
       'Hádanky',
       'Ktorí hráči vždy vyhrávajú ?',
       'Kabátik má pichľavý, schováva sa do trávy.',
       'Štyri rohy, štyri nohy ale hlava nikde.',
       'S kamarátmi jedlo drobia, okrem toho ústa zdobia',
       'Len jeden kopček je jeho domček'
     ]
     ]
    return q


def parseDB(getid=-1):
    questions = {}
    id=0
    for category in DB():
        tmp = []

        for i in range(len(category)-1):
            if int(id) == int(getid):
                return Question(category[i+1],(i+1)*10,id)
            tmp.append(Question(category[i+1],(i+1)*10,id))
            id+=1
        questions[category[0]] = tmp
    return questions

def show(request,id):
    print(id)
    question = parseDB(id)
    print (question)
    return render_to_response('show.html',locals())


def reset(request):
    if 'visited' in request.session:
        del request.session['visited']
    if 'teams' in request.session:
        del request.session['teams']
    if 'curteam' in request.session:
        del request.session['curteam']
    return index(request)

def vysledky(request):
    tmp = request.session.get('teams',emptyTeams())
    teams = []
    for team in tmp:
        teams.append(Team(team[0],team[1]))
    return render_to_response('vysledky.html',locals())



def index(request,id=-1,ans=-1 ):

    #########################
    # Nacitanie veci z databazy
    #########################

    #tím na ťahu
    curteam = request.session.get('curteam',0)

    #ak neexistoval, tak ho nastav
    request.session['curteam']=curteam

    #nacitaj navstivene otazky
    visited = request.session.get('visited',{})

    #nacitaj timy
    teams = request.session.get('teams',emptyTeams())

    ###########################
    # Spracovanie zodpovedanej otazky
    ###########################

    #oznac otazku za pouzitu
    visited[id]=True

    #ak bola odpoved spravna pripocitaj body
    if ans=='1':
        teams[curteam][1]+=parseDB(id).points

    #ak bola zodpovedana otazka(niesme na zaciatku), tak pojde nasledujuci tim
    if(id!=-1):
        curteam+=1;
        curteam%=len(emptyTeams())

    ##############################
    # Priprava mapy s otazkami
    ##############################

    #nacitaj otazky z DB a oznac uz pouzite
    questions = parseDB()
    for name,category in questions.items():
            for q in category:
                q.visited=visited.get(str(q.id),False);


    #uloz zmeny do DB
    request.session['visited']=visited
    request.session['teams']=teams
    request.session['curteam']=curteam


    #debug
    print(len(emptyTeams()))
    print(teams)
    print(curteam)
    print(teams[curteam])

    #tim na tahu
    naTahu = teams[curteam][0]


    #############################
    # priprav vysledky
    #############################

    tmp = request.session.get('teams',emptyTeams())
    vysledky = []
    for team in tmp:
        vysledky.append(Team(team[0],team[1]))

    return render_to_response('index.html',locals())