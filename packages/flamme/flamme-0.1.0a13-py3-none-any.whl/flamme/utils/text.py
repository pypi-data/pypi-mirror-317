r"""Contain text utility functions."""

from __future__ import annotations

__all__ = ["markdown_to_html"]


from flamme.utils.imports import check_markdown, is_markdown_available

if is_markdown_available():  # pragma: no cover
    import markdown


def markdown_to_html(text: str, ignore_error: bool = False) -> str:
    r"""Convert a markdown text to HTML text.

    Args:
        text: The markdown text to convert.
        ignore_error: If ``False``, an error is raised if ``markdown``
            is not installed, otherwise the input text is returned.

    Returns:
        The converted text if ``markdown`` is installed,
            otherwise the input text.

    Example usage:

    ```pycon

    >>> from flamme.utils.text import markdown_to_html
    >>> out = markdown_to_html("- a\n- b\n- c")
    >>> print(out)
    <ul>
    <li>a</li>
    <li>b</li>
    <li>c</li>
    </ul>

    ```
    """
    if not ignore_error:
        check_markdown()
    if is_markdown_available():
        return markdown.markdown(text)
    return text
