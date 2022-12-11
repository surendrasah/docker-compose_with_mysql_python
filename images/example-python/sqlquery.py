########examples table query##########
def drop_examplestable():
    return("DROP TABLE IF EXISTS examples;")

def create_examplestable():
    return("CREATE TABLE examples(id int NOT NULL auto_increment primary key,name varchar(80) default null);")

def insert_exampletable():
    return("INSERT INTO codetest.examples(name) VALUES (%s);")


def select_examplestable():
    return("""SELECT * FROM codetest.examples """)
    


##########people table query############

def insert_peopletable():
    return("INSERT INTO codetest.people VALUES (%s,%s,%s,%s);")

def select_peopletable():
    return("""SELECT * FROM codetest.people """)




#########place table query################
def insert_placestable():
    return("""INSERT INTO codetest.places VALUES (%s,%s,%s);""")


def select_placestable():
    return("""SELECT * FROM codetest.places ;""")
    
    
    
    
####summary query#############
def summary_query():
	return(""" SELECT country,count(country) FROM codetest.places
		   INNER JOIN codetest.people
		   ON place_of_birth = city
		   GROUP BY country ;""")
