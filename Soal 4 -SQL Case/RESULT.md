# Result of Soal 4 - SQL Case

In this case, there is problem with data quality which totally null columns they are `productRevenue`,  `productRefundAmount` and also lack of meta data to describe what the data talk about. I assure only `test case 2` since it is not full null. 

# Steps to solve the problem
- Run PostgreSQL in Docker container
- Storing all data to PostgreSQL using pandas
- Create `postgres.sql` and all script test cases with documentation using Dbeaver