from django.http import HttpResponse
from pymongo import MongoClient
from newsproject.utils import get_db_handle, get_collection_handle
from newsproject.settings import DATABASE_NAME, CONNECTIONSTRING, BLOG_COLLECTION
db_handle, mongo_client = get_db_handle(DATABASE_NAME, CONNECTIONSTRING)
blog_collection_handle = get_collection_handle(db_handle, BLOG_COLLECTION)
blog_collection_handle.insert({'teste':'teste'})

def index(request):

    return HttpResponse("Hello, world. You're at the polls index.")