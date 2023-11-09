from app import app, db
from app.models import Person
from tqdm import tqdm

if __name__ == "__main__":
    with app.app_context():
        with open("names.tsv", "r") as f:
            for line in tqdm(f):
                for name in line.split("\t"):
                    name = name.rstrip()
                    name = name.strip()
                    if name.strip() == "":
                        continue
                    if name:
                        db.session.add(Person(name=name))
        db.session.commit()