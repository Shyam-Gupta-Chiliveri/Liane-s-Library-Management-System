USE lianes_library;
-- ============================================================
--  Insert books
-- ============================================================
INSERT INTO books (isbn, book_name, author, genre, published_year, total_pages, book_condition, mood_tags, is_available) VALUES
('9780141036144', 'To Kill a Mockingbird',             'Harper Lee',          'Fiction',    1960, 281, 'good',    'emotional,inspiring',   TRUE),
('9780743273565', 'The Great Gatsby',                  'F. Scott Fitzgerald', 'Fiction',    1925, 180, 'worn',    'dark,romantic',         TRUE),
('9780062316097', 'Sapiens',                           'Yuval Noah Harari',   'Non-Fiction',2011, 443, 'mint',    'educational,inspiring', TRUE),
('9780747532743', 'Harry Potter and the Philosophers Stone', 'J.K. Rowling', 'Fantasy',    1997, 223, 'good',    'magical,cosy',          TRUE),
('9781501156700', 'It Ends with Us',                   'Colleen Hoover',      'Romance',    2016, 384, 'mint',    'emotional,romantic',    TRUE),
('9780593311295', 'Atomic Habits',                     'James Clear',         'Self-Help',  2018, 320, 'good',    'inspiring,educational', TRUE),
('9780385490818', 'The Handmaids Tale',                'Margaret Atwood',     'Dystopian',  1985, 311, 'worn',    'dark,emotional',        TRUE),
('9780679720201', 'Crime and Punishment',              'Fyodor Dostoevsky',   'Classic',    1901, 545, 'damaged', 'dark,intense',          TRUE),
('9781250301697', 'The Midnight Library',              'Matt Haig',           'Fiction',    2020, 288, 'mint',    'emotional,cosy',        TRUE),
('9780525559474', 'The Subtle Art of Not Giving a F', 'Mark Manson',         'Self-Help',  2016, 224, 'good',    'inspiring,funny',       TRUE);

-- ============================================================
--  Insert friends
-- ============================================================
INSERT INTO friends (friend_name, phone_number, email, max_loans, trust_score, preferred_genres, notes) VALUES
('Emma Watson',   '07911123456', 'emma@email.com',   3, 100, 'Fiction,Fantasy',       'Very reliable, always returns on time'),
('James Brown',   '07922234567', 'james@email.com',  2, 75,  'Non-Fiction,Self-Help', 'Returned one book damaged'),
('Sophie Turner', '07933345678', 'sophie@email.com', 3, 90,  'Romance,Fiction',       'Sometimes a little late'),
('Liam Smith',    '07944456789', 'liam@email.com',   2, 60,  'Classic,Dystopian',     'Lost a book once, be careful'),
('Olivia Jones',  '07955567890', 'olivia@email.com', 3, 100, 'Self-Help,Fiction',     'Best borrower, never late');

-- ============================================================
--  Insert loans
-- ============================================================
INSERT INTO loans (isbn, friend_id, loan_date, due_date, renewal_date, notes) VALUES
('9780141036144', 1, '2024-08-01', '2024-08-15', '2024-08-22', 'First loan ever'),
('9780743273565', 2, '2024-08-05', '2024-08-19', NULL,         'Reminded once'),
('9780062316097', 3, '2024-08-10', '2024-08-24', '2024-08-31', 'Renewed once'),
('9780747532743', 4, '2024-08-12', '2024-08-26', NULL,         NULL),
('9781501156700', 5, '2024-08-15', '2024-08-29', '2024-09-05', 'Loves this book'),
('9780593311295', 1, '2024-08-20', '2024-09-03', NULL,         NULL),
('9780385490818', 2, '2024-08-22', '2024-09-05', NULL,         'Handle carefully'),
('9780679720201', 3, '2024-08-25', '2024-09-08', '2024-09-15', NULL),
('9781250301697', 4, '2024-09-01', '2024-09-15', NULL,         NULL),
('9780525559474', 5, '2024-09-05', '2024-09-19', '2024-09-26', NULL);

-- ============================================================
--  Insert reading sessions
-- ============================================================
INSERT INTO reading_sessions (loan_id, session_date, pages_read, mood_rating, session_notes) VALUES
(1,  '2024-08-02', 50,  5, 'Amazing start'),
(1,  '2024-08-05', 80,  5, 'Could not put it down'),
(2,  '2024-08-06', 30,  3, 'Slow start'),
(3,  '2024-08-11', 60,  4, 'Really enjoying it'),
(4,  '2024-08-13', 40,  3, 'Getting into it slowly'),
(5,  '2024-08-16', 100, 5, 'Finished in one sitting'),
(6,  '2024-08-21', 45,  4, 'Very practical book'),
(7,  '2024-08-23', 55,  4, 'Dark but gripping'),
(8,  '2024-08-26', 70,  5, 'Intense reading'),
(9,  '2024-09-02', 90,  5, 'Beautiful story');

-- ============================================================
--  Insert wishlist
-- ============================================================
INSERT INTO wishlist (friend_id, book_title, author, requested_on, fulfilled) VALUES
(1, 'The Alchemist',          'Paulo Coelho',    '2024-08-10', FALSE),
(2, 'Thinking Fast and Slow', 'Daniel Kahneman', '2024-08-12', FALSE),
(3, 'Pride and Prejudice',    'Jane Austen',     '2024-08-15', FALSE),
(4, '1984',                   'George Orwell',   '2024-08-18', FALSE),
(5, 'The Power of Now',       'Eckhart Tolle',   '2024-08-20', FALSE);

-- ============================================================
--  Insert reviews
-- ============================================================
INSERT INTO reviews (loan_id, rating, review_text, reviewed_on) VALUES
(1, 5, 'Absolutely loved it, a masterpiece',       '2024-08-20'),
(2, 3, 'Good but found it slow in the middle',     '2024-08-25'),
(3, 5, 'Changed the way I think about everything', '2024-08-30'),
(4, 4, 'Magical and fun, great read',              '2024-09-01'),
(5, 5, 'Cried three times, brilliant book',        '2024-09-06');

-- ============================================================
--  Verify everything
-- ============================================================
SELECT * FROM books;
SELECT * FROM friends;
SELECT * FROM loans;
SELECT * FROM reading_sessions;
SELECT * FROM wishlist;
SELECT * FROM reviews;
SELECT loan_id, tracker_id, isbn, friend_id FROM loans;


