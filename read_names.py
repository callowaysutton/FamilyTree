from app import db
from app.models import Person

if __name__ == "__main__":
    with open("names.tsv", "r") as f:
        for line in f:
            for name in line.split("\t"):
                name = line.strip()
                if name:
                    db.session.add(Person(name=name))