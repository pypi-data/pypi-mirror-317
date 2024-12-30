"""Join two lists of items using a language model."""
import logging
from typing import Any, Optional, Tuple, List
from concurrent.futures import ThreadPoolExecutor
import functools

import numpy as np
from numpy.typing import ArrayLike
import tqdm

from joinly.ai import BaseAI, OpenAI

logger = logging.getLogger(__name__)


_DEFAULT_PROMPT = """
YOU MUST ONLY RETURN TWO ANSWERS AS A SINGLE WORD: FALSE if the two words do not match, TRUE if they do match. THIS
IS VERY IMPORTANT FOR HUMANITY.  You are given to words left and right.  Using the CONTEXT below as a guide, determine
if the two words refer to the same thing and thus are a close sematic match.  If they are a close semantic match, return
TRUE.  If they are not a close semantic match, return FALSE.  If you are unsure, return FALSE.

CONTEXT: {context}
"""

def process_embedding(item: Tuple[str, Any], llm: BaseAI) -> Tuple[Tuple[str, Optional[ArrayLike]], Any]:
    text, label = item
    vec = llm.embed(text)
    return ((text, vec), label)


def embed(items: List[Tuple[str, Any]], llm:Optional[BaseAI]=None) -> List[Tuple[Tuple[str, Optional[ArrayLike]], Any]]:
    if llm is None:
        llm = OpenAI()
    process_func = functools.partial(process_embedding, llm=llm)
    embeddings = []
    with ThreadPoolExecutor() as executor:
        futures = list(tqdm.tqdm(executor.map(process_func, items), total=len(items), desc="Embedding items"))
        embeddings.extend(futures)
    return embeddings


def _cosine(v1: ArrayLike, v2: ArrayLike) -> Any:
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


ITEM_TYPE = Tuple[str, Any]
EMBED_TIME_TYPE = Tuple[Tuple[str, ArrayLike], Any]
VALUE_TYPE = List[ITEM_TYPE]
LIST_EMBED_TYPE = List[EMBED_TIME_TYPE]
COGROUP_VALUE_TYPE = Tuple[VALUE_TYPE, VALUE_TYPE]


def _process_embedding_pair(pair: EMBED_TIME_TYPE, context: str, llm: BaseAI) -> Optional[Tuple[ITEM_TYPE, ITEM_TYPE]]:
    (lk, lv), (rk, rv) = pair
    match = matcher((lk, lv), (rk, rv), context, llm)
    if match:
        return (lk, lv), (rk, rv)
    return None


def _parallel_process_embed(
    left_list: List[ITEM_TYPE],
    right_list: List[ITEM_TYPE],
    context: str,
    llm: BaseAI,
    embedding_treshold: float
) -> List[Tuple[ITEM_TYPE, ITEM_TYPE]]:
    process_func = functools.partial(_process_embedding_pair, context=context, llm=llm)
    results = []
    right_embedding = embed(right_list, llm)
    with ThreadPoolExecutor() as executor:
        futures = []
        for left in tqdm.tqdm(left_list, leave=False):
            le = llm.embed(left[0])
            for right in right_embedding:
                ((rk, re), rv) = right
                if re is None or le is None:
                    continue
                dist = _cosine(le, re)
                if dist < embedding_treshold:
                    continue
                future = executor.submit(process_func, (left, (rk, rv)))
                futures.append(future)
        for future in tqdm.tqdm(futures):
            result = future.result()
            if result:
                left_v, right_v = result
                results.append((left_v, right_v))
    return results


def inner_join(
    left: List[ITEM_TYPE],
    right: List[ITEM_TYPE],
    context: str = "",
    llm: Optional[BaseAI] = None,
    embedding_treshold: float = 0.6,
) -> List[Tuple[ITEM_TYPE, ITEM_TYPE]]:
    """Inner join two lists of items using a language model.
    Args:
        left: List of items to join.
        right: List of items to join.
        context: Context for the join.
        llm: Language model to use for the join.
        embedding_treshold: Minimum distance between embeddings for a match.
    Returns:
        List of tuples of matched items.
    """
    if llm is None:
        llm = OpenAI()
    matches = _parallel_process_embed(left, right, context, llm, embedding_treshold)
    return matches


def left_join(
    left: List[ITEM_TYPE],
    right: List[ITEM_TYPE],
    context: str = "",
    llm: Optional[BaseAI] = None,
    embedding_treshold: float = 0.6,
) -> List[Tuple[ITEM_TYPE, Optional[ITEM_TYPE]]]:
    """Left join two lists of items using a language model.
    Args:
        left: List of items to join.
        right: List of items to join.
        context: Context for the join.
        llm: Language model to use for the join.
        embedding_treshold: Minimum distance between embeddings for a match.
    Returns:
        List of tuples of matched items.
    """
    inner = inner_join(left, right, context, llm, embedding_treshold)
    return_items: List[Tuple[ITEM_TYPE, Optional[ITEM_TYPE]]] = []
    for l in left:
        found = False
        for i in inner:
            if l == i[0]:
                return_items.append(i)
                found = True
                break
        if not found:
            return_items.append((l, None))
    return return_items + list(inner)


def right_join(
    left: List[ITEM_TYPE],
    right: List[ITEM_TYPE],
    context: str = "",
    llm: Optional[BaseAI] = None,
    embedding_treshold: float = 0.6,
) -> List[Tuple[Optional[ITEM_TYPE], ITEM_TYPE]]:
    """Right join two lists of items using a language model.
    Args:
        left: List of items to join.
        right: List of items to join.
        context: Context for the join.
        llm: Language model to use for the join.
        embedding_treshold: Minimum distance between embeddings for a match.
    Returns:
        List of tuples of matched items.
    """
    inner = inner_join(left, right, context, llm, embedding_treshold)
    return_items: List[Tuple[Optional[ITEM_TYPE], ITEM_TYPE]] = []
    for r in right:
        found = False
        for i in inner:
            if r == i[1]:
                return_items.append(i)
                found = True
                break
        if not found:
            return_items.append((None, r))
    return return_items + list(inner)


def full_join(
    left: List[ITEM_TYPE],
    right: List[ITEM_TYPE],
    context: str = "",
    llm: Optional[BaseAI] = None,
    embedding_treshold: float = 0.6,
) -> List[Tuple[Optional[ITEM_TYPE], Optional[ITEM_TYPE]]]:
    """Full join two lists of items using a language model.
    Args:
        left: List of items to join.
        right: List of items to join.
        context: Context for the join.
        llm: Language model to use for the join.
        embedding_treshold: The minimum distance between embeddings for a match.
    Returns:
        List of tuples of matched items.
    """
    inner = inner_join(left, right, context, llm, embedding_treshold)
    return_items: List[Tuple[Optional[ITEM_TYPE], Optional[ITEM_TYPE]]] = []
    for l in left:
        found = False
        for i in inner:
            if l == i[0]:
                return_items.append(i)
                found = True
                break
        if not found:
            return_items.append((l, None))
    for r in right:
        found = False
        for i in inner:
            if r == i[1]:
                found = True
                break
        if not found:
            return_items.append((None, r))
    return return_items + list(inner)


def matcher(
    left: Tuple[str, Any],
    right: Tuple[str, Any],
    context: str = "",
    llm: Optional[BaseAI] = None,
) -> bool:
    """Match two items using a language model.
    Args:
        left: Item to match.
        right: Item to match.
        context: Context for the match.
        llm: Language model to use for the match.
    Returns:
        True if the items match, False otherwise.
    """
    if llm is None:
        llm = OpenAI()
    prompt = _DEFAULT_PROMPT.format(context=context)
    answer = llm(prompt, f"left = {str(left[0])}, right={str(right[0])}")
    logger.debug(answer)
    if answer is None:
        return False
    if "FALSE" in answer:
        return False
    return True
