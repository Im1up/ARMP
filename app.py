from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('surgery_stats.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    surgeries = conn.execute('SELECT * FROM Surgeries').fetchall()

    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    
    stats = {}
    for surgery in surgeries:
        surgery_id = surgery['SurgeryID']
        
        # Fetch today's stats
        today_stat = conn.execute('''
            SELECT *
            FROM SurgeryStats
            WHERE SurgeryID = ? AND Date = ?
        ''', (surgery_id, today)).fetchone()
        
        if not today_stat:
            conn.execute('''
                INSERT INTO SurgeryStats (SurgeryID, Date) VALUES (?, ?)
            ''', (surgery_id, today))
            conn.commit()
            today_stat = conn.execute('''
                SELECT *
                FROM SurgeryStats
                WHERE SurgeryID = ? AND Date = ?
            ''', (surgery_id, today)).fetchone()
        
        # Fetch yesterday's stats
        yesterday_stat = conn.execute('''
            SELECT *
            FROM SurgeryStats
            WHERE SurgeryID = ? AND Date = ?
        ''', (surgery_id, yesterday)).fetchone()

        # Fetch predictions for today
        prediction = conn.execute('''
            SELECT *
            FROM SurgeryPredictions
            WHERE SurgeryID = ? AND Date = ?
        ''', (surgery_id, today)).fetchone()
        
        if not prediction:
            conn.execute('''
                INSERT INTO SurgeryPredictions (SurgeryID, Date) VALUES (?, ?)
            ''', (surgery_id, today))
            conn.commit()
            prediction = conn.execute('''
                SELECT *
                FROM SurgeryPredictions
                WHERE SurgeryID = ? AND Date = ?
            ''', (surgery_id, today)).fetchone()

        stats[surgery_id] = {
            'today': today_stat,
            'yesterday': yesterday_stat,
            'prediction': prediction
        }
    conn.close()

    return render_template('index.html', surgeries=surgeries, stats=stats, today=today, yesterday=yesterday)

@app.route('/manage')
def manage():
    conn = get_db_connection()
    surgeries = conn.execute('SELECT * FROM Surgeries').fetchall()

    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    
    stats = {}
    for surgery in surgeries:
        surgery_id = surgery['SurgeryID']
        
        # Fetch today's stats
        today_stat = conn.execute('''
            SELECT *
            FROM SurgeryStats
            WHERE SurgeryID = ? AND Date = ?
        ''', (surgery_id, today)).fetchone()
        
        if not today_stat:
            conn.execute('''
                INSERT INTO SurgeryStats (SurgeryID, Date) VALUES (?, ?)
            ''', (surgery_id, today))
            conn.commit()
            today_stat = conn.execute('''
                SELECT *
                FROM SurgeryStats
                WHERE SurgeryID = ? AND Date = ?
            ''', (surgery_id, today)).fetchone()
        
        # Fetch yesterday's stats
        yesterday_stat = conn.execute('''
            SELECT *
            FROM SurgeryStats
            WHERE SurgeryID = ? AND Date = ?
        ''', (surgery_id, yesterday)).fetchone()

        # Fetch predictions for today
        prediction = conn.execute('''
            SELECT *
            FROM SurgeryPredictions
            WHERE SurgeryID = ? AND Date = ?
        ''', (surgery_id, today)).fetchone()
        
        if not prediction:
            conn.execute('''
                INSERT INTO SurgeryPredictions (SurgeryID, Date) VALUES (?, ?)
            ''', (surgery_id, today))
            conn.commit()
            prediction = conn.execute('''
                SELECT *
                FROM SurgeryPredictions
                WHERE SurgeryID = ? AND Date = ?
            ''', (surgery_id, today)).fetchone()

        stats[surgery_id] = {
            'today': today_stat,
            'yesterday': yesterday_stat,
            'prediction': prediction
        }
    conn.close()

    return render_template('manage.html', surgeries=surgeries, stats=stats, today=today, yesterday=yesterday)

@app.route('/update', methods=['POST'])
def update():
    surgery_id = request.form['surgery_id']
    tasks = request.form['tasks']
    registrations = request.form['registrations']
    documents = request.form['documents']
    referrals = request.form['referrals']
    date = datetime.now().strftime('%Y-%m-%d')

    conn = get_db_connection()
    conn.execute('''
        UPDATE SurgeryStats
        SET Tasks = ?, Registrations = ?, Documents = ?, Referrals = ?
        WHERE SurgeryID = ? AND Date = ?
    ''', (tasks, registrations, documents, referrals, surgery_id, date))
    conn.commit()
    conn.close()

    return redirect(url_for('manage'))

@app.route('/update_prediction', methods=['POST'])
def update_prediction():
    surgery_id = request.form['surgery_id']
    predicted_tasks = request.form['predicted_tasks']
    predicted_registrations = request.form['predicted_registrations']
    predicted_documents = request.form['predicted_documents']
    predicted_referrals = request.form['predicted_referrals']
    date = datetime.now().strftime('%Y-%m-%d')

    conn = get_db_connection()
    conn.execute('''
        UPDATE SurgeryPredictions
        SET PredictedTasks = ?, PredictedRegistrations = ?, PredictedDocuments = ?, PredictedReferrals = ?
        WHERE SurgeryID = ? AND Date = ?
    ''', (predicted_tasks, predicted_registrations, predicted_documents, predicted_referrals, surgery_id, date))
    conn.commit()
    conn.close()

    return redirect(url_for('manage'))

@app.route('/total/<int:surgery_id>')
def total(surgery_id):
    conn = get_db_connection()
    total_stats = conn.execute('''
        SELECT 
            SUM(Tasks) AS TotalTasks, 
            SUM(Registrations) AS TotalRegistrations, 
            SUM(Documents) AS TotalDocuments, 
            SUM(Referrals) AS TotalReferrals 
        FROM SurgeryStats 
        WHERE SurgeryID = ?
    ''', (surgery_id,)).fetchone()
    conn.close()

    return render_template('total.html', total_stats=total_stats, surgery_id=surgery_id)

@app.route('/period/<int:surgery_id>')
def period(surgery_id):
    # Get the last 2 weeks
    end_date = datetime.now()
    start_date = end_date - timedelta(weeks=2)
    conn = get_db_connection()
    period_stats = conn.execute('''
        SELECT Date, Tasks, Registrations, Documents, Referrals
        FROM SurgeryStats
        WHERE SurgeryID = ? AND Date BETWEEN ? AND ?
        ORDER BY Date ASC
    ''', (surgery_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))).fetchall()
    conn.close()

    return render_template('period.html', period_stats=period_stats, surgery_id=surgery_id, start_date=start_date, end_date=end_date)

if __name__ == '__main__':
    app.run(debug=True)
