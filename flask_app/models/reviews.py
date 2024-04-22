from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Review:

    def __init__(self, data):
        self.id = data['id']
        self.book_name = data['book_name']
        self.author = data ['author']
        self.genre = data['genre']
        self.value = data['value']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.comments = data['comments']
        self.buy_link = data['buy_link']
        self.users_id = data['user_id']
        

    @staticmethod
    def validate_review(form):
        is_valid = True

        if form ["book_name"] == "":
            is_valid = False
            flash("Debes ingresar nombre de libro", "reseña")

        if form ["author"] == "":
            is_valid = False
            flash("Debes ingresar nombre de autor", "reseña")
        
        return is_valid

    @classmethod
    def save(cls, form):
        query = "INSERT INTO reviews(book_name, author, genre, value, comments, buy_link, user_id) VALUES (%(book_name)s, %(author)s, %(genre)s, %(value)s, %(comments)s, %(buy_link)s, %(user_id)s)"
        result = connectToMySQL('esquema_reviews').query_db(query, form)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews"
        results = connectToMySQL('esquema_reviews').query_db(query)
        reviews = []
        for review in results:
            reviews.append(cls(review))

        return reviews
    
    @classmethod
    def get_by_id(cls, review_id):
        query = "SELECT * FROM reviews WHERE id = %(id)s"
        data = { 'id': review_id }
        result = connectToMySQL('esquema_reviews').query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return None


