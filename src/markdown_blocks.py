def markdown_to_blocks(markdown: str):
    blocks = list(
        filter(
            lambda b: b != "",
            map(
                lambda b: b.strip(),
                markdown.split("\n\n"),
            ),
        )
    )
    return blocks
