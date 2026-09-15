-- Question 1
SELECT first_name, last_name, email From customer Order By last_name

-- Question 2
SELECT name, unit_price FROM Track WHERE unit_price > 0.99

-- Question 3
SELECT COUNT (track_id) FROM Track 

-- Question 4
SELECT c.first_name, c.last_name, COUNT(i.invoice_id)
FROM customer as c 
LEFT JOIN invoice as i 
ON c.customer_id=i.customer_id
GROUP BY c.customer_id
Order BY count desc

-- Question 5
SELECT t.name, count (il.track_id)
FROM track as t
JOIN invoice_line as il
ON t.track_id=il.track_id
GROUP BY t.name
Order BY count desc
LIMIT 5

-- Question 6
SELECT a.title, ar.name, COUNT(t.album_id) as number_tracks
FROM album as a
JOIN artist as ar 
ON a.artist_id=ar.artist_id
JOIN track as t
ON t.album_id = a.album_id
GROUP BY ar.name, a.title
ORDER BY number_tracks DESC

-- Question 7
SELECT concat(c.first_name, ' ', c.last_name) as customer_full_name, 
concat(e.first_name, ' ', e.last_name) as employee_full_name,
c.country
FROM customer as c
JOIN employee as e
ON c.support_rep_id = e.employee_id
WHERE e.country = c.country
 
-- Question 8
SELECT g.name as genre_name, SUM(i.unit_price) as revenue
FROM genre as g
JOIN track as t 
ON t.genre_id = g.genre_id
JOIN invoice_line as i 
ON t.track_id = i.track_id
GROUP BY genre_name
ORDER BY revenue DESC

-- Question 9 
SELECT TO_CHAR(i.invoice_date, 'MM Month') as month, SUM(il.unit_price) as revenue
FROM invoice as i
JOIN invoice_line il
ON i.invoice_id = il.invoice_id
WHERE TO_CHAR(invoice_date, 'YYYY') = '2021' 
GROUP BY month
ORDER BY month

-- Question 10
SELECT DISTINCT concat(c.first_name, ' ', c.last_name) as full_name, c.email
FROM customer as c
LEFT JOIN invoice as i
ON c.customer_id = i.customer_id
JOIN invoice_line as il
ON i.invoice_id = il.invoice_id 
JOIN track as t
ON t.track_id = il.track_id
WHERE t.genre_id != 1
Order by full_name

-- QUESTION 11
