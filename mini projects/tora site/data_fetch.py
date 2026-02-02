import requests
import json

# Define books for each section
torah_books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
neviim_books = ["Joshua", "Judges", "I Samuel", "II Samuel", "I Kings", "II Kings", 
                "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", 
                "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi"]
ketuvim_books = ["Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", 
                 "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "I Chronicles", "II Chronicles"]

def fetch_book(book_name):
    url = f"https://www.sefaria.org/api/texts/{book_name}?context=0"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("text", [])
    else:
        print(f"Error fetching {book_name}: {response.status_code}")
        return []

def collect_verses(books, book_type):
    verses = []
    for book in books:
        chapters = fetch_book(book)
        for chapter_idx, chapter in enumerate(chapters):
            if isinstance(chapter, list):
                for verse_idx, verse in enumerate(chapter):
                    if verse.strip():  # Skip empty verses
                        verses.append({
                            "text": verse,
                            "book_type": book_type
                        })
    return verses

# Collect all verses
all_verses = []
all_verses.extend(collect_verses(torah_books, "Torah"))
all_verses.extend(collect_verses(neviim_books, "Nevi’im"))
all_verses.extend(collect_verses(ketuvim_books, "Ketuvim"))

# Save to JSON
with open("verses_data.json", "w", encoding="utf-8") as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=4)

print(f"Collected {len(all_verses)} verses and saved to verses_data.json")