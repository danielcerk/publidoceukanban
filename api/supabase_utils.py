import uuid
from django.conf import settings
from supabase import create_client
from storage3.exceptions import StorageApiError
#from api.compress_utils import compress_image

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
storage = supabase.storage

def upload_to_supabase(file, original_name=None, content_type=None):

    if file.size > 120 * 1024 * 1024:

        raise ValueError("O arquivo é muito grande. O limite é 120MB.")

    ext = file.name.split('.')[-1]
    
    short_uuid = str(uuid.uuid4())[:8]
    unique_filename = f'files_cards/{short_uuid}.{ext}'

    file_bytes = file.read()

    try:

        storage.from_(settings.SUPABASE_BUCKET).upload(
            unique_filename, file_bytes,
            {"content-type": content_type or "application/octet-stream"}
        )

    except StorageApiError as e:

        if e.status_code == 413:

            raise ValueError("O arquivo é muito grande. O limite é 120MB.")
        
        raise

    public_url = storage.from_(settings.SUPABASE_BUCKET).get_public_url(unique_filename)

    return public_url


def get_supabase_client():

    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_SERVICE_KEY

    return create_client(supabase_url, supabase_key)

def delete_from_supabase(file_path):

    try:

        print(f"INICIANDO EXCLUSÃO - file_path recebido: {file_path}")
        
        supabase = get_supabase_client()
        
        clean_file_path = file_path.split('?')[0]
        clean_file_path = clean_file_path.split('#')[0]
        
        print(f"File_path limpo: {clean_file_path}")
        
        if 'supabase.co/storage/v1/object/public/' in clean_file_path:

            parts = clean_file_path.split('/object/public/')

            if len(parts) > 1:

                bucket_and_path = parts[1]
                bucket_name = bucket_and_path.split('/')[0]
                file_name = '/'.join(bucket_and_path.split('/')[1:])
                
                print(f"Bucket extraído: {bucket_name}")
                print(f"Arquivo extraído: {file_name}")

            else:

                print("Não foi possível extrair bucket e arquivo da URL")

                return False
        else:

            bucket_name = settings.SUPABASE_BUCKET
            file_name = clean_file_path

            print(f"Bucket das settings: {bucket_name}")
            print(f"Arquivo direto: {file_name}")
    
        print(f"Tentando excluir: {file_name} do bucket: {bucket_name}")
        result = supabase.storage.from_(bucket_name).remove([file_name])
        print(f"Resultado da exclusão: {result}")
        
        if result:

            print("Arquivo excluído com sucesso do Supabase!")

            return True
        
        else:

            print("Exclusão retornou resultado vazio, mas pode ter funcionado")

            return True  
            
    except Exception as e:

        print(f"ERRO CRÍTICO ao excluir arquivo do Supabase: {e}")

        import traceback

        print(f"Stack trace: {traceback.format_exc()}")

        return False