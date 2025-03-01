from types import MethodType
from typing import Dict, Any

from transformers import AutoTokenizer, PreTrainedTokenizerBase, PreTrainedTokenizer

from distillflow.common import get_logger
from distillflow.model.args import ModelArguments

logger = get_logger(__name__)

def tokenizer_init_kwargs(model_args: ModelArguments) -> Dict[str, Any]:
    r"""
    Gets arguments to load config/tokenizer/model.

    Note: including inplace operation of model_args.
    """
    return {
        "trust_remote_code": True,
        "cache_dir": model_args.cache_dir,
        "revision": model_args.model_revision,
        "token": model_args.hf_hub_token,
    }

def load_tokenizer(model_args: ModelArguments, template: str = None) -> PreTrainedTokenizer:
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            model_args.model_name_or_path,
            split_special_tokens=model_args.split_special_tokens,
            padding_side="right",
            **tokenizer_init_kwargs(model_args),
        )
    except Exception as e:
        raise OSError("Failed to load tokenizer.") from e

    if model_args.new_special_tokens is not None:
        num_added_tokens = tokenizer.add_special_tokens(
            dict(additional_special_tokens=model_args.new_special_tokens),
            replace_additional_special_tokens=False,
        )
        logger.info("Add {} to special tokens.".format(",".join(model_args.new_special_tokens)))
        if num_added_tokens > 0 and not model_args.resize_vocab:
            model_args.resize_vocab = True
            logger.warning("New tokens have been added, changed `resize_vocab` to True.")
    else:
        tokenizer.pad_token = tokenizer.eos_token

    if "PreTrainedTokenizerBase" not in str(tokenizer._pad.__func__):
        tokenizer._pad = MethodType(PreTrainedTokenizerBase._pad, tokenizer)

    if template is not None:
        tokenizer.chat_template = template

    return tokenizer
