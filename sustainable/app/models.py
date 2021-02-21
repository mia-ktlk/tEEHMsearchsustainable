from datetime import datetime
from sustainable.app import db, auth


# represents Search Sustainable user
class User:
    def __init__(self, email, password):
        self.user = auth.sign_in_with_email_and_password(
            form.username.data, form.password.data
        )
        self.user_id = user["idToken"]
        self.session["usr"] = user_id

    def signUp(self, email, password):
        self.user = auth.create_user_with_email_and_password(email, password)

    def signIn(self, email, password):
        self.user = auth.sign_in_with_email_and_password(email, password)
        self.token = auth.get_account_info(user["idToken"])

    def sendEmailVerification(self, id):
        auth.send_email_verification(id)


class ItemEntry:
    """
    Class to represent a single item entry in the database
    """

    def __init__(
        self, name, img, term, brand, price, rating, date, url, vendor, approved
    ):
        self.name = name
        self.img_src = img
        self.search_terms = term
        self.brand = brand
        self.price = price
        self.rating = rating
        self.date_stored = date
        self.url = url
        self.vendor = vendor
        self.approved = approved
        # add to firebase db
        try:
            self.add_to_db()
        except:
            print("error")

    def to_dict(self):
        return dict((key, value) for (key, value) in self.__dict__.items())

    def add_to_db(self):
        if db.child("items").order_by_child("url").equal_to(self.url).get:
            return "already in database"
        else:
            d = self.to_dict()
            db.child("items").push(d)
