from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3
from db import get_db, get_report_data
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, pwd))
        con.commit()
        flash('Registered successfully! Login now.')
        return redirect('/')
    return render_template('register.html')

# Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (uname, pwd))
        user = cur.fetchone()
        if user:
            session['user'] = uname
            return redirect('/dashboard')
        flash('Invalid credentials')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out.")
    return redirect('/')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

# View/Add Books
@app.route('/books')
def books():
    conn = sqlite3.connect('db/library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return render_template('books.html', books=books)
@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']
    isbn = request.form['isbn']
    copies = request.form['copies']

    conn = sqlite3.connect('db/library.db')
    c = conn.cursor()
    c.execute("INSERT INTO book (title, author, year, isbn, copies) VALUES (?, ?, ?, ?, ?)",
              (title, author, year, isbn, copies))
    conn.commit()
    conn.close()

    return redirect(url_for('books'))
# Delete Book
@app.route('/books/delete/<int:book_id>')
def delete_book(book_id):
    if 'user' not in session:
        return redirect('/')
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    con.commit()
    flash("Book deleted")
    return redirect('/books')

# View/Add Members
@app.route('/members', methods=['GET', 'POST'])
def members():
    if 'user' not in session:
        return redirect('/')
    con = get_db()
    cur = con.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
        con.commit()
        flash("Member added")
        return redirect('/members')
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    return render_template('members.html', members=members)

# Delete Member
@app.route('/members/delete/<int:member_id>')
def delete_member(member_id):
    if 'user' not in session:
        return redirect('/')
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM members WHERE id=?", (member_id,))
    con.commit()
    flash("Member deleted")
    return redirect('/members')

# Issue Book
@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    if 'user' not in session:
        return redirect('/')
    con = get_db()
    cur = con.cursor()
    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        issue_date = request.form['issue_date']
        due_date = request.form['due_date']
        cur.execute("INSERT INTO transactions (book_id, member_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
                    (book_id, member_id, issue_date, due_date))
        con.commit()
        flash("Book issued successfully")
        return redirect('/issue')
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.execute("SELECT * FROM members")
    members = cur.fetchall()
    return render_template('issue.html', books=books, members=members)

# Return Book
@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if 'user' not in session:
        return redirect('/')
    con = get_db()
    cur = con.cursor()
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        return_date = request.form['return_date']
        cur.execute("UPDATE transactions SET return_date=? WHERE id=?", (return_date, transaction_id))
        con.commit()
        flash("Book returned")
        return redirect('/return')
    cur.execute("SELECT * FROM transactions WHERE return_date IS NULL")
    transactions = cur.fetchall()
    return render_template('return.html', transactions=transactions)

# Report
@app.route('/report')
def report():
    if 'user' not in session:
        return redirect('/')
    data = get_report_data()
    return render_template('report.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
