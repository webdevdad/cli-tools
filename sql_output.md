# SQL Query
```sql
```sql
SELECT u.*
FROM users u
WHERE u.email IN 
    (
    SELECT email
    FROM users
    GROUP BY email
    HAVING COUNT(email) > 1
    )
```
```

## Explanation
This query first creates a subquery that groups entries in the users table by the email field and counts how many times an email occurs. The HAVING clause then filters out the emails that occur more than once. Then, the main query selects the detail of users that have an email in the result of the subquery, effectively giving us the users with duplicate emails.

## Alternative Approaches
- 1. Using a self join on email field:
- 
- ```sql
- SELECT u1.*
- FROM users u1 
- JOIN users u2 ON u1.email = u2.email
- WHERE u1.id != u2.id
- ```
- This query works by doing a self join on the email column, and then filtering out rows where the user id is the same in both tables (to get rid of situations where a user is joined with itself).
- 
- 2. Using window function:
- 
- ```sql
- SELECT user_id, email
- FROM (
-     SELECT user_id, email, COUNT(*) OVER (PARTITION BY email) as cnt
-     FROM users
- ) t
- WHERE cnt > 1
- ```
- This alternative uses a window function to count the occurrences of each email. The window function partitions the data by email, counts the occurrences, and only selects rows where the count is more than 1. The subquery is necessary because window functions cannot be used directly in WHERE clauses.
- 
- Note: Null values and SQL injection are not a concern here as no external inputs are being used in the query, and all data is coming directly from the table. Parameterization is also not applicable for the same reason.

Safety Rating: 4/5