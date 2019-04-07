##### 
## This section imports the necessary classes and methods from the SQLAlchemy library
####
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

######## IMPORTANT! Change this to your metric number for grading
student_no = 'A0105505U' 
#########################

#####
## This section creates an engine for the PostgreSQL
## and creates a database session s.
#####
username = 'postgres'
password = 'postgres'
dbname = 'cs5421'

# username = 'postgres'
# password = 'postgres'
# dbname = 'cs4221'
engine = create_engine('postgres://%s:%s@localhost:5432/%s' % (username, password, dbname))

Session = sessionmaker(bind=engine)
s = Session()

#####
## Query 
#####
query1 = """
select f.LO_ORDERKEY, p.P_NAME, s.S_NAME, f.LO_ORDERDATE, f.LO_EXTENDEDPRICE from FACT_LINEORDER f
inner join DIM_CUSTOMER c
on f.LO_CUSTKEY = c.C_CUSTKEY
inner join DIM_SUPPLIER s
on f.LO_SUPPKEY = s.S_SUPPKEY
inner join DIM_PART p
on f.LO_PARTKEY = p.P_PARTKEY
where c.C_NAME = 'Customer#000000001';
"""

s.execute(query1)

query2="""
select s.S_NATION, s.S_REGION, c.C_MKTSEGMENT, sum(f.LO_EXTENDEDPRICE) from FACT_LINEORDER f
inner join DIM_PART p
on f.LO_PARTKEY = p.P_PARTKEY
inner join DIM_SUPPLIER s
on f.LO_SUPPKEY = s.S_SUPPKEY
inner join DIM_CUSTOMER c
on f.LO_CUSTKEY = c.C_CUSTKEY
where p.P_BRAND = 'Brand#13'
group by s.S_NATION, s.S_REGION, c.C_MKTSEGMENT;
"""

s.execute(query2)

query3="""
select d.d_year_actual, d.d_month_actual,
sum(f.LO_EXTENDEDPRICE) as sum_extended_price, 
sum(f.LO_EXTENDEDPRICE*(1-f.LO_DISCOUNT)) as sum_extended_discounted_price,
sum(f.LO_EXTENDEDPRICE*(1-f.LO_DISCOUNT)+f.LO_TAX) as sum_extended_discounted_taxed_price, 
avg(f.LO_QUANTITY) as avg_quantity, 
avg(f.LO_DISCOUNT) as avg_discount
from FACT_LINEORDER f
inner join DIM_DATE d
on f.LO_ORDERDATE = d.d_date_actual
group by d.d_year_actual, d.d_month_actual
order by d.d_year_actual, d.d_month_actual asc
"""

s.execute(query3)

query4 = """
select f.LO_ORDERPRIORITY, count(f.LO_ORDERPRIORITY)
from FACT_LINEORDER f
where f.LO_RECEIPTDATE > f.LO_COMMITDATE
group by f.LO_ORDERPRIORITY
order by f.LO_ORDERPRIORITY asc;
"""

s.execute(query4)


s.commit()





