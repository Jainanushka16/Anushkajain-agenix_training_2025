-- Retrieve the top 5 most-issued books with their issue count:
FROM books b
JOIN book_transactions bt ON b.book_id = bt.book_id
GROUP BY b.book_id
ORDER BY issue_count DESC
LIMIT 5;
-- List books along with their authors that belong to the “Fantasy” genre, sorted by publication year:
FROM books b
JOIN authors a ON b.author_id = a.author_id
WHERE b.genre = 'Fantasy'
ORDER BY b.publication_year DESC;
-- 	Identify the top 3 customers who have borrowed the most books:
FROM customers c
JOIN book_transactions bt ON c.customer_id = bt.customer_id
GROUP BY c.customer_id
ORDER BY borrow_count DESC
LIMIT 3;
--	List all customers who have overdue books:FROM customers c
JOIN book_transactions bt ON c.customer_id = bt.customer_id
WHERE bt.return_date IS NULL AND bt.issue_date < CURRENT_DATE - INTERVAL '30 days';
-- 	Find authors who have written more than 3 books:
FROM authors a
JOIN books b ON a.author_id = b.author_id
GROUP BY a.author_id
HAVING COUNT(b.book_id) > 3;
-- Retrieve a list of authors who have books issued in the last 6 monthsSELECT DISTINCT 
FROM authors a
JOIN books b ON a.author_id = b.author_id
JOIN book_transactions bt ON b.book_id = bt.book_id
WHERE bt.issue_date > CURRENT_DATE - INTERVAL '6 months';
-- Calculate the total number of books currently issued and the percentage of books issued compared to the total available: 
    (SELECT COUNT(*) FROM book_transactions WHERE return_date IS NULL) AS issued_books,
    (SELECT COUNT(*) FROM books) AS total_books,
    ROUND((COUNT() * 100.0 / (SELECT COUNT() FROM books)), 2) AS issued_percentage
FROM book_transactions
WHERE  IS NULL;
--Generate a monthly report of issued books for the past year:
    TO_CHAR(bt.issue_date, 'YYYY-MM') AS month,
    COUNT(bt.transaction_id) AS book_count,
    COUNT(DISTINCT bt.customer_id) AS unique_customer_count
FROM book_transactions bt
WHERE bt.issue_date > CURRENT_DATE - INTERVAL '1 year'
GROUP BY month
ORDER BY month;
-- Add appropriate indexes to optimize queries:
CREATE INDEX idx_customer_id ON book_transactions (customer_id);
CREATE INDEX idx_book_id ON book_transactions (book_id);
CREATE INDEX idx_genre ON books (genre);
-- 	Analyze query execution plans for two queries:
EXPLAIN ANALYZE SELECT * FROM book_transactions WHERE return_date IS NULL;