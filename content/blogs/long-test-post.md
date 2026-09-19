# The Long Test Post

This is a deliberately long blog post written for testing purposes. It exercises
headings, paragraphs, lists, blockquotes, code blocks, tables, inline styling,
links, images, and horizontal rules so you can verify that every piece of
markdown renders correctly. Feel free to delete it once you are done testing.

## Why Testing Matters

Any software project benefits from thorough testing, but content pipelines are
especially prone to subtle failures. Markdown parsers behave differently across
libraries, templates can mangle HTML, and special characters are easy to
mistype. By writing a long, varied post we can catch those problems before a
real reader ever sees them.

### Paragraph Fatigue

Reading long paragraphs is tiring. It tests your patience, your eyesight, and,
most importantly, your rendering pipeline. Really long paragraphs stress line
wrapping, block layout, and font metrics within the blog template. The text you
are reading right now is intentionally meandering so that the width of the
content column is pushed close to its limit and the reflow logic has to work.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.

## Features To Check

Here is a checklist of everything this post is meant to exercise:

1. Headings from level one down to level four
2. Bold, italic, strikethrough, and inline code
3. Unordered and ordered, nested lists
4. Blockquotes
5. Fenced and indented code blocks
6. Links, including reference-style links
7. Tables
8. Horizontal rules
9. Images (with a broken source on purpose)
10. Long paragraphs and long words

### Inline Styling

You can write **bold text**, *italicised text*, **_bold italic_**, ~~struck
through~~, and `inline code`. You can even mix them together like **a bold
paragraph that contains *italics* and `code`** to ensure the CSS doesn't break.

Special characters: ampersands &amp; that kind of thing, &lt;angle brackets&gt;,
quotation "marks", apostrophes 'like this', and the occasional em dash --- or
ellipsis... All of these should survive the round trip through the markdown
parser without being mangled or escaped twice.

### Lists

#### Unordered

- First item
- Second item
  - Nested item one
  - Nested item two
    - Deeply nested item
      - Even deeper
- Third item after the nesting

#### Ordered

1. Wake up
2. Drink coffee
3. Write a blog post
   1. Open the editor
   2. Think very hard
   3. Type, delete, retype
4. Publish and hope for the best
5. Check the analytics

### Blockquotes

> This is a blockquote. It is used to highlight an excerpt, a note, or someone
> else's words.
>
> > Nested blockquotes also work, though they are rare.
>
> The blockquote can contain **styled** text and even `code`.

> A very long blockquote that goes on and on for a while to make sure that the
> blockquote styling handles multiple wrapped lines gracefully and the left
> border is drawn correctly across the entire quoted region without any gaps or
> glitches appearing between consecutive lines in the rendered output.

## Code Blocks

Fenced code block with no language:

```
def hello():
    print("Hello, world!")
```

Fenced code block with a language (Python):

```python
import random
from typing import List


def sample(items: List[int], k: int) -> List[int]:
    """Return k random samples from items without replacement."""
    return random.sample(items, k=k)


def main() -> None:
    data = list(range(100))
    print(sample(data, 5))


if __name__ == "__main__":
    main()
```

Fenced code block with JSON, which frequently trips people up:

```json
{
  "name": "bloggy",
  "version": "0.1.0",
  "features": [
    "markdown rendering",
    "strict HTML escaping",
    "code highlighting"
  ],
  "nested": {
    "objects": [true, false, null, 42, 3.14]
  }
}
```

An indented code block (four spaces):

    This block was indented with four spaces.
    It contains no syntax highlighting.
        It can even contain further indentation.

### Code Blocks In Lists

1. First, install the package:

   ```bash
   pip install example-package
   ```

2. Then run the server:

   ```bash
   cd bloggy
   python main.py
   ```

3. Finally, visit `http://localhost:8000` in your browser and confirm that
   the server logs show a successful request.

## Links

Inline link: [Flask](https://flask.palletsprojects.com/).

Reference-style link: the Markdown [spec][md] is worth a read, and so is the
Python-Markdown [documentation][pymd].

[md]: https://daringfireball.net/projects/markdown/
[pymd]: https://python-markdown.github.io/

A bare URL (auto-link): https://example.com

A relative link that will 404 on purpose: [this page does not exist](/blog/nope).

## Tables

| Feature          | Supported | Notes                        |
| ---------------- | :-------: | --------------------------- |
| Headings         |    Yes    | All levels                   |
| Lists            |    Yes    | Nested and mixed             |
| Code blocks      |    Yes    | With and without language    |
| Tables           |    Yes    | This very table              |
| Images           |    Yes    | See below                    |
| Raw HTML         |    No     | Is this post escaping it?    |
| Long words       |    Yes    | Pneumonoultramicroscopicsilicovolcanoconiosis |

A second, narrower table to verify both alignment and number alignment:

| Left                | Center        | Right |
| :------------------ | :-----------: | ----: |
| one                 |     -2        |   400 |
| twenty-three        |     120       |     1 |
| four                |   9000        | 12345 |

## Images

This image references a file that almost certainly does not exist, so the
broken-image icon should appear while the title text stays readable:

![Broken image for testing](no-broken-image.png "Broken test image")

A data-URI style of pixel would be better but is not available here, so we
settle for describing what would ordinarily go in this spot.

## Horizontal Rules

Below this paragraph is a horizontal rule built from three asterisks.

***

Then another one built from dashes.

---

And a third built from underscores, just to be thorough.

___

## Raw HTML / Escaping

The parser may or may not allow raw HTML. Whatever the config, this has to be
rendered safely:

```html
<script>alert('xss');</script>
```

Important: the tag above must appear as *text* inside the code block and never
execute. Inline in the paragraph, a raw `<script>` tag should likewise be
escaped (or stripped):


And an `<img onerror="...">` should not fire:


If your markdown library escapes HTML, these will render as visible text. If it
does not, you have a security problem and this test post has done its job.

## Words And Characters

A word that is famously very long: Pneumonoultramicroscopicsilicovolcanoconiosis
is 45 characters, but it is not the longest word in any language.

Characters to double check: é, ü, ñ, 中, 日本語, العربية, 👩‍💻, 🧪, €, £, ¥, ©, ®, ™.

Works with Markdown: `x^2 + y^2 = z^2` and `CO_2` for sub/superscripts if the
library supports them: H~2~O and x^2^.

## Conclusion

If all of the above renders cleanly, then the blog pipeline is in good shape:
titles, inline styling, lists, quotes, code, links, tables, images, and
escaping all behave. If something looks wrong, you now have a single document
you can trim down to isolate the offending construct.

Remember to delete this file before going live, or at the very least remove it
from the article listing.