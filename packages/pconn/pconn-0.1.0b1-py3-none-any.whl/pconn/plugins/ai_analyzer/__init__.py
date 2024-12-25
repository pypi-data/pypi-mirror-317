"""Demo plugin to show functionalities."""

from __future__ import annotations

from collections.abc import AsyncIterable
from enum import StrEnum
import json
from typing import Any, TypeVar

from google.api_core.exceptions import InvalidArgument, ServerError
import google.generativeai as genai
from google.generativeai.types import RequestOptions

from pconn.const import CONF_API_KEY
from pconn.core import PConn
from pconn.exceptions import PluginEntryError
from pconn.plugin_entries import PluginEntry

DOMAIN = "ai_analyzer"

_DATA_TYPE = TypeVar("_DATA_TYPE", bound=StrEnum)


async def async_setup_entry(
    pconn: PConn, entry: PluginEntry[genai.GenerativeModel]
) -> bool:
    """Setup demo plugin from config."""
    genai.configure(api_key=entry.data[CONF_API_KEY])
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash-latest",
        system_instruction=[
            "You are a security system data analyzer.",
            "Keep your answers related to the provided data.",
        ],
    )
    session = genai.ChatSession(model)
    try:
        response = await session.send_message_async(
            "Are you working.",
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema={"type": "boolean"},
            ),
            request_options=RequestOptions(timeout=20),
        )
    except (InvalidArgument, ServerError) as err:
        raise PluginEntryError("Invalid API key") from err
    if response.text == "false":
        raise PluginEntryError("Gemini is not responding")

    entry.plugin_data = session
    return True


class AIAnalyzer:
    """AI Analyzer platform class."""

    def __init__(
        self, pconn: PConn, entry: PluginEntry, model: genai.ChatSession
    ) -> None:
        """Initialize plugin."""
        self.pconn = pconn
        self.plugin_entry = entry
        self.model = model

    async def _get_response_stream(self, prompt: str) -> AsyncIterable[str]:
        """Return the response from the AI model."""
        response = await self.model.send_message_async(
            prompt, stream=True, request_options=RequestOptions(timeout=20)
        )
        async for chunk in response:
            yield chunk.text

    async def async_generate_response(
        self, question: str, data: dict[str, Any]
    ) -> AsyncIterable[str]:
        """Return the response from the AI model."""
        prompt = f"""
        Using the previous answer if available and from the following data:

        {json.dumps(data, indent=4)}

        Please try to answer the following question in markdown language:
        {question}
        If the question is irrelevant simply say
        'Please ask a question related to the selected items.'
        """
        return self._get_response_stream(prompt)

    async def async_analyze_question(
        self, question: str, data_type: type[_DATA_TYPE]
    ) -> _DATA_TYPE:
        """Return the response from the AI model."""
        prompt = ["What is this question asking about:", question]
        response = await self.model.send_message_async(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="text/x.enum",
                response_schema=data_type,
            ),
            request_options=RequestOptions(timeout=20),
        )
        return data_type(response.text)

    async def async_generate_followup_response(
        self, question: str
    ) -> AsyncIterable[str]:
        """Return the response from the AI model."""
        return self._get_response_stream(question)

    async def verify_followup_question(self, question: str) -> bool:
        """Verify that the followup question is related to the previous answer."""
        response = await self.model.send_message_async(
            ["Is this question related to the previous response.", question],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema={"type": "boolean"},
            ),
            request_options=RequestOptions(timeout=20),
        )
        return response.text == "true"
