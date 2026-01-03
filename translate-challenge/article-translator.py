"""Azure OpenAI Article Translator - Clean implementation."""

import os
import logging
from typing import Optional

from langchain_openai.chat_models.azure import AzureChatOpenAI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArticleTranslator:
    """Translate articles using Azure OpenAI GPT models."""
    
    def __init__(
        self,
        azure_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = "2024-02-15-preview",
        deployment_name: str = "gpt-4o-mini",
        max_retries: int = 2
    ):
        self.azure_endpoint = azure_endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')
        self.api_key = api_key or os.getenv('AZURE_OPENAI_KEY')
        
        if not self.azure_endpoint or not self.api_key:
            raise ValueError("Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY environment variables")
        
        self.client = AzureChatOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version=api_version,
            deployment_name=deployment_name,
            max_retries=max_retries
        )
    
    def translate_article(
        self,
        text: str,
        target_language: str,
        return_markdown: bool = True
    ) -> str:
        """
        Translate article text using GPT model.
        
        Args:
            text: Text to translate
            target_language: Target language (e.g., 'Português', 'Español')
            return_markdown: Whether to format response as markdown
            
        Returns:
            Translated text
        """
        format_instruction = " e responda em markdown" if return_markdown else ""
        
        messages = [
            ("system", "Você atua como tradutor de textos"),
            ("user", f"Traduza o texto '{text}' para o idioma {target_language}{format_instruction}")
        ]
        
        try:
            response = self.client.invoke(messages)
            logger.info(f"Successfully translated to {target_language}")
            return response.content
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise


if __name__ == "__main__":
    # Example usage
    translator = ArticleTranslator(
        azure_endpoint="https://oai-dio-bootcamp-dev-gi-001.openai.azure.com/",
        api_key="YOUR_API_KEY"
    )
    
    result = translator.translate_article("Spanish guitar", "Português")
    print(result)