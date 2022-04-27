import sys
sys.path.append('.')
sys.path.append('..')
import model,base

def utilisateur(liste,u):
    el=model.User(liste[u]['id'],liste[u]['name'],liste[u]['username'],liste[u]['phone'],liste[u]['email'],str(liste[u]['address']),str(liste[u]['company']), liste[u]['website'])
    base.session.add(el)
    base.session.commit()

# for i in range(5):
#     utilisateur(base.f0,i)

def album():
    for u in range(len(base.f1)):
        el=model.Album(base.f1[u]['userId'],base.f1[u]['id'],base.f1[u]['title'])
        base.session.add(el)
    base.session.commit()
# album()

def photo():
    for u in range(len(base.f2)):
        el=model.Photo(base.f2[u]['albumId'],base.f2[u]['id'],base.f2[u]['title'],base.f2[u]['url'],base.f2[u]['thumbnailUrl'])
        base.session.add(el)
    base.session.commit()

# photo()

def donnees_todo():
    for u in range(len(base.f3)):
        el=model.Todo(base.f3[u]['userId'],base.f3[u]['id'],base.f3[u]['title'],base.f3[u]['completed'])
        base.session.add(el)
    base.session.commit()
# donnees_todo()

def donnees_post():
    for u in range(len(base.f4)):
        el=model.Post(base.f4[u]['userId'],base.f4[u]['id'],base.f4[u]['title'],base.f4[u]['body'])
        base.session.add(el)
    base.session.commit()
# donnees_post()

def donnees_comment():
    for u in range(len(base.f5)):
        el=model.Comment(base.f5[u]['postId'],base.f5[u]['id'],base.f5[u]['name'],base.f5[u]['email'],base.f5[u]['body'])
        base.session.add(el)
    base.session.commit()
# donnees_comment()


# Récupération du mot de pass correspondant à un username ou email bien definit

def recup_mot_de_pass(email):
    mdp=base.session.query(model.User.mot_de_pass )






# val=base.session.query(model.User)
# for i in val:

