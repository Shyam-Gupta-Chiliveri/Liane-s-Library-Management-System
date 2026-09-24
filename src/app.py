import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import date, timedelta

# ── Connection ────────────────────────────────────────────────────────────────
load_dotenv(override=True)

schema   = "lianes_library"
host = os.getenv("MYSQL_HOST", "db")
user     = "root"
password = os.getenv("MYSQL_PASSWORD")
port     = 3306

connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
engine = create_engine(connection_string)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Liane's Library",
    page_icon="📚",
    layout="wide"
)

# ── Helper functions ──────────────────────────────────────────────────────────
def run_query(sql):
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)

def run_write(sql):
    with engine.begin() as conn:
        conn.execute(text(sql))

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
if "login" not in st.session_state:
    st.session_state["login"] = "notloggedin"

if st.session_state["login"] == "notloggedin":

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0500 0%, #2b1000 40%, #6b3010 75%, #b07030 100%);
        min-height: 100vh;
    }
    [data-testid="stHeader"]  { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    /* Outer flex wrapper */
    .login-outer {
        display: flex;
        min-height: 100vh;
        width: 100%;
        align-items: stretch;
    }
    /* LEFT side */
    .login-left {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 48px 52px 52px 52px;
    }
    .ll-brand {
        display: flex; align-items: center; gap: 14px;
    }
    .ll-brand-icon { font-size: 2.4rem; }
    .ll-brand-name {
        font-size: 1.3rem; font-weight: 800;
        color: #fff; margin: 0; letter-spacing: -0.3px;
    }
    .ll-brand-tag {
        font-size: 0.68rem; color: rgba(255,255,255,0.35);
        text-transform: uppercase; letter-spacing: 1.5px; margin: 3px 0 0 0;
    }
    .ll-middle { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 60px 0 40px 0; }
    .ll-quote-mark {
        font-size: 7rem; line-height: 0.6; color: rgba(200,145,74,0.4);
        font-family: Georgia, serif; margin-bottom: 16px; display: block;
    }
    .ll-quote {
        font-size: 2rem; font-weight: 700; color: #fff;
        line-height: 1.4; margin: 0 0 20px 0; letter-spacing: -0.4px;
        max-width: 520px;
    }
    .ll-author {
        font-size: 0.9rem; color: rgba(255,255,255,0.4); font-style: italic;
    }
    .ll-dots { display: flex; gap: 8px; margin-top: 36px; }
    .ll-dot-on  { width: 28px; height: 7px; border-radius: 4px; background: #c8914a; }
    .ll-dot-off { width: 8px;  height: 7px; border-radius: 4px; background: rgba(255,255,255,0.2); }
    .ll-bottom {}
    .ll-features {
        display: flex; gap: 0; 
        border-top: 1px solid rgba(255,255,255,0.08); padding-top: 32px;
    }
    .ll-feat {
        flex: 1; text-align: center;
        border-right: 1px solid rgba(255,255,255,0.08);
        padding: 0 16px;
    }
    .ll-feat:last-child { border-right: none; }
    .ll-feat-icon  { font-size: 1.8rem; display: block; margin-bottom: 6px; }
    .ll-feat-label {
        font-size: 0.68rem; color: rgba(255,255,255,0.35);
        text-transform: uppercase; letter-spacing: 1px;
    }
    /* RIGHT side */
    .login-right {
        width: 440px;
        min-width: 400px;
        background: #fff;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 64px 56px;
        box-shadow: -20px 0 60px rgba(0,0,0,0.25);
    }
    .lr-eyebrow {
        font-size: 0.72rem; font-weight: 800; color: #c8914a;
        letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 12px;
    }
    .lr-title {
        font-size: 2.1rem; font-weight: 900; color: #1a0a00;
        margin: 0 0 10px 0; letter-spacing: -0.5px; line-height: 1.2;
    }
    .lr-sub {
        font-size: 0.92rem; color: #9a8070; margin-bottom: 36px;
    }
    .lr-line {
        height: 1px; background: #f0e8e0; margin-bottom: 32px;
    }
    div[data-testid="stTextInput"] label {
        color: #4a3728 !important; font-size: 0.73rem !important;
        font-weight: 800 !important; letter-spacing: 1.2px !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stTextInput"] input {
        background: #faf7f4 !important;
        border: 1.5px solid #e8ddd4 !important;
        border-radius: 10px !important; color: #1a0a00 !important;
        font-size: 0.98rem !important; padding: 13px 16px !important;
        transition: all 0.2s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #c8914a !important;
        background: #fff !important;
        box-shadow: 0 0 0 4px rgba(200,145,74,0.1) !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: #c0b0a0 !important; }
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #b87830 0%, #e0a848 100%) !important;
        color: #fff !important; font-weight: 800 !important;
        font-size: 0.98rem !important; border: none !important;
        border-radius: 10px !important; padding: 14px !important;
        width: 100% !important; letter-spacing: 0.3px !important;
        box-shadow: 0 6px 20px rgba(184,120,48,0.3) !important;
        transition: all 0.25s !important; margin-top: 8px !important;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(184,120,48,0.4) !important;
    }
    div[data-testid="stAlert"] { border-radius: 10px !important; margin-top: 14px !important; }
    .lr-footer {
        margin-top: 32px; font-size: 0.73rem; color: #c0b0a0; text-align: center;
    }
    </style>

    <div class="login-outer">
        <div class="login-left">
            <div class="ll-brand">
                <span class="ll-brand-icon">📚</span>
                <div>
                    <p class="ll-brand-name">Liane's Library</p>
                    <p class="ll-brand-tag">Book Management System</p>
                </div>
            </div>
            <div class="ll-middle">
                <span class="ll-quote-mark">"</span>
                <p class="ll-quote">A room without books is like a body without a soul.</p>
                <p class="ll-author">— Marcus Tullius Cicero</p>
                <div class="ll-dots">
                    <div class="ll-dot-on"></div>
                    <div class="ll-dot-off"></div>
                    <div class="ll-dot-off"></div>
                </div>
            </div>
            <div class="ll-bottom">
                <div class="ll-features">
                    <div class="ll-feat">
                        <span class="ll-feat-icon">📖</span>
                        <div class="ll-feat-label">Track Books</div>
                    </div>
                    <div class="ll-feat">
                        <span class="ll-feat-icon">👥</span>
                        <div class="ll-feat-label">Friends</div>
                    </div>
                    <div class="ll-feat">
                        <span class="ll-feat-icon">📋</span>
                        <div class="ll-feat-label">Loans</div>
                    </div>
                    <div class="ll-feat">
                        <span class="ll-feat-icon">⭐</span>
                        <div class="ll-feat-label">Reviews</div>
                    </div>
                    <div class="ll-feat">
                        <span class="ll-feat-icon">🎁</span>
                        <div class="ll-feat-label">Wishlist</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Right panel using Streamlit column positioned absolutely on the right
    _, right = st.columns([1, 0.52])
    with right:
        st.markdown("""
        <style>
        /* Pull the right column up flush with top */
        [data-testid="stHorizontalBlock"] {
            margin-top: -100vh !important;
            align-items: center !important;
            min-height: 100vh !important;
        }
        [data-testid="stHorizontalBlock"] > div:last-child {
            background: #fff;
            min-height: 100vh;
            padding: 64px 48px !important;
            box-shadow: -20px 0 60px rgba(0,0,0,0.25);
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        </style>
        <p class="lr-eyebrow">Welcome back</p>
        <h1 class="lr-title">Sign in to<br>your library</h1>
        <p class="lr-sub">Enter your credentials to continue</p>
        <div class="lr-line"></div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username  = st.text_input("Username", placeholder="e.g. liane")
            pwd       = st.text_input("Password", type="password", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            login_btn = st.form_submit_button("Sign In  →", use_container_width=True)

        if login_btn:
            correct_user = os.getenv("LIBRARY_USERNAME", "liane")
            correct_pass = os.getenv("LIBRARY_PASSWORD", "liane123")
            if not username:
                st.error("Please enter your username.")
            elif not pwd:
                st.error("Please enter your password.")
            elif username == correct_user and pwd == correct_pass:
                st.session_state["login"] = "loggedin"
                st.rerun()
            else:
                st.error("Incorrect username or password. Try again.")

        st.markdown("""
        <div class="lr-footer">
            Liane's Library &nbsp;·&nbsp; Built with ❤️ &nbsp;·&nbsp; v1.0
        </div>
        """, unsafe_allow_html=True)


elif st.session_state["login"] == "loggedin":

    # Fix is_available for all books based on active loans
    try:
        run_write("""
            UPDATE books b
            SET b.is_available = CASE
                WHEN EXISTS (
                    SELECT 1 FROM loans l
                    WHERE l.isbn = b.isbn AND l.return_date IS NULL
                ) THEN FALSE
                ELSE TRUE
            END
        """)
    except Exception:
        pass

    # ── Sidebar navigation ────────────────────────────────────────────────────
    st.sidebar.markdown("## 📚 Liane's Library")
    st.sidebar.markdown("---")

    page = st.sidebar.radio("Navigate", [
        "📊 Dashboard",
        "📖 Books",
        "👥 Friends",
        "📋 Active Loans",
        "➕ Lend a Book",
        "📬 Return a Book",
        "🔍 Track a Loan",
        "🔄 Renew a Loan",
        "⭐ Leave a Review",
        "🎁 Wishlist",
    ])

    st.sidebar.markdown("---")
    st.sidebar.caption("Liane's Personal Library System")
    if st.sidebar.button("🚪 Logout"):
        st.session_state["login"] = "notloggedin"
        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — DASHBOARD
    # ══════════════════════════════════════════════════════════════════════════
    if page == "📊 Dashboard":
        st.title("📊 Library Dashboard")
        st.markdown("Welcome back, Liane! Here's what's happening in your library.")
        st.markdown("---")

        summary = run_query("""
            SELECT
                (SELECT COUNT(*) FROM books)                              AS total_books,
                (SELECT COUNT(*) FROM books WHERE is_available = 1)      AS available,
                (SELECT COUNT(*) FROM friends)                           AS total_friends,
                (SELECT COUNT(*) FROM loans WHERE return_date IS NULL)   AS active_loans,
                (SELECT COUNT(*) FROM loans
                 WHERE return_date IS NULL
                 AND CURDATE() > COALESCE(renewal_date, due_date))       AS overdue,
                (SELECT COALESCE(SUM(
                    CASE
                        WHEN return_date IS NULL
                        AND CURDATE() > COALESCE(renewal_date, due_date)
                        THEN ROUND(DATEDIFF(CURDATE(), COALESCE(renewal_date, due_date)) * 0.50, 2)
                        WHEN fine_status = 'unpaid' AND return_date IS NOT NULL
                        THEN fine_amount
                        ELSE 0
                    END
                ), 0) FROM loans)                                        AS unpaid_fines,
                (SELECT COUNT(*) FROM wishlist WHERE fulfilled = 0)      AS wishlist_pending
        """).iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Books",    int(summary["total_books"]))
            st.metric("Available",      int(summary["available"]))
        with c2:
            st.metric("Friends",        int(summary["total_friends"]))
            st.metric("Active Loans",   int(summary["active_loans"]))
        with c3:
            st.metric("Overdue",        int(summary["overdue"]))
            st.metric("Wishlist",       int(summary["wishlist_pending"]))
        with c4:
            st.metric("Unpaid Fines",  f"£{float(summary['unpaid_fines']):.2f}")

        st.markdown("---")
        st.subheader("Recent Loans")
        recent = run_query("""
            SELECT
                l.tracker_id,
                f.friend_name,
                b.book_name,
                l.loan_date,
                l.due_date,
                CASE
                    WHEN l.return_date IS NOT NULL                         THEN 'Returned'
                    WHEN CURDATE() > COALESCE(l.renewal_date, l.due_date) THEN 'OVERDUE'
                    WHEN l.renewal_date IS NOT NULL                        THEN 'Renewed'
                    ELSE 'Active'
                END AS status
            FROM loans l
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            ORDER BY l.loan_id DESC
            LIMIT 8
        """)
        st.dataframe(recent, use_container_width=True, hide_index=True)

        overdue = run_query("""
            SELECT
                l.tracker_id,
                f.friend_name,
                f.phone_number,
                b.book_name,
                DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) AS days_overdue,
                ROUND(DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) * 0.50, 2) AS fine_due
            FROM loans l
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            WHERE l.return_date IS NULL
            AND CURDATE() > COALESCE(l.renewal_date, l.due_date)
            ORDER BY days_overdue DESC
        """)
        if not overdue.empty:
            st.markdown("---")
            st.subheader("🚨 Overdue Books")
            st.dataframe(overdue, use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — BOOKS
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📖 Books":
        st.title("📖 Book Collection")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            availability = st.selectbox("Availability", ["All Books", "Available Only", "On Loan"])
        with col2:
            genres = run_query("SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL ORDER BY genre")
            genre_list = ["All Genres"] + genres["genre"].tolist()
            genre_filter = st.selectbox("Genre", genre_list)
        with col3:
            mood_filter = st.text_input("Mood Tag", placeholder="e.g. cosy, dark, inspiring")

        where = []
        if availability == "Available Only":
            where.append("b.is_available = 1")
        elif availability == "On Loan":
            where.append("b.is_available = 0")
        if genre_filter != "All Genres":
            where.append(f"b.genre = '{genre_filter}'")
        if mood_filter:
            where.append(f"b.mood_tags LIKE '%{mood_filter}%'")

        where_clause = "WHERE " + " AND ".join(where) if where else ""

        books = run_query(f"""
            SELECT
                b.isbn,
                b.book_name,
                b.author,
                b.genre,
                b.published_year,
                b.total_pages,
                b.book_condition AS book_condition,
                b.mood_tags,
                b.is_available
            FROM books b
            {where_clause}
            ORDER BY b.book_name
        """)

        books["status"] = books["is_available"].apply(lambda x: "Available" if x == 1 else "On Loan")
        books = books.drop(columns=["is_available"])

        st.markdown(f"**{len(books)} book(s) found**")
        st.dataframe(books, use_container_width=True, hide_index=True)

        # ── Add a book ────────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("➕ Add a New Book")
        with st.expander("Click to add a book"):
            with st.form("add_book_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_isbn      = st.text_input("ISBN (10 or 13 digits)")
                    new_title     = st.text_input("Book Title")
                    new_author    = st.text_input("Author")
                    new_genre     = st.text_input("Genre")
                with c2:
                    new_year      = st.number_input("Published Year", min_value=1901, max_value=2026, value=2020)
                    new_pages     = st.number_input("Total Pages", min_value=1, value=200)
                    new_condition = st.selectbox("Condition", ["mint", "good", "worn", "damaged"])
                    new_mood      = st.text_input("Mood Tags", placeholder="e.g. cosy,dark,inspiring")

                submitted = st.form_submit_button("Add Book")
                if submitted:
                    if not new_isbn or not new_title or not new_author:
                        st.warning("ISBN, Title and Author are required.")
                    elif len(new_isbn) not in (10, 13) or not new_isbn.isnumeric():
                        st.warning("ISBN must be 10 or 13 numbers only.")
                    else:
                        existing = run_query(f"SELECT isbn FROM books WHERE isbn = '{new_isbn}'")
                        if not existing.empty:
                            st.warning("This ISBN already exists in the library.")
                        else:
                            run_write(f"""
                                INSERT INTO books (isbn, book_name, author, genre, published_year,
                                                   total_pages, book_condition, mood_tags, is_available)
                                VALUES ('{new_isbn}', '{new_title}', '{new_author}', '{new_genre}',
                                        {new_year}, {new_pages}, '{new_condition}', '{new_mood}', TRUE)
                            """)
                            st.session_state["book_added"] = new_title
                            st.rerun()

        if "book_added" in st.session_state:
            st.success(f"✅ '{st.session_state['book_added']}' has been added to the library!")
            del st.session_state["book_added"]

        # ── Update a book ─────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("✏️ Update a Book")
        with st.expander("Click to update a book"):
            book_field_map = {
                "Title"         : "book_name",
                "Author"        : "author",
                "Genre"         : "genre",
                "Condition"     : "book_condition",
                "Mood Tags"     : "mood_tags",
                "Published Year": "published_year",
                "Total Pages"   : "total_pages",
            }
            st.markdown("**Step 1 — Select the book you want to update**")
            all_books_raw = run_query("""
                SELECT isbn, book_name, author, genre, published_year,
                       total_pages, book_condition, mood_tags, is_available
                FROM books ORDER BY book_name
            """)
            all_books_display = all_books_raw.drop(columns=["is_available"]).fillna("")
            upd_book_df = st.dataframe(
                all_books_display,
                selection_mode="single-row", on_select="rerun",
                key="update_book_df", use_container_width=True
            )
            if len(upd_book_df.selection["rows"]) > 0:
                upd_book = all_books_raw.iloc[upd_book_df.selection["rows"][0]]
                st.success(f"Selected: **{upd_book['book_name']}** by {upd_book['author']}")

                st.markdown("**Step 2 — Choose what to update**")
                book_label = st.selectbox(
                    "Field to update", list(book_field_map.keys()),
                    key="book_field_label", index=None
                )
                if book_label:
                    db_field    = book_field_map[book_label]
                    current_val = str(upd_book[db_field]) if upd_book[db_field] is not None else ""
                    st.caption(f"Current value: **{current_val}**")

                    if book_label == "Condition":
                        new_val = st.selectbox(
                            "New Condition", ["mint","good","worn","damaged"],
                            key=f"upd_book_{upd_book['isbn']}_{db_field}"
                        )
                    else:
                        new_val = st.text_input(
                            f"New {book_label}", value="", placeholder=current_val,
                            key=f"upd_book_{upd_book['isbn']}_{db_field}"
                        )

                    if st.button("Update Book", key="update_book_btn"):
                        val_to_save = new_val.strip() if isinstance(new_val, str) else str(new_val)
                        if not val_to_save:
                            st.warning("Please enter a new value.")
                        else:
                            run_write(f"UPDATE books SET {db_field} = '{val_to_save}' WHERE isbn = '{upd_book['isbn']}'")
                            st.session_state["book_updated"] = f"{book_label} updated to '{val_to_save}' for '{upd_book['book_name']}'."
                            st.rerun()

        if "book_updated" in st.session_state:
            st.success(f"✅ {st.session_state['book_updated']}")
            del st.session_state["book_updated"]

        # ── Remove a book ─────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("🗑️ Remove a Book")
        with st.expander("Click to remove a book"):
            st.warning("⚠️ A book cannot be removed if it is currently on loan.")
            del_books_raw = run_query("""
                SELECT isbn, book_name, author, genre,
                       book_condition, is_available
                FROM books ORDER BY book_name
            """)
            del_books_display = del_books_raw.copy().fillna("")
            del_book_df = st.dataframe(
                del_books_display,
                selection_mode="single-row", on_select="rerun",
                key="delete_book_df", use_container_width=True
            )
            if len(del_book_df.selection["rows"]) > 0:
                del_book = del_books_raw.iloc[del_book_df.selection["rows"][0]]
                st.error(f"You are about to remove: **{del_book['book_name']}** by {del_book['author']}")

                # Check if on active loan
                on_loan = run_query(f"SELECT loan_id FROM loans WHERE isbn = '{del_book['isbn']}' AND return_date IS NULL")
                if not on_loan.empty:
                    st.warning(f"Cannot remove — this book is currently on loan. Ask for it to be returned first.")
                else:
                    confirm = st.checkbox(f"I confirm I want to permanently delete '{del_book['book_name']}'", key="confirm_del_book")
                    if confirm:
                        if st.button("🗑️ Delete Book", key="delete_book_btn"):
                            run_write(f"DELETE FROM books WHERE isbn = '{del_book['isbn']}'")
                            st.session_state["book_deleted"] = f"'{del_book['book_name']}' has been removed from the library."
                            st.rerun()

        if "book_deleted" in st.session_state:
            st.success(f"✅ {st.session_state['book_deleted']}")
            del st.session_state["book_deleted"]

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — FRIENDS
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "👥 Friends":
        st.title("👥 Friends & Borrowers")
        st.markdown("---")

        min_trust = st.slider("Minimum Trust Score", 0, 100, 0)

        friends = run_query(f"""
            SELECT
                f.friend_id,
                f.friend_name,
                f.phone_number,
                f.email,
                f.max_loans,
                f.trust_score,
                f.preferred_genres,
                COUNT(l.loan_id)               AS total_loans,
                SUM(l.return_date IS NULL)     AS currently_holding,
                COALESCE(SUM(
                    CASE
                        WHEN l.return_date IS NULL
                        AND CURDATE() > COALESCE(l.renewal_date, l.due_date)
                        THEN ROUND(DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) * 0.50, 2)
                        WHEN l.fine_status = 'unpaid' AND l.return_date IS NOT NULL
                        THEN l.fine_amount
                        ELSE 0
                    END
                ), 0)                              AS total_fines,
                f.notes
            FROM friends f
            LEFT JOIN loans l ON f.friend_id = l.friend_id
            WHERE f.trust_score >= {min_trust}
            GROUP BY f.friend_id, f.friend_name, f.phone_number, f.email,
                     f.max_loans, f.trust_score, f.preferred_genres, f.notes
            ORDER BY f.trust_score DESC
        """)

        st.markdown(f"**{len(friends)} friend(s) found**")
        st.dataframe(friends, use_container_width=True, hide_index=True)

        # ── Add a friend ──────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("➕ Add a New Friend")
        with st.expander("Click to add a friend"):
            with st.form("add_friend_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_name   = st.text_input("Full Name")
                    new_phone  = st.text_input("Phone Number")
                    new_email  = st.text_input("Email")
                with c2:
                    new_max    = st.number_input("Max Loans Allowed", min_value=1, max_value=10, value=3)
                    new_genres = st.text_input("Preferred Genres", placeholder="Fiction, Romance")
                    new_notes  = st.text_area("Notes")

                submitted = st.form_submit_button("Add Friend")
                if submitted:
                    if not new_name:
                        st.warning("Name is required.")
                    elif not new_email or "@" not in new_email:
                        st.warning("Valid email is required.")
                    else:
                        existing = run_query(f"SELECT email FROM friends WHERE email = '{new_email}'")
                        if not existing.empty:
                            st.warning("This email is already registered.")
                        else:
                            run_write(f"""
                                INSERT INTO friends (friend_name, phone_number, email,
                                                     max_loans, trust_score, preferred_genres, notes)
                                VALUES ('{new_name}', '{new_phone}', '{new_email}',
                                        {new_max}, 100, '{new_genres}', '{new_notes}')
                            """)
                            st.session_state["friend_added"] = new_name
                            st.rerun()

        if "friend_added" in st.session_state:
            st.success(f"✅ '{st.session_state['friend_added']}' has been added as a borrower!")
            del st.session_state["friend_added"]

        # ── Update a friend ───────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("✏️ Update a Friend")
        with st.expander("Click to update a friend"):
            friend_field_map = {
                "Name"            : "friend_name",
                "Phone Number"    : "phone_number",
                "Email"           : "email",
                "Max Loans"       : "max_loans",
                "Preferred Genres": "preferred_genres",
                "Notes"           : "notes"
            }
            st.markdown("**Step 1 — Select the friend**")
            all_friends_raw = run_query("SELECT * FROM friends ORDER BY friend_name")
            all_friends_display = all_friends_raw.copy().fillna("")
            upd_friend_df = st.dataframe(
                all_friends_display,
                selection_mode="single-row", on_select="rerun",
                key="update_friend_df", use_container_width=True
            )
            if len(upd_friend_df.selection["rows"]) > 0:
                upd_friend = all_friends_raw.iloc[upd_friend_df.selection["rows"][0]]
                st.success(f"Selected: **{upd_friend['friend_name']}** — {upd_friend['email']}")

                st.markdown("**Step 2 — Choose what to update**")
                friend_label = st.selectbox(
                    "Field to update", list(friend_field_map.keys()),
                    key="friend_field_label", index=None
                )
                if friend_label:
                    db_field    = friend_field_map[friend_label]
                    current_val = str(upd_friend[db_field]) if upd_friend[db_field] is not None else ""
                    st.caption(f"Current value: **{current_val}**")
                    new_val = st.text_input(
                        f"New {friend_label}", value="", placeholder=current_val,
                        key=f"upd_friend_{upd_friend['friend_id']}_{db_field}"
                    )
                    if st.button("Update Friend", key="update_friend_btn"):
                        val_to_save = new_val.strip()
                        if not val_to_save:
                            st.warning("Please type a new value.")
                        elif db_field == "email" and "@" not in val_to_save:
                            st.warning("Please enter a valid email address.")
                        else:
                            run_write(f"UPDATE friends SET {db_field} = '{val_to_save}' WHERE friend_id = {upd_friend['friend_id']}")
                            st.session_state["friend_updated"] = f"{friend_label} updated to '{val_to_save}' for '{upd_friend['friend_name']}'."
                            st.rerun()

        if "friend_updated" in st.session_state:
            st.success(f"✅ {st.session_state['friend_updated']}")
            del st.session_state["friend_updated"]

        # ── Lower trust score ─────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("⚠️ Lower Trust Score")
        with st.expander("Click to lower a friend's trust score"):
            trust_raw = run_query("SELECT * FROM friends ORDER BY friend_name")
            trust_df  = st.dataframe(
                trust_raw.fillna(""),
                selection_mode="single-row", on_select="rerun",
                key="trust_friend_df", use_container_width=True
            )
            if len(trust_df.selection["rows"]) > 0:
                trust_friend = trust_raw.iloc[trust_df.selection["rows"][0]]
                st.info(f"Selected: **{trust_friend['friend_name']}** — Current score: {trust_friend['trust_score']}")
                points = st.slider("Points to deduct", 5, 50, 10, key="trust_points")
                reason = st.text_input("Reason (optional)", key="trust_reason")
                if st.button("Lower Trust Score", key="lower_trust_btn"):
                    run_write(f"""
                        UPDATE friends
                        SET trust_score = GREATEST(0, trust_score - {points})
                        WHERE friend_id = {trust_friend['friend_id']}
                    """)
                    st.success(f"Trust score for '{trust_friend['friend_name']}' reduced by {points} points.")
                    st.rerun()

        # ── Remove a friend ───────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("🗑️ Remove a Friend")
        with st.expander("Click to remove a friend"):
            st.warning("⚠️ Removing a friend will also delete ALL their loans, reviews and wishlist entries.")
            del_friends_raw = run_query("SELECT * FROM friends ORDER BY friend_name")
            del_friend_df   = st.dataframe(
                del_friends_raw.fillna(""),
                selection_mode="single-row", on_select="rerun",
                key="delete_friend_df", use_container_width=True
            )
            if len(del_friend_df.selection["rows"]) > 0:
                del_friend = del_friends_raw.iloc[del_friend_df.selection["rows"][0]]

                # Show their current loans count
                active_loans = run_query(f"SELECT loan_id FROM loans WHERE friend_id = {del_friend['friend_id']} AND return_date IS NULL")
                total_loans  = run_query(f"SELECT loan_id FROM loans WHERE friend_id = {del_friend['friend_id']}")

                st.error(f"You are about to remove: **{del_friend['friend_name']}** ({del_friend['email']})")
                c1, c2 = st.columns(2)
                c1.metric("Active Loans",  len(active_loans))
                c2.metric("Total Loans",   len(total_loans))

                if len(active_loans) > 0:
                    st.warning(f"This friend still has {len(active_loans)} active loan(s). Return them first before removing.")
                else:
                    confirm = st.checkbox(
                        f"I confirm I want to permanently delete '{del_friend['friend_name']}' and all their history",
                        key="confirm_del_friend"
                    )
                    if confirm:
                        if st.button("🗑️ Delete Friend", key="delete_friend_btn"):
                            fid   = del_friend["friend_id"]
                            loans = run_query(f"SELECT loan_id FROM loans WHERE friend_id = {fid}")
                            with engine.begin() as conn:
                                for lid in loans["loan_id"]:
                                    conn.execute(text(f"DELETE FROM reviews WHERE loan_id = {lid}"))
                                conn.execute(text(f"DELETE FROM loans    WHERE friend_id = {fid}"))
                                conn.execute(text(f"DELETE FROM wishlist WHERE friend_id = {fid}"))
                                conn.execute(text(f"DELETE FROM friends  WHERE friend_id = {fid}"))
                            st.session_state["friend_deleted"] = f"'{del_friend['friend_name']}' and all their data removed."
                            st.rerun()

        if "friend_deleted" in st.session_state:
            st.success(f"✅ {st.session_state['friend_deleted']}")
            del st.session_state["friend_deleted"]

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 — ACTIVE LOANS
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📋 Active Loans":
        st.title("📋 Active Loans")
        st.markdown("---")

        loans = run_query("""
            SELECT
                l.tracker_id,
                f.friend_name,
                f.phone_number,
                b.book_name,
                l.loan_date,
                l.due_date,
                l.renewal_date,
                DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) AS days_overdue,
                CASE
                    WHEN DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) > 0
                    THEN ROUND(DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) * 0.50, 2)
                    ELSE 0
                END AS fine_accrued,
                CASE
                    WHEN DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) > 0
                    THEN 'UNPAID'
                    ELSE 'none'
                END AS fine_status
            FROM loans l
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            WHERE l.return_date IS NULL
            ORDER BY l.due_date ASC
        """)

        if loans.empty:
            st.info("No active loans right now!")
        else:
            loans["status"] = loans["days_overdue"].apply(lambda x: "OVERDUE" if x > 0 else "Active")
            overdue_count   = len(loans[loans["days_overdue"] > 0])
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Active", len(loans))
            c2.metric("Overdue",      overdue_count)
            c3.metric("On Time",      len(loans) - overdue_count)
            st.markdown("---")
            st.dataframe(loans, use_container_width=True, hide_index=True)

        # ── Update a loan ─────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("✏️ Update a Loan")
        with st.expander("Click to update a loan"):

            loan_field_map = {
                "Due Date"    : "due_date",
                "Renewal Date": "renewal_date",
                "Notes"       : "notes",
            }

            st.markdown("**Step 1 — Select the loan you want to update**")
            upd_loans_raw = run_query("""
                SELECT
                    l.loan_id,
                    l.tracker_id,
                    f.friend_name,
                    b.book_name,
                    l.loan_date,
                    l.due_date,
                    l.renewal_date,
                    l.notes
                FROM loans l
                JOIN books   b ON l.isbn      = b.isbn
                JOIN friends f ON l.friend_id = f.friend_id
                WHERE l.return_date IS NULL
                ORDER BY l.due_date ASC
            """)

            if upd_loans_raw.empty:
                st.info("No active loans to update.")
            else:
                upd_loan_df = st.dataframe(
                    upd_loans_raw.fillna(""),
                    selection_mode="single-row", on_select="rerun",
                    key="update_loan_df", use_container_width=True
                )

                if len(upd_loan_df.selection["rows"]) > 0:
                    upd_loan = upd_loans_raw.iloc[upd_loan_df.selection["rows"][0]]
                    st.success(f"Selected: **{upd_loan['tracker_id']}** — {upd_loan['friend_name']} — {upd_loan['book_name']}")

                    st.markdown("**Step 2 — Choose what to update**")
                    loan_label = st.selectbox(
                        "Field to update",
                        list(loan_field_map.keys()),
                        key="loan_field_label", index=None
                    )

                    if loan_label:
                        db_field    = loan_field_map[loan_label]
                        current_val = str(upd_loan[db_field]) if upd_loan[db_field] is not None else ""
                        st.caption(f"Current value: **{current_val}**")

                        if loan_label in ("Due Date", "Renewal Date"):
                            new_date = st.date_input(
                                f"New {loan_label}",
                                key=f"upd_loan_{upd_loan['loan_id']}_{db_field}"
                            )
                            if st.button("Update Loan", key="update_loan_btn"):
                                run_write(f"""
                                    UPDATE loans SET {db_field} = '{new_date}'
                                    WHERE loan_id = {upd_loan['loan_id']}
                                """)
                                st.session_state["loan_updated"] = f"{loan_label} updated to '{new_date}' for {upd_loan['tracker_id']}."
                                st.rerun()
                        else:
                            new_val = st.text_input(
                                f"New {loan_label}", value="", placeholder=current_val,
                                key=f"upd_loan_{upd_loan['loan_id']}_{db_field}"
                            )
                            if st.button("Update Loan", key="update_loan_btn"):
                                val_to_save = new_val.strip().replace("'", "")
                                if not val_to_save:
                                    st.warning("Please enter a new value.")
                                else:
                                    run_write(f"""
                                        UPDATE loans SET {db_field} = '{val_to_save}'
                                        WHERE loan_id = {upd_loan['loan_id']}
                                    """)
                                    st.session_state["loan_updated"] = f"{loan_label} updated for {upd_loan['tracker_id']}."
                                    st.rerun()

        if "loan_updated" in st.session_state:
            st.success(f"✅ {st.session_state['loan_updated']}")
            del st.session_state["loan_updated"]

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5 — LEND A BOOK
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "➕ Lend a Book":
        st.title("➕ Lend a Book")
        st.markdown("---")

        available_books = run_query("""
            SELECT isbn, book_name, author FROM books
            WHERE is_available = 1
            ORDER BY book_name
        """)
        friends = run_query(
            "SELECT friend_id, friend_name, trust_score, max_loans FROM friends ORDER BY friend_name"
        )

        if available_books.empty:
            st.warning("No books are currently available to lend!")
        else:
            with st.form("lend_form"):
                c1, c2 = st.columns(2)
                with c1:
                    book_options   = {f"{r['book_name']} ({r['author']})": r['isbn']
                                      for _, r in available_books.iterrows()}
                    selected_book  = st.selectbox("Select Book", list(book_options.keys()))
                with c2:
                    friend_options  = {f"{r['friend_name']} (Trust: {r['trust_score']})": r['friend_id']
                                       for _, r in friends.iterrows()}
                    selected_friend = st.selectbox("Select Friend", list(friend_options.keys()))

                due_days  = st.slider("Loan Duration (days)", 7, 60, 14)
                loan_note = st.text_input("Notes (optional)")
                submitted = st.form_submit_button("Record Loan")

                if submitted:
                    isbn      = book_options[selected_book]
                    friend_id = friend_options[selected_friend]
                    friend    = friends[friends['friend_id'] == friend_id].iloc[0]

                    active_loans = run_query(
                        f"SELECT loan_id FROM loans WHERE friend_id = {friend_id} AND return_date IS NULL"
                    )
                    if len(active_loans) >= friend['max_loans']:
                        st.warning(f"{friend['friend_name']} has reached their max loan limit ({friend['max_loans']}).")
                    elif friend['trust_score'] < 50:
                        st.warning(f"{friend['friend_name']} has a low trust score ({friend['trust_score']}). Lend with caution!")
                    else:
                        due_date     = date.today() + timedelta(days=due_days)
                        renewal_date = due_date + timedelta(days=7)
                        safe_note    = loan_note.replace("'", "")
                        run_write(f"""
                            INSERT INTO loans (isbn, friend_id, loan_date, due_date, renewal_date, notes)
                            VALUES ('{isbn}', {friend_id}, CURDATE(), '{due_date}', '{renewal_date}', '{safe_note}')
                        """)
                        # Mark book as unavailable
                        run_write(f"UPDATE books SET is_available = FALSE WHERE isbn = '{isbn}'")
                        st.session_state["loan_added"] = f"Loan recorded! '{selected_book.split(' (')[0]}' is due back by {due_date}."
                        st.rerun()

        if "loan_added" in st.session_state:
            st.success(f"✅ {st.session_state['loan_added']}")
            del st.session_state["loan_added"]

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6 — RETURN A BOOK
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "📬 Return a Book":
        st.title("📬 Return a Book")
        st.markdown("---")

        active_loans = run_query("""
            SELECT
                l.tracker_id,
                f.friend_name,
                b.book_name,
                l.loan_date,
                l.due_date,
                DATEDIFF(CURDATE(), COALESCE(l.renewal_date, l.due_date)) AS days_overdue
            FROM loans l
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            WHERE l.return_date IS NULL
            ORDER BY l.due_date ASC
        """)

        if active_loans.empty:
            st.info("No books are currently out on loan!")
        else:
            active_loans["status"] = active_loans["days_overdue"].apply(
                lambda x: f"OVERDUE by {x} days" if x > 0 else "On time"
            )
            loan_options = {
                f"{r['tracker_id']} — {r['friend_name']} — {r['book_name']}": r['tracker_id']
                for _, r in active_loans.iterrows()
            }

            with st.form("return_form"):
                selected  = st.selectbox("Select Loan to Return", list(loan_options.keys()))
                condition = st.selectbox("Book Condition on Return", ["mint", "good", "worn", "damaged"])
                submitted = st.form_submit_button("Mark as Returned")

                if submitted:
                    tracker_id = loan_options[selected]
                    # Get isbn before updating
                    loan_info = run_query(f"SELECT isbn FROM loans WHERE tracker_id = '{tracker_id}'").iloc[0]
                    run_write(f"""
                        UPDATE loans
                        SET return_date = CURDATE(), return_condition = '{condition}'
                        WHERE tracker_id = '{tracker_id}'
                    """)
                    # Mark book as available again
                    run_write(f"UPDATE books SET is_available = TRUE WHERE isbn = '{loan_info['isbn']}'")
                    result = run_query(
                        f"SELECT fine_amount FROM loans WHERE tracker_id = '{tracker_id}'"
                    ).iloc[0]
                    fine = float(result['fine_amount'])
                    if fine > 0:
                        st.session_state["book_returned"] = f"Book returned! A fine of £{fine:.2f} has been applied."
                        st.session_state["return_warning"] = True
                    else:
                        st.session_state["book_returned"] = "Book returned successfully! No fine."
                        st.session_state["return_warning"] = False
                    st.rerun()

        if "book_returned" in st.session_state:
            if st.session_state.get("return_warning"):
                st.warning(f"📬 {st.session_state['book_returned']}")
            else:
                st.success(f"📬 {st.session_state['book_returned']}")
            del st.session_state["book_returned"]
            del st.session_state["return_warning"]

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 7 — TRACK A LOAN
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🔍 Track a Loan":
        st.title("🔍 Track a Loan")
        st.markdown("---")

        tracker_input = st.text_input("Enter Tracker ID", placeholder="e.g. LIB-000001")

        if tracker_input:
            result = run_query(f"""
                SELECT
                    l.tracker_id,
                    f.friend_name,
                    f.phone_number,
                    b.book_name,
                    b.author,
                    l.loan_date,
                    l.due_date,
                    l.renewal_date,
                    l.return_date,
                    l.fine_amount,
                    l.fine_status,
                    CASE
                        WHEN l.return_date IS NOT NULL                         THEN 'Returned'
                        WHEN CURDATE() > COALESCE(l.renewal_date, l.due_date) THEN 'OVERDUE'
                        WHEN l.renewal_date IS NOT NULL                        THEN 'Renewed'
                        ELSE 'Active'
                    END AS status
                FROM loans l
                JOIN books   b ON l.isbn      = b.isbn
                JOIN friends f ON l.friend_id = f.friend_id
                WHERE l.tracker_id = '{tracker_input.upper().strip()}'
            """)

            if result.empty:
                st.warning(f"No loan found with tracker ID '{tracker_input}'.")
            else:
                row = result.iloc[0]
                st.subheader(f"{row['status']} — {row['tracker_id']}")
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Friend:** {row['friend_name']}")
                    st.write(f"**Phone:** {row['phone_number']}")
                    st.write(f"**Book:** {row['book_name']}")
                    st.write(f"**Author:** {row['author']}")
                with c2:
                    st.write(f"**Loan Date:** {row['loan_date']}")
                    st.write(f"**Due Date:** {row['due_date']}")
                    st.write(f"**Renewal Date:** {row['renewal_date'] or 'N/A'}")
                    st.write(f"**Returned:** {row['return_date'] or 'Not yet'}")
                st.markdown("---")
                st.write(f"**Fine:** £{float(row['fine_amount']):.2f} — Status: **{row['fine_status']}**")

                if row['fine_status'] == 'unpaid' and float(row['fine_amount']) > 0:
                    if st.button("Mark Fine as Paid"):
                        run_write(
                            f"UPDATE loans SET fine_status = 'paid' WHERE tracker_id = '{tracker_input.upper().strip()}'"
                        )
                        st.success("Fine marked as paid!")
                        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 8 — RENEW A LOAN
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🔄 Renew a Loan":
        st.title("🔄 Renew a Loan")
        st.markdown("---")

        active_loans = run_query("""
            SELECT
                l.tracker_id,
                f.friend_name,
                b.book_name,
                l.due_date,
                l.renewal_date
            FROM loans l
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            WHERE l.return_date IS NULL
            ORDER BY l.due_date ASC
        """)

        if active_loans.empty:
            st.info("No active loans to renew!")
        else:
            loan_options = {
                f"{r['tracker_id']} — {r['friend_name']} — {r['book_name']}": r['tracker_id']
                for _, r in active_loans.iterrows()
            }

            with st.form("renew_form"):
                selected   = st.selectbox("Select Loan to Renew", list(loan_options.keys()))
                extra_days = st.slider("Extra Days", 3, 30, 7)
                submitted  = st.form_submit_button("Renew Loan")

                if submitted:
                    tracker_id = loan_options[selected]
                    run_write(f"""
                        UPDATE loans
                        SET renewal_date = DATE_ADD(COALESCE(renewal_date, due_date), INTERVAL {extra_days} DAY)
                        WHERE tracker_id = '{tracker_id}'
                    """)
                    st.session_state["loan_renewed"] = f"Loan {tracker_id} renewed by {extra_days} extra days!"
                    st.rerun()

        if "loan_renewed" in st.session_state:
            st.success(f"✅ {st.session_state['loan_renewed']}")
            del st.session_state["loan_renewed"]

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 9 — LEAVE A REVIEW
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "⭐ Leave a Review":
        st.title("⭐ Leave a Review")
        st.markdown("---")

        if "review_added" in st.session_state:
            st.success(st.session_state["review_added"])
            del st.session_state["review_added"]

        st.subheader("📝 Add a New Review")

        all_loans = run_query("""
            SELECT
                l.loan_id,
                l.tracker_id,
                f.friend_name,
                b.book_name,
                l.return_date,
                CASE WHEN l.return_date IS NOT NULL THEN 'Returned' ELSE 'Active' END AS loan_status,
                CASE WHEN r.review_id IS NOT NULL THEN 'Yes' ELSE 'No' END AS reviewed
            FROM loans l
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            LEFT JOIN reviews r ON l.loan_id = r.loan_id
            ORDER BY l.return_date DESC, l.loan_date DESC
        """)

        if all_loans.empty:
            st.info("No loans found. Lend a book first before leaving a review!")
        else:
            unreviewed = all_loans[all_loans["reviewed"] == "No"]
            reviewed   = all_loans[all_loans["reviewed"] == "Yes"]

            st.caption(f"{len(unreviewed)} loan(s) without a review · {len(reviewed)} already reviewed")

            if unreviewed.empty:
                st.info("All loans have already been reviewed!")
            else:
                loan_options = {
                    f"{r['tracker_id']} — {r['friend_name']} — {r['book_name']} [{r['loan_status']}]": r['loan_id']
                    for _, r in unreviewed.iterrows()
                }

                with st.form("review_form"):
                    st.markdown("**Select a loan to review:**")
                    selected    = st.selectbox("Loan", list(loan_options.keys()))
                    st.markdown("**Your rating:**")
                    rating      = st.slider("Stars (1-5)", 1, 5, 4)
                    st.markdown("**Your review:**")
                    review_text = st.text_area(
                        "Write your thoughts",
                        placeholder="What did you think of this book? Would you recommend it?",
                        height=120
                    )
                    submitted = st.form_submit_button("Submit Review", use_container_width=True)

                    if submitted:
                        loan_id     = loan_options[selected]
                        safe_review = review_text.replace("'", "")
                        existing    = run_query(f"SELECT review_id FROM reviews WHERE loan_id = {loan_id}")
                        if not existing.empty:
                            st.warning("This loan already has a review.")
                        else:
                            run_write(f"""
                                INSERT INTO reviews (loan_id, rating, review_text, reviewed_on)
                                VALUES ({loan_id}, {rating}, '{safe_review}', CURDATE())
                            """)
                            book_name = selected.split(" — ")[2].split(" [")[0]
                            st.session_state["review_added"] = f"{'star' * rating} Review submitted for '{book_name}'!"
                            st.rerun()

        st.markdown("---")
        st.subheader("All Reviews")
        reviews = run_query("""
            SELECT
                f.friend_name,
                b.book_name,
                r.rating,
                r.review_text,
                r.reviewed_on
            FROM reviews r
            JOIN loans   l ON r.loan_id   = l.loan_id
            JOIN books   b ON l.isbn      = b.isbn
            JOIN friends f ON l.friend_id = f.friend_id
            ORDER BY r.reviewed_on DESC
        """)
        if not reviews.empty:
            st.markdown(f"**{len(reviews)} review(s) total**")
            st.dataframe(reviews, use_container_width=True, hide_index=True)
        else:
            st.info("No reviews yet!")


    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 10 — WISHLIST
    # ══════════════════════════════════════════════════════════════════════════
    elif page == "🎁 Wishlist":
        st.title("🎁 Wishlist")
        st.markdown("---")

        wishlist = run_query("""
            SELECT
                w.wishlist_id,
                f.friend_name,
                w.book_title,
                w.author,
                w.requested_on,
                w.fulfilled
            FROM wishlist w
            JOIN friends f ON w.friend_id = f.friend_id
            ORDER BY w.fulfilled ASC, w.requested_on ASC
        """)

        wishlist["status"] = wishlist["fulfilled"].apply(lambda x: "Fulfilled" if x == 1 else "Pending")
        pending   = wishlist[wishlist["fulfilled"] == 0]
        fulfilled = wishlist[wishlist["fulfilled"] == 1]

        col1, col2 = st.columns(2)
        col1.metric("Pending",   len(pending))
        col2.metric("Fulfilled", len(fulfilled))
        st.markdown("---")

        st.subheader("Pending Requests")
        if pending.empty:
            st.info("No pending wishlist requests!")
        else:
            for _, row in pending.iterrows():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.write(f"**{row['book_title']}** by {row['author']} — requested by *{row['friend_name']}* on {row['requested_on']}")
                with c2:
                    if st.button("Fulfil", key=f"wish_{row['wishlist_id']}"):
                        run_write(f"UPDATE wishlist SET fulfilled = TRUE WHERE wishlist_id = {row['wishlist_id']}")
                        st.success("Marked as fulfilled!")
                        st.rerun()

        st.markdown("---")
        st.subheader("➕ Add a Wishlist Request")
        with st.expander("Click to add a request"):
            friends_list = run_query("SELECT friend_id, friend_name FROM friends ORDER BY friend_name")
            with st.form("wishlist_form"):
                friend_options  = {r['friend_name']: r['friend_id'] for _, r in friends_list.iterrows()}
                selected_friend = st.selectbox("Friend", list(friend_options.keys()))
                wish_title      = st.text_input("Book Title")
                wish_author     = st.text_input("Author (optional)")
                submitted       = st.form_submit_button("Add to Wishlist")

                if submitted:
                    if not wish_title:
                        st.warning("Book title is required.")
                    else:
                        friend_id  = friend_options[selected_friend]
                        safe_title = wish_title.replace("'", "")
                        safe_auth  = wish_author.replace("'", "")
                        run_write(f"""
                            INSERT INTO wishlist (friend_id, book_title, author, fulfilled)
                            VALUES ({friend_id}, '{safe_title}', '{safe_auth}', FALSE)
                        """)
                        st.session_state["wish_added"] = f"'{wish_title}' added to wishlist for {selected_friend}!"
                        st.rerun()

        if "wish_added" in st.session_state:
            st.success(f"✅ {st.session_state['wish_added']}")
            del st.session_state["wish_added"]

        if not fulfilled.empty:
            st.markdown("---")
            st.subheader("Fulfilled Requests")
            st.dataframe(
                fulfilled[["friend_name", "book_title", "author", "requested_on"]],
                use_container_width=True,
                hide_index=True
            )
