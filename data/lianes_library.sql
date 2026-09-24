/*
TABLES:

books: isbn, tittle, author , genre, status, is_available

friends: friend_1d, friend_name, phone_number, email, max_loans, notes

loans: loan_id, isbn, friend_id, loan_date, retun_date, notes



*/

DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS friends;
DROP TABLE IF EXISTS books;
DROP SCHEMA IF EXISTS lianes_library;

CREATE SCHEMA IF NOT EXISTS lianes_library;
USE lianes_library;

-- BOOKS: extended with physical condition + mood tags
CREATE TABLE books (
    isbn           VARCHAR(13)  PRIMARY KEY,
    book_name      VARCHAR(150) NOT NULL,
    author         VARCHAR(100) NOT NULL,
    genre          VARCHAR(40),
    published_year YEAR,
    total_pages    SMALLINT UNSIGNED,
    book_condition ENUM('mint','good','worn','damaged') NOT NULL DEFAULT 'good',
    mood_tags      VARCHAR(200),
    cover_url      VARCHAR(500),
    is_available   BOOLEAN NOT NULL DEFAULT TRUE,
    date_added     DATE NOT NULL DEFAULT (CURRENT_DATE)
);

-- FRIENDS: with trust scoring and reading preferences
CREATE TABLE friends (
    friend_id       INT AUTO_INCREMENT PRIMARY KEY,
    friend_name     VARCHAR(80)  NOT NULL,
    phone_number    VARCHAR(20),
    email           VARCHAR(120) UNIQUE,
    max_loans       TINYINT UNSIGNED NOT NULL DEFAULT 3,
    trust_score     TINYINT UNSIGNED NOT NULL DEFAULT 100
                    CHECK (trust_score BETWEEN 0 AND 100),
    preferred_genres VARCHAR(200),     -- e.g. 'sci-fi,mystery'
    date_added      DATE NOT NULL DEFAULT (CURRENT_DATE),
    notes           TEXT
);

-- LOANS: with late fee tracking and return condition
CREATE TABLE loans (
    loan_id          INT AUTO_INCREMENT PRIMARY KEY,
    isbn             VARCHAR(13) NOT NULL,
    friend_id        INT         NOT NULL,
    loan_date        DATE        NOT NULL DEFAULT (CURRENT_DATE),
    due_date         DATE        NOT NULL,
    return_date      DATE,
    return_condition ENUM('mint','good','worn','damaged'),
    late_fee_owed    DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    notes            TEXT,

    FOREIGN KEY (isbn)      REFERENCES books(isbn),
    FOREIGN KEY (friend_id) REFERENCES friends(friend_id),

    CONSTRAINT no_duplicate_active UNIQUE (isbn, friend_id, loan_date)
);

-- READING SESSIONS: tracks reading progress (unique to your schema!)
CREATE TABLE reading_sessions (
    session_id    INT AUTO_INCREMENT PRIMARY KEY,
    loan_id       INT NOT NULL,
    session_date  DATE NOT NULL DEFAULT (CURRENT_DATE),
    pages_read    SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    mood_rating   TINYINT UNSIGNED CHECK (mood_rating BETWEEN 1 AND 5),
    session_notes TEXT,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);

-- WISHLIST: friends can request books Liane doesn't own yet
CREATE TABLE wishlist (
    wishlist_id   INT AUTO_INCREMENT PRIMARY KEY,
    friend_id     INT NOT NULL,
    book_title    VARCHAR(150) NOT NULL,
    author        VARCHAR(100),
    requested_on  DATE NOT NULL DEFAULT (CURRENT_DATE),
    fulfilled     BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (friend_id) REFERENCES friends(friend_id)
);

-- BOOK REVIEWS: friends leave ratings after returning
CREATE TABLE reviews (
    review_id     INT AUTO_INCREMENT PRIMARY KEY,
    loan_id       INT NOT NULL UNIQUE,   -- one review per loan
    rating        TINYINT UNSIGNED NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text   TEXT,
    reviewed_on   DATE NOT NULL DEFAULT (CURRENT_DATE),
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
);