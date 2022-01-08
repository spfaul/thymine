# Thymine-Lang (TL) - Thymine's custom Markdown-inspired markup language!

An example `test.tym` file with everything you need to know can be found [here](https://github.com/t0a5ted/thymine/blob/master/tests/test.tym), because who actually enjoys writing documentation??

The resulting generated HTML webpage can be found [here](https://github.com/t0a5ted/thymine/blob/master/tests/build/test.html).
To build the `test.tym` file, run `python main.py` in the root project directory (for now, until we have a proper cli).
It will be built with the `debug` template specified in [`templates.json`](https://github.com/t0a5ted/thymine/blob/master/templates.json), which has a sexy [gruvbox](https://s3-alpha.figma.com/hub/file/320830941/3d7b6fb4-1603-46de-b249-8a964036a8c4-cover) theme!

TL's source code can be found [here](https://github.com/t0a5ted/thymine/tree/master/src/lang). 

## Docs
### Metadata
TBD

## FYI
Q: Almost every other markup language is using RegEx, why go to the trouble of making a full tokenizer and parser?

A:
Thymine was created to learn more about markup languages, lexers, parsers, etc.
I do use RegEx for simple things like getting the level of a header, however I try not to depend heavily on it.  

> "Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems." - Jamie Zawinski, 1997

Good luck on making sense of my spaghetti code regardless.
