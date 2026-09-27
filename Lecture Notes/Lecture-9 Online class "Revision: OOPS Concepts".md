#class and objects
#database
#pandas 

#Data-anything that gets gnerate on your electronics parts
#anything getting wriiten on your hard drive is called data .

#data-different types-Structured data -CSV,excel,xml file.
#unstructured -pdf,images and videos.
semi structured-json-javascript object notation-dict
#dict vs json-dict-key


structure data -datatype

primitive datatype --> int float string char and complex number 
and non-primitive data --> user defined data type
--> class structure 


#class-blueprint of your data .how the data will look like
class classname:
    variable functions

#variable-space where we store the data
-glass
-we store the water 


#function-behaviour 

#variable types--instance func, class func and static function
#function types--instance func , class func and static function


#instance-class in memory .
#instance of class be infinite

memory-ram of your pc
#instance of class is called as object.


            abc=classname()
            e.g user class

            class User:
            #class variable
            id=0
            #constructor
            #self reference
            #instance reference 
            def__init__(self,name):
            #instance variable
            #self.variable_name
            self.name=name
            self.employee_id=user.id+1
            user.id+=1

            def get_user_info(self):
                print(f"user_id: {self.user_id},"name: {self.name}") 


            #class function
            @classmethod
            def employee_count(cls):
                    print(User.id)

            @staticmethod()
            def static_user():
              count=0
                return "user"

            def__init__(self,name)

            #self variable

            def get_user_info(self):
            print(f"user_id: {self.user_id},"name: {self.name}")


            @staticmethod()
            def static_user():
            count=0
            return "user"


            User.employee_count
            obj=user()
            obj=User("Trisha")  #constructor automatically called.add()
            obj.get_user_info() #explicitly  calling function

            ##u can call as
            User.static_user
            obj.static

#class-properties-oops
#object oriented programming system
#major pillars
#minor pillars

#major - abstraction,encapsulation,polymorphism and hierarcy
#minor - concurrency and modularity 

#abstraction - hiding the implimentation and giving an getting access 
#encapsulation - binding of a data with function.

#polymorphism - different forms (functions)  #different behaviour
#ek function- different forms hum usse polymorphism 
#poly- static runtime and compile time poly 
#compile- function is identified in compile time
#runtime - jab runtime pr work ho 

           class user:
            def user():
            def user(this,name):
             def user(this,name,mobile)

#hierarchy-  composition and inheritance 
#inheritance - parent - child behavior 

        class department:
            self.name=dept_name

        class Employee(user):
            def__init__(self,name,mobile,dept_name): # runtime poly
                self.__super__(self,name,mobile)
                self.dept=Department(dept_name) # composition 
    
        def get_user_info(self): #runtime polu
        print((f"user_id): {user_id} user_name: {self.name} dept_name:
        {dept_name}")

        #abstract class and interface 
        #abstract class -cannot create object of it 
        #partial incomplete methods -

        #class-all function are incomplete methods - interface 
        #force to apply the certain behavior 

        #MRO  - Method resolution order
        #python supports multiple inheritance  
        #class bird(flayable , aquatic ) # left hand side class will have priority 
        #flyable and aquatic- function pqr- function of flyable will get called

        abc import ABC,abstractmethod

        #abstract class and interface 
        #all interface class are abstract class but not a vice -versa
        class flyable(ABC):

        @abstractmethod
        def fly(self):
             pass

        class flyable(ABC):

        @abstractmethod
        def fly(self):
        pass

        #instance method/concrete method
        def get_bird_name(self):
           return self.bird_name

           #class complete          
