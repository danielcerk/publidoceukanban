import uuid
from django.conf import settings
from supabase import create_client

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
storage = supabase.storage

def upload_to_supabase(file):
    
    ext = file.name.split('.')[-1]
    
    short_uuid = str(uuid.uuid4())[:8]
    unique_filename = f'images_cards/{short_uuid}.{ext}'

    file_bytes = file.read()

    storage.from_(settings.SUPABASE_BUCKET).upload(unique_filename, file_bytes)
    public_url = storage.from_(settings.SUPABASE_BUCKET).get_public_url(unique_filename)

    return public_url