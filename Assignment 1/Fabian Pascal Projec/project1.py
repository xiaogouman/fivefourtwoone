##### 
## This section imports the necessary classes and methods from the SQLAlchemy library
####
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#####
## This section creates an engine for the PostgreSQL
## and creates a database session s.
#####
username = 'postgres'
password = 'postgres'
dbname = 'cs4221'
engine = create_engine('postgres://%s:%s@localhost:5432/%s' % (username, password, dbname))

Session = sessionmaker(bind=engine)
s = Session()


#####
## 1. Write your stored procedures here, the template is given.
#####
s.execute("""
    CREATE OR REPLACE FUNCTION test (TEXT, INT)
    RETURNS TEXT AS $$
    BEGIN
    RETURN 0.0;
    END;
    $$ LANGUAGE plpgsql;
""")


#####
## This code is used to check the correctness of your queries.
## The check_query function returns (X,Y) where X = 1 if the query is correct and 0 if it is wrong
## and Y is the average execution time if X = 1 otherwise Y = 0.
## Remember that your score is 0 if X = 0.
## YOU CAN IGNORE THIS PART OF THE CODE
#####
def check_query (query): 
    try:
        result = [tuple(a) for a in list(s.execute(query))]
    except:
        return 0,0 

    ## example query with a cross join
    query_cross = """SELECT per.empid, per.lname
                     FROM employee per, payroll pay
                     WHERE per.empid = pay.empid AND pay.salary = 199170;"""
    answer = [tuple(a) for a in list(s.execute(query_cross))]

    ## Check number of results
    if len(result) != len(answer):
        return 0, 0

    ## Check content query - answer
    found = False
    for res in result:
        if res not in answer:
            found = True
            break
        
    if found:
        return 0, 0

    ## Check content answer - query
    found = False
    for res in answer:
        if res not in result:
            found = True
            break

    if found:
        return 0, 0 

    query = query.replace("\n", " ")
    explain = list(s.execute("SELECT test('" + query + "', 1000);"))
    time = float(explain[0][0])
    return 1, time
        
#####
## 2. Write different but equivalent SQL queries that find the identifier and the last name of the employees earning a salary of $199170.
## Replace the queries below by your answer.
#####

## a simple query with an OUTER JOIN, in the WHERE clause you can only check for the NULL values and nothing else
print check_query(""" SELECT * 
                      FROM employee e, payroll p
                      LIMIT 1;
                  """)
## a nested query  with a correlated subquery in the WHERE clause
print check_query(""" SELECT * 
                      FROM employee e, payroll p
                      LIMIT 1;
                  """)

## a nested query with an uncorrelated subquery in the WHERE clause
print check_query(""" SELECT * 
                      FROM employee e, payroll p
                      LIMIT 1;
                  """)
## a nested query  with an uncorrelated subquery  in the FROM clause
print check_query(""" SELECT * 
                      FROM employee e, payroll p
                      LIMIT 1;
                  """)
## a double-negative nested query with a correlated subquery in the WHERE clause
print check_query(""" SELECT * 
                      FROM employee e, payroll p
                      LIMIT 1;
                  """)


#####
## 3. Write your new query that is non-trivially as slow as possible. 
####
print check_query(""" SELECT * 
                      FROM employee e, payroll p
                      LIMIT 1;
                  """)

