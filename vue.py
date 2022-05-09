import random
import sys
sys.path.append('.')
sys.path.append('..')
import model,base
import requests

def utilisateur(liste,u):
    idUserLocal=base.session.query(model.User.id).filter(model.User.id==liste[u]['id']).first()
    if idUserLocal:
        pass
    else:
        el=model.User(liste[u]['id'],liste[u]['name'],liste[u]['username'],liste[u]['email'],liste[u]['address']['street'],liste[u]['address']['suite'],liste[u]['address']['city'],liste[u]['address']['zipcode'],
        liste[u]['address']['geo']['lat'],liste[u]['address']['geo']['lng'],liste[u]['phone'], liste[u]['website'],liste[u]['company']['name'],liste[u]['company']['catchPhrase'],liste[u]['company']['bs'],1)
        base.session.add(el)
        base.session.commit()

# for i in range(5):
#     utilisateur(base.f0,i)

def donnees_album(userId):
    f1=requests.get(f"https://jsonplaceholder.typicode.com/albums/?userId={userId}")
    f1=f1.json()
    for u in range(len(f1)):
        idAlbumLocal=base.session.query(model.Album.id).filter(model.Album.id==f1[u]['id']).first()
        if idAlbumLocal:
            pass
        else:
            el=model.Album(f1[u]['userId'],f1[u]['id'],f1[u]['title'],1)
            base.session.add(el)
            base.session.commit()
            base.session.close()
    # for u in range(len(base.f1)):
    #     el=model.Album(base.f1[u]['userId'],base.f1[u]['id'],base.f1[u]['title'])
    #     base.session.add(el)
    # base.session.commit()
# album()

def donnees_photo(albumId):
    f2=requests.get(f"https://jsonplaceholder.typicode.com/photos/?albumId={albumId}")
    f2=f2.json()
    for u in range(len(f2)):
        idPhotoLocal=base.session.query(model.Photo.id).filter(model.Photo.id==f2[u]['id']).first()
        if idPhotoLocal:
            pass
        else:
            el=model.Photo(f2[u]['albumId'],f2[u]['id'],f2[u]['title'],f2[u]['url'],f2[u]['thumbnailUrl'],1)
            base.session.add(el)
            base.session.commit()
            base.session.close()
    # for u in range(len(base.f2)):
    #     el=model.Photo(base.f2[u]['albumId'],base.f2[u]['id'],base.f2[u]['title'],base.f2[u]['url'],base.f2[u]['thumbnailUrl'])
    #     base.session.add(el)
    # base.session.commit()

# Photos()

def donnees_todo(userId):
    f3=requests.get(f"https://jsonplaceholder.typicode.com/todos/?userId={userId}")
    f3=f3.json()
    for u in range(len(f3)):
        print(f3[u])
        idtodos=base.session.query(model.Todo.id).filter(model.Todo.id==f3[u]['id']).first()
        if idtodos:
            pass
        else:
            if f3[u]['completed']==True:
                etat="Termine"
            else:
                etat=random.choice(["En cours","A faire"])
            el=model.Todo(base.f3[u]['userId'],base.f3[u]['id'],base.f3[u]['title'],etat)
            base.session.add(el)
            base.session.commit()
            base.session.close
def donnees_post(userId):
    f4=requests.get(f"https://jsonplaceholder.typicode.com/posts/?userId={userId}")
    f4=f4.json()
    for u in range(len(f4)):
        idPostLocal=base.session.query(model.Post.id).filter(model.Post.id==f4[u]['id']).first()
        if idPostLocal:
            pass
        else:
            el=model.Post(f4[u]['userId'],f4[u]['id'],f4[u]['title'],f4[u]['body'],1)
            base.session.add(el)
            base.session.commit()
            base.session.close()
    # idPost=base.session.query(model.Post.id).filter(model.Post.id==f4[u]['id']).first()
    # postId=idPost['id']
    # return postId
# donnees_post()

def donnees_comment(postId):
    f5=requests.get(f"https://jsonplaceholder.typicode.com/comments/?postId={postId}")
    f5=f5.json()
    for u in range(len(f5)):
        idCommentLocal=base.session.query(model.Comment.id).filter(model.Comment.id==f5[u]['id']).first()
        if idCommentLocal:
            pass
        else:
            el=model.Comment(f5[u]['postId'],f5[u]['id'],f5[u]['name'],f5[u]['email'],f5[u]['body'],1)
            base.session.add(el)
            base.session.commit()
            base.session.close()
    # for u in range(len(base.f5)):
    #     el=model.Comment(base.f5[u]['postId'],base.f5[u]['id'],base.f5[u]['name'],base.f5[u]['email'],base.f5[u]['body'])
    #     base.session.add(el)
    # base.session.commit()
# donnees_comment()


# Récupération du mot de pass correspondant à un username ou email bien definit

def recup_mot_de_pass(email):
    mdp=base.session.query(model.User.mot_de_pass )






# val=base.session.query(model.User)
# for i in val:

