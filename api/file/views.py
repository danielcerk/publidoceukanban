from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from api.cloudinary_utils import generate_cloudinary_signature, delete_from_cloudinary
from .models import FileCard
from .serializers import FileCardSerializer
from api.card.models import Card
from api.compress_utils import compress_file

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cloudinary_signature(request):
    """
    Endpoint para o frontend obter uma assinatura temporária
    """
    try:
        folder = request.GET.get('folder', 'files_cards')
        
        signature_data = generate_cloudinary_signature(
            folder=folder, 
            user_id=request.user.id
        )
        
        print(f"🎯 Enviando assinatura para frontend:")
        print(f"   User ID: {request.user.id}")
        print(f"   Timestamp: {signature_data['timestamp']}")
        print(f"   Folder: {signature_data['folder']}")
        
        return Response(signature_data)
    
    except Exception as e:
        print(f"💥 ERRO na view get_cloudinary_signature: {e}")
        return Response(
            {"error": "Erro ao gerar assinatura", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class FileCardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileCardSerializer

    def get_queryset(self):
        card_id = self.kwargs.get('card_pk')
        if card_id is None:
            return FileCard.objects.none()
        return FileCard.objects.filter(card_id=card_id).order_by('-id')

    def perform_create(self, serializer):
        """
        Cria novo file associado ao card
        """
        card_id = self.kwargs.get('card_pk')
        
        # ✅ CORREÇÃO: Remove a verificação de user que não existe no modelo Card
        card_instance = get_object_or_404(Card, pk=card_id)
        
        print(f"📝 Salvando arquivo para card {card_instance.id}")
        serializer.save(card=card_instance)

        

    def perform_destroy(self, instance):
        """
        Sobrescreve a exclusão para remover também do Cloudinary
        """
        try:
            if instance.file:
                print(f"🗑️ Tentando excluir arquivo do Cloudinary: {instance.file}")
                success = delete_from_cloudinary(instance.file)
                if not success:
                    print(f"⚠️ Aviso: Não foi possível excluir arquivo do Cloudinary: {instance.file}")
            
            instance.delete()
            print("✅ Arquivo excluído com sucesso do banco de dados")
            
        except Exception as e:
            print(f"💥 Erro durante exclusão: {e}")
            raise

    # ✅ REMOVA o método create sobrescrito se não for necessário
    # O método padrão do ModelViewSet já é suficiente