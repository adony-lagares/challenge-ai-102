from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from utils.Config import Config

def analyse_card(card_url):
    """This function analyses the card info and return what it could find."""

    try:
        credential = AzureKeyCredential(Config.KEY)
        document_client = DocumentIntelligenceClient(Config.ENDPOINT, credential)
        card_info = document_client.begin_analyze_document("prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url))

        result = card_info.result()

        # iterate over returned info for each image (only one in this case)
        for document in result.documents:

            fields = document.get("fields", {})

            return {
                "card_name": fields.get("CardHolderName", {}).get("content"),
                "card_number": fields.get("CardNumber", {}).get("content"),
                "expiry_date": fields.get("ExpirationDate", {}).get("content"),
                "bank_name": fields.get("IssuingBank", {}).get("content")
            }

    except Exception as e:
        return None
