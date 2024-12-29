from datetime import datetime

from pydantic import Field

from Schemas_ses.models.model import Model


class BlacklistToken(Model):
    """
    Token Model for storing JWT tokens
    """
    token: str
    blacklisted_on: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self):
        return f'<id: token: {self.token}'

    def save(self):
        data = self.to_bson()
        result = self.database.Blacklist.insert_one(data)
        self.id = result.inserted_id

    @staticmethod
    def check_blacklist(auth_token, database):
        res = database.Blacklist.find_one({'token': auth_token})
        return bool(res)
