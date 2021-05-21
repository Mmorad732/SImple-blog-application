pip install redis

import redis 
import json
user = None

class loggedInUser:
    def __init__(self, un , password):
         self._un = un
         self._password = password
      
    # getters method
    def get_un(self):
        return self._un
    
    def get_password(self):
        return self._password 
    
    # setters method
    def set_un(self, un):
        self._un = un
        
    def set_password(self, un):
        self._password = password
        
        
def auth(un,password):
    password = password
    if db.hexists('users',un.upper()):
        json_str = json.loads(db.hget('users',un))  
        if json_str['password']== password.upper():
            return True
    else:
        return False
    
def login():
    rep = True
    print("log in")
    log_un = input("username : ").upper()
    log_password = input("Password : ").upper()
    if auth(log_un,log_password) :
        global user
        user = loggedInUser(log_un,log_password)
        print("Logged in")
        print("user",user.get_un())
        return True
    else:
        print("Invalid Username or Password")
        return False
        
def signup():
    account = {}
    un = input("username: ").upper()
    if db.hexists('users',un) == False:
        account['name'] = input("name: ")
        account['password'] = input("password: ").upper()
        if un != 'ADMIN':
            account['age'] = int(input("age: "))
        json_str = json.dumps(account)
        user = loggedInUser(un,account['password'])
        db.hset('users',un,json_str)  
        
    else:
        print("Username alread exists")
    
        
    


db = redis.Redis("localhost")
print(" 1- Create User \n 2- Login and edit \n 3- Write a post \n"
    + " 4- Log out \n 5- show user info \n 6- Show your posts \n"
    + " 7- Delete posts \n 8- Delete users(for admin)\n 9- View all blogs \n"
    + " 10- Quit \n 11- Save \n 12-Flush database \n")

cont = True
while cont:
  op = input("Enter operation: ")
  if op == '1':
        signup()
    
  elif op == '2':
    
    if login():
        print(db.hmget('users',user.get_un()))
        edit = input("Edit (yes/no) : ").upper()
        if edit == "YES":
            field = input("field : ").lower()
            account = json.loads(db.hget('users',user.get_un()))
            if account[field] != None :
                new = input("new : ").lower()
                if new == 'posts':
                    print('Not available')
                    continue
                else:
                    account[field] = new
                    password = account['password']
                    user.set_password(password)
                    account = json.dumps(account)
                    db.hset('users',user.get_un(),account) 
                
       
        
  elif op == '3':
    if user == None:
        if login() == False:
            continue
            
    if user != None:    
        if auth(user.get_un(),user.get_password()) : 
            db.incr("postid")
            post = {'user':"" , 'header':"",'body':""}
            post['header'] = input("Header: ")
            post['body'] = input("Body: ")
            post['user'] = user.get_un()
            json_post = json.dumps(post)
            db.hset( 'posts',db.get("postid") , json_post )
            json_user = json.loads(db.hget('users',user.get_un()))
            
            if 'posts' in json_user:
                posts= {'posts':[]}
                posts['posts'] = json_user['posts']
                posts['posts'].append(int(db.get("postid").decode()))
                json_user['posts'] = posts['posts']
                json_user = json.dumps(json_user)
                db.hset('users',user.get_un(),json_user)
            
            else:
                posts= {'posts':[]}
                posts['posts'].append(int(db.get("postid").decode())) 
                json_user['posts'] = posts['posts']
                json_user = json.dumps(json_user)
                db.hset('users',user.get_un(),json_user)
                
               

  elif op == '4':
    if user != None:
        user = None
        
  elif op == '5':
    if user == None:
        if login() == False:
            continue
    if user != None:
        json_user = json.loads(db.hget('users',user.get_un()))
        print(json_user)


        
  elif op == '6':
    if user == None:
        if login() == False:
            continue
    if user != None:
        json_str = json.loads(db.hget('users',user.get_un()))
        if 'posts' in json_str :
            if len(json_str['posts']) != 0 :
                for x in json_str['posts']:
                    json_post = json.loads(db.hget('posts',x))
                    print(" Writer : ",json_post['user']," \n Post ID : ",x," \n" 
                        + " Header : ",json_post['header']," \n Body : ",json_post['body'])
            else:
                print("No posts yet")
        else:
            print("No posts yet")
  elif op == '7':
    if user == None:
        if login() == False:
            continue
    if user!= None:
        json_user = json.loads(db.hget('users',user.get_un()))
        print(json_user['posts'])
        postId = input("choose post id to delete : ")
        if postId != 0 and int(postId) in json_user['posts']:
            json_user['posts'].remove(int(postId))
            json_user = json.dumps(json_user)
            db.hset('users',user.get_un(),json_user)
            db.hdel('posts',postId)
            
            
        else:
            continue
  
  elif op == '8':
        if user == None:
            if login() == False:
                continue
        if user != None:
            if user.get_un() == 'ADMIN' and user.get_password() == 'ADMIN':
                print(db.hgetall('users'))
                username = input('Choose user name to delete').upper()
                if db.hexists('users',username) and user.get_un() != username:
                    json_user = json.loads(db.hget('users',username))
                    if 'posts' in json_user:
                        if len(json_user['posts']) != 0:
                            for x in json_user['posts']:
                                db.hdel('posts',x)
                    db.hdel('users',username)
                    print('User seccessfully deleted')
                else:
                    print("Action invalid")
                    continue
            else:
                print("Access denied")
  elif op == '9':
    postsIds = db.hkeys('posts')
    for x in postsIds:
        x = x.decode()
        json_post = json.loads(db.hget('posts',x))
        json_user = json.loads(db.hget('users',json_post['user']))
        print(" Writer : ",json_user['name']," \n Post ID : ",x," \n" 
            + " Header : ",json_post['header']," \n Body : ",json_post['body'] ,"\nn ========")
    
  elif op == '10':
    cont = False
    print("Quitted")
  elif op == '11':
    db.lastsave()
  elif op == '12':
    db.flushall()
    print("Database flushed")
  


  



