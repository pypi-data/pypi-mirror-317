from __future__ import annotations

from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
    completion_create_params,
)
from typing_extensions import Dict, Iterable, List, Optional, Union

from york_patched.common.client.llm.protocol import NOT_GIVEN, LlmClient, NotGiven
from york_patched.logger import logger


class AioLlmClient(LlmClient):
    def __init__(self, *clients: LlmClient):
        logger.info(f'clients init {clients}')
        self.__original_clients = clients
        self.__clients = []
        self.__supported_models = set()
        logger.info(f'init client {clients}')
        for client in clients:
            logger.info('ho rha hai')
            try:

                logger.info(f'client aavi gyo {client.get_models()}')
                self.__supported_models.update(client.get_models())
                logger.info('model support')
                self.__clients.append(client)
            except Exception:
                pass
        logger.info(f'clientttt {self.__supported_models}')

        logger.info(f'clientttt {self.__clients}')

    def get_models(self) -> set[str]:
        return self.__supported_models

    def is_model_supported(self, model: str) -> bool:
        return any(client.is_model_supported(model) for client in self.__clients)

    def is_prompt_supported(self, messages: Iterable[ChatCompletionMessageParam], model: str) -> int:
        for client in self.__clients:
            if client.is_model_supported(model):
                return client.is_prompt_supported(messages, model)
        return -1

    def truncate_messages(
        self, messages: Iterable[ChatCompletionMessageParam], model: str
    ) -> Iterable[ChatCompletionMessageParam]:
        for client in self.__clients:
            if client.is_model_supported(model):
                return client.truncate_messages(messages, model)
        return messages

    def chat_completion(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        model: str,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: dict | completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion:
        logger.info('done 12')
        logger.info(f'self.__clients:  {self.__clients}')
        logger.info(f'for loop model {model}')
        logger.info(f'self.__original_clients {self.__original_clients}')
            
        for client in self.__clients:
            try:

                logger.info(f'client:')
                if client.is_model_supported(model):
                    logger.info(f"Using {client.__class__.__name__} for model {model}")
                    
                    logger.debug(f"Using {client.__class__.__name__} for model {model}")
                    
                    return client.chat_completion(
                        messages,
                        model,
                        frequency_penalty,
                        logit_bias,
                        logprobs,
                        max_tokens,
                        n,
                        presence_penalty,
                        response_format,
                        stop,
                        temperature,
                        top_logprobs,
                        top_p,
                    )
                else:
                    logger.info(f"Model {model} is xyz")
            except Exception as e:
                logger.warn(f"Failed to connect to")
        client_names = [client.__class__.__name__ for client in self.__original_clients]
        raise ValueError(
            f"Model {model} is not supported by {client_names} clients. "
            f"Please ensure that the respective API keys are correct."
        )
