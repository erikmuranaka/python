from ninja import NinjaAPI
from financeiro.api_access import financeiro_router

api = NinjaAPI()
api.add_router('', financeiro_router)