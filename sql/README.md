SQL query:
```bash
SELECT
  t1.pk,
  t1.id,
  t1.title,
  t1.rating,
  t1.last_update
FROM app t1
INNER JOIN (SELECT
  id,
  MAX(last_update) AS most_recent
FROM app
GROUP BY id) t2
  ON t1.id = t2.id
  AND t1.last_update = t2.most_recent;
```
# Output:
  test-#   AND t1.last_update = t2.most_recent;
 pk |            id             |   title    | rating | last_update 
----+---------------------------+------------+--------+-------------
  1 | com.facebook.katana       | Facebook   |    4.0 | 2016-09-12
  3 | com.whatsapp              | WhatsApp   |    4.4 | 2016-09-12
  6 | com.nianticlabs.pokemongo | Pokémon GO |    4.1 | 2016-09-07
(3 rows)



```bash

SELECT
  pk,
  id,
  title,
  rating,
  last_update
FROM (SELECT
  *,
  ROW_NUMBER() OVER (PARTITION BY id ORDER BY last_update DESC) AS rn
FROM app) t
WHERE t.rn = 1;
```
output:

 pk |            id             |   title    | rating | last_update 
----+---------------------------+------------+--------+-------------
  1 | com.facebook.katana       | Facebook   |    4.0 | 2016-09-12
  6 | com.nianticlabs.pokemongo | Pokémon GO |    4.1 | 2016-09-07
  3 | com.whatsapp              | WhatsApp   |    4.4 | 2016-09-12

  The method



```bash
SELECT
  t1.pk,
  t1.id,
  t1.title,
  t1.rating,
  t1.last_update
FROM app t1
LEFT OUTER JOIN app t2
  ON t1.id = t2.id
  AND t1.last_update < t2.last_update
WHERE t2.id IS NULL
ORDER BY t1.last_update DESC;

 pk |            id             |   title    | rating | last_update 
----+---------------------------+------------+--------+-------------
  1 | com.facebook.katana       | Facebook   |    4.0 | 2016-09-12
  3 | com.whatsapp              | WhatsApp   |    4.4 | 2016-09-12
  6 | com.nianticlabs.pokemongo | Pokémon GO |    4.1 | 2016-09-07

  ```




The first approach give corrrect answer for this specific table, but there is no garantee that it wont return
more than one record per date (MAX(last_update)) for a date that will join multiple rows, expercially

Space complexity: