
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re


def get_nq_tokens(simplified_nq_example):
  """Returns list of blank separated tokens."""

  if "document_text" not in simplified_nq_example:
    raise ValueError("`get_nq_tokens` should be called on a simplified NQ"
                     "example that contains the `document_text` field.")

  return simplified_nq_example["document_text"].split(" ")


def simplify_nq_example(nq_example):
  r"""Returns dictionary with blank separated tokens in `document_text` field.

  Removes byte offsets from annotations, and removes `document_html` and
  `document_tokens` fields. All annotations in the ouput are represented as
  [start_token, end_token) offsets into the blank separated tokens in the
  `document_text` field.

  WARNING: Tokens are separated by a single blank character. Do not split on
    arbitrary whitespace since different implementations have different
    treatments of some unicode characters such as \u180e.

  Args:
    nq_example: Dictionary containing original NQ example fields.

  Returns:
    Dictionary containing `document_text` field, not containing
    `document_tokens` or `document_html`, and with all annotations represented
    as [`start_token`, `end_token`) offsets into the space separated sequence.
  """

  def _clean_token(token):
    """Returns token in which blanks are replaced with underscores.

    HTML table cell openers may contain blanks if they span multiple columns.
    There are also a very few unicode characters that are prepended with blanks.

    Args:
      token: Dictionary representation of token in original NQ format.

    Returns:
      String token.
    """
    return re.sub(u" ", "_", token["token"])

  text = " ".join([_clean_token(t) for t in nq_example["document_tokens"]])

  def _remove_html_byte_offsets(span):
    if "start_byte" in span:
      del span["start_byte"]

    if "end_byte" in span:
      del span["end_byte"]

    return span

  def _clean_annotation(annotation):
    annotation["long_answer"] = _remove_html_byte_offsets(
        annotation["long_answer"])
    annotation["short_answers"] = [
        _remove_html_byte_offsets(sa) for sa in annotation["short_answers"]
    ]
    return annotation

  simplified_nq_example = {
      "question_text": nq_example["question_text"],
      "example_id": nq_example["example_id"],
      "document_url": nq_example["document_url"],
      "document_text": text,
      "long_answer_candidates": [
          _remove_html_byte_offsets(c)
          for c in nq_example["long_answer_candidates"]
      ],
      "annotations": [_clean_annotation(a) for a in nq_example["annotations"]]
  }

  if len(get_nq_tokens(simplified_nq_example)) != len(
      nq_example["document_tokens"]):
    raise ValueError("Incorrect number of tokens.")

  return simplified_nq_example