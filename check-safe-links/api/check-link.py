import json
import sqlite3  # Możesz zmienić na inne połączenie DB, np. MySQL, PostgreSQL

def handler(request):
    # Zainicjalizuj połączenie z bazą danych
    conn = sqlite3.connect('/tmp/safe_links.db')  # SQLite działa w środowisku Vercel, używamy lokalnej bazy
    cursor = conn.cursor()

    # Pobierz link z zapytania
    link = request.args.get('link')

    # Sprawdź link w bazie danych
    cursor.execute("SELECT * FROM links WHERE url = ?", (link,))
    result = cursor.fetchone()

    # Sprawdź status
    if result:
        status = result[2]  # Załóżmy, że 2. kolumna to 'status'
        if status == 'bezpieczna':
            return json.dumps({"message": "Strona jest bezpieczna"})
        elif status == 'niebezpieczna':
            return json.dumps({"message": "Ten link nie jest bezpieczny"})
        else:
            return json.dumps({"message": "Ta strona jeszcze nie jest sprawdzona"})
    else:
        return json.dumps({"message": "Link nie znaleziony w bazie"})
