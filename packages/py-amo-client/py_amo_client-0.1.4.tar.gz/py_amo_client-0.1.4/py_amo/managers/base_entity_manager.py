from pydantic import BaseModel
from repositories import BaseRepository


class BaseEntityManager(BaseModel):

    def __init__(self, repository: BaseRepository, *args, **kwargs):
        self.repository = repository
        return super().__init__(*args, **kwargs)
    
    def save(self):
        self.repository.update(self)