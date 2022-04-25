import sys
sys.path.append('.')
sys.path.append('..')
import model,base

def utilisateur():
    for u in range(len(base.f0)):
        el=model.User(base.f0[u]['id'],base.f0[u]['name'],base.f0[u]['username'],base.f0[u]['phone'],base.f0[u]['email'],str(base.f0[u]['address']),base.f0[u]['company'])
        base.session.add(el)
    base.session.commit()

# utilisateur()

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






# val=base.session.query(model.User)
# for i in val:

