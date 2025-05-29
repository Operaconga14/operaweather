from mangum import Adapter
from .index import app

# Handler for Vercel
handler = Adapter(app) 