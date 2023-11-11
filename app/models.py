from app import db
import sqlalchemy

# Create a model for a person
class Person(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    
    # Name
    name = sqlalchemy.Column(sqlalchemy.String) # "Calloway Patrick Sutton"
    
    # Parent class which is one or more Person objects
    parents = sqlalchemy.Column(sqlalchemy.String) # "2,3"
    siblings = sqlalchemy.Column(sqlalchemy.String) # "4,5"
    
    # Titles
    title = sqlalchemy.Column(sqlalchemy.Text)
    
    # Bio
    bio = sqlalchemy.Column(sqlalchemy.Text)
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name.split(" ")[::-1] # "[Sutton, Patrick, Calloway]"
    
    def get_family_name(self):
        return self.get_name()[0] # "Sutton"
    
    def get_given_name(self):
        return self.get_name()[1:][::-1] # "[Calloway, Patrick]"
    
    def get_parents(self):
        if self.parents:
            return [Person.query.get(int(parent_id)) for parent_id in self.parents.split(",") if parent_id != ""]
        else:
            return []
    
    def get_siblings(self):
        if self.parents:
            return [Person.query.get(int(sibling_id)) for sibling_id in self.siblings.split(",") if sibling_id != ""]
        else:
            return []