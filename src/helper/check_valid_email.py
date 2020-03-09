import re 
  

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
      
def check(email):  
  
    if(re.search(regex,email)):  
        print("Valid Email")  
          
    else:  
        print("Invalid Email")  
      
if __name__ == '__main__' :  
      
    email = "ankitrai326@gmail.com"
       
    check(email) 
  
    email = "my.ownsite@ourearth.org"
    check(email) 
  
    email = "ankitrai326.com"
    check(email) 