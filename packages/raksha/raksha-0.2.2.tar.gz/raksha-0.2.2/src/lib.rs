use logos::{
    Lexer,
    Logos,
    Skip,
};
use pyo3::{
    exceptions::PyValueError,
    prelude::*,
};
use std::{
    fmt::Display,
    str::FromStr,
};
use strum::EnumString;
use thiserror::Error;

type Position = (usize, usize);

#[derive(Debug, PartialEq)]
struct TokenContent<'parse> {
    text: &'parse str,
    position: Position,
}

fn parse_newline<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) {
    lexer.extras.0 += 1;
    lexer.extras.1 = lexer.span().end;
}

fn parse_whitespace<'parse>(_: &mut Lexer<'parse, Token<'parse>>) -> Skip {
    Skip
}

fn parse_shortcut<'parse>(
    lexer: &mut Lexer<'parse, Token<'parse>>,
) -> TokenContent<'parse> {
    let text = lexer.slice().trim_start_matches("\\");

    let line = lexer.extras.0 + 1;
    let column = lexer.span().start - lexer.extras.1 + 1;
    let position = (line, column);

    TokenContent { text, position }
}

fn parse_enclosed_shortcut<'parse>(
    lexer: &mut Lexer<'parse, Token<'parse>>,
) -> TokenContent<'parse> {
    let text = lexer
        .slice()
        .trim_start_matches("\\")
        .trim_end_matches("\\");

    let line = lexer.extras.0 + 1;
    let column = lexer.span().start - lexer.extras.1 + 1;
    let position = (line, column);

    TokenContent { text, position }
}

fn parse_open_tag<'parse>(
    lexer: &mut Lexer<'parse, Token<'parse>>,
) -> TokenContent<'parse> {
    let text = lexer.slice().trim_start_matches("<").trim_end_matches(">");

    let line = lexer.extras.0 + 1;
    let column = lexer.span().start - lexer.extras.1 + 1;
    let position = (line, column);

    TokenContent { text, position }
}

fn parse_close_tag<'parse>(
    lexer: &mut Lexer<'parse, Token<'parse>>,
) -> TokenContent<'parse> {
    let text = lexer.slice().trim_start_matches("</").trim_end_matches(">");

    let line = lexer.extras.0 + 1;
    let column = lexer.span().start - lexer.extras.1 + 1;
    let position = (line, column);

    TokenContent { text, position }
}

fn parse_self_closing_tag<'parse>(
    lexer: &mut Lexer<'parse, Token<'parse>>,
) -> TokenContent<'parse> {
    let text = lexer.slice().trim_start_matches("<").trim_end_matches("/>");

    let line = lexer.extras.0 + 1;
    let column = lexer.span().start - lexer.extras.1 + 1;
    let position = (line, column);

    TokenContent { text, position }
}

fn parse_text<'parse>(
    lexer: &mut Lexer<'parse, Token<'parse>>,
) -> TokenContent<'parse> {
    let text = lexer.slice();

    let line = lexer.extras.0 + 1;
    let column = lexer.span().start - lexer.extras.1 + 1;
    let position = (line, column);

    TokenContent { text, position }
}

#[derive(Logos, Debug, PartialEq)]
#[logos(extras = Position)]
enum Token<'parse> {
    #[regex(r#"\n"#, parse_newline)]
    Newline,

    #[regex(r#"[ \t\r\f]+"#, parse_whitespace)]
    Whitespace,

    #[regex(r#"\\[A-Za-z0-9]+"#, parse_shortcut)]
    Shortcut(TokenContent<'parse>),

    #[regex(r#"\\[A-Za-z0-9]+\\"#, parse_enclosed_shortcut)]
    EnclosedShortcut(TokenContent<'parse>),

    #[regex(r#"<[A-Za-z0-9]+>"#, parse_open_tag)]
    OpenTag(TokenContent<'parse>),

    #[regex(r#"</[A-Za-z0-9]+>"#, parse_close_tag)]
    CloseTag(TokenContent<'parse>),

    #[regex(r#"<[A-Za-z0-9]+/>"#, parse_self_closing_tag)]
    SelfClosingTag(TokenContent<'parse>),

    #[regex(r#"([^\n^<^"\\]|\\["\\bnfrt]|u[a-fA-F0-9]{4})*"#, parse_text)]
    Text(TokenContent<'parse>),
}

#[derive(Debug, PartialEq, Clone)]
enum ShortcutKind {
    Prefixed,
    Enclosed,
}

#[derive(EnumString, Debug, PartialEq, Clone)]
#[strum(ascii_case_insensitive)]
enum Shortcuts {
    Va,
    Msca,
    Mscb,
    BhG,
    Similar,
    Vab,
    Vad,
    Vd,
}

#[derive(Debug, PartialEq, Clone)]
#[pyclass]
struct Shortcut {
    kind: ShortcutKind,
    inner: Shortcuts,
}

impl Display for Shortcut {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self.kind {
            ShortcutKind::Prefixed => write!(f, "\\{:?}", self.inner),
            ShortcutKind::Enclosed => write!(f, "\\{:?}\\", self.inner),
        }
    }
}

#[derive(Debug, PartialEq, Clone, Copy)]
enum TagKind {
    Open,
    Close,
    SelfClosing,
}

#[derive(EnumString, Debug, PartialEq, Clone, Copy)]
#[strum(serialize_all = "UPPERCASE")]

enum Tags {
    Start,
    Text,
    App,
    Paral,
    Note,
    Tr,
    Lem,
}

#[derive(Debug, PartialEq, Clone, Copy)]
#[pyclass]
struct Tag {
    kind: TagKind,
    inner: Tags,
}

impl Display for Tag {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self.kind {
            TagKind::Open => write!(f, "<{:?}>", self.inner),
            TagKind::Close => write!(f, "</{:?}>", self.inner),
            TagKind::SelfClosing => write!(f, "<{:?}/>", self.inner),
        }
    }
}

#[derive(Debug, PartialEq, Clone)]
#[pyclass]
enum Value {
    Shortcut(Shortcut),
    Tag(Tag),
    Text(String),
    Newline(),
}

impl Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Value::Shortcut(shortcut) => write!(f, "{}", shortcut),
            Value::Tag(tag) => write!(f, "{}", tag),
            Value::Text(text) => write!(f, "{}", text),
            Value::Newline() => write!(f, "\n"),
        }
    }
}

#[derive(Debug, Error)]
#[pyclass]
enum RakshaError {
    #[error("Could not parse input at {0:?}:{1:?} as {2:?}")]
    Parse(usize, usize, String),

    #[error("An empty tree is not allowed")]
    EmptyTree(),

    #[error("Tree doesn't begin with a root node. Found {0:?} instead")]
    NoRoot(Value),
}

impl From<RakshaError> for PyErr {
    fn from(value: RakshaError) -> Self {
        PyValueError::new_err(value.to_string())
    }
}

impl<'parse> TryFrom<Token<'parse>> for Value {
    type Error = RakshaError;

    fn try_from(value: Token<'parse>) -> Result<Self, Self::Error> {
        match value {
            Token::Shortcut(shortcut) => {
                let Ok(shortcut) = Shortcuts::from_str(shortcut.text) else {
                    return Err(RakshaError::Parse(
                        shortcut.position.0,
                        shortcut.position.1,
                        "Shortcut".to_string(),
                    ));
                };

                Ok(Value::Shortcut(Shortcut {
                    kind: ShortcutKind::Prefixed,
                    inner: shortcut,
                }))
            }

            Token::EnclosedShortcut(shortcut) => {
                let Ok(shortcut) = Shortcuts::from_str(shortcut.text) else {
                    return Err(RakshaError::Parse(
                        shortcut.position.0,
                        shortcut.position.1,
                        "Shortcut".to_string(),
                    ));
                };

                Ok(Value::Shortcut(Shortcut {
                    kind: ShortcutKind::Enclosed,
                    inner: shortcut,
                }))
            }

            Token::OpenTag(tag) => {
                let Ok(tag) = Tags::from_str(tag.text) else {
                    return Err(RakshaError::Parse(
                        tag.position.0,
                        tag.position.1,
                        "Tag".to_string(),
                    ));
                };

                Ok(Value::Tag(Tag {
                    kind: TagKind::Open,
                    inner: tag,
                }))
            }

            Token::CloseTag(tag) => {
                let Ok(tag) = Tags::from_str(tag.text) else {
                    return Err(RakshaError::Parse(
                        tag.position.0,
                        tag.position.1,
                        "Tag".to_string(),
                    ));
                };

                Ok(Value::Tag(Tag {
                    kind: TagKind::Close,
                    inner: tag,
                }))
            }

            Token::SelfClosingTag(tag) => {
                let Ok(tag) = Tags::from_str(tag.text) else {
                    return Err(RakshaError::Parse(
                        tag.position.0,
                        tag.position.1,
                        "Tag".to_string(),
                    ));
                };

                Ok(Value::Tag(Tag {
                    kind: TagKind::SelfClosing,
                    inner: tag,
                }))
            }

            Token::Text(content) => Ok(Value::Text(String::from(content.text))),

            Token::Newline => Ok(Value::Newline()),

            _ => unreachable!("Logos will not yield `SKIP` tokens"),
        }
    }
}

struct Iter<'parse> {
    lexer: Lexer<'parse, Token<'parse>>,
}

impl<'parse> std::iter::Iterator for Iter<'parse> {
    type Item = Result<Value, RakshaError>;

    fn next(&mut self) -> Option<Self::Item> {
        match self.lexer.next() {
            Some(Ok(token)) => Some(Value::try_from(token)),
            _ => None,
        }
    }
}

impl<'parse> From<&'parse str> for Iter<'parse> {
    fn from(value: &'parse str) -> Self {
        Self {
            lexer: Token::lexer(value),
        }
    }
}

/// For tags that have node children
#[derive(Debug, PartialEq)]
#[pyclass]
pub struct DOM {
    root: Tags,
    children: Vec<DomChild>,
}

#[pymethods]
impl DOM {
    fn __repr__(&self) -> String {
        format!("DOM({:#?})", self)
    }

    fn __str__(&self) -> String {
        format!("{:?}", self)
    }

    #[staticmethod]
    fn parse(input: &str) -> Result<DOM, RakshaError> {
        DOM::populate(input)
    }
}

/// Either a childless or a regular Element node
#[derive(Debug, PartialEq)]
enum DomChild {
    Leaf(Value),
    Node(DOM),
}

impl DOM {
    fn new(tag: Tags) -> Self {
        Self {
            root: tag,
            children: vec![],
        }
    }

    fn append(&mut self, value: DomChild) {
        self.children.push(value);
    }

    fn populate<'parse>(input: &'parse str) -> Result<DOM, RakshaError> {
        let mut lexer = Iter::from(input);

        let Some(maybe_val) = lexer.next() else {
            return Err(RakshaError::EmptyTree());
        };

        let val = match maybe_val {
            Ok(val) => val,
            Err(e) => return Err(e),
        };

        let mut dom = match val {
            Value::Tag(tag) => Self::new(tag.inner),
            _ => {
                return Err(RakshaError::NoRoot(val));
            }
        };

        while let Some(value) = lexer.next() {
            match value {
                Ok(Value::Tag(tag)) => match tag.kind {
                    TagKind::Close => {}
                    _ => {
                        let child_node = Self::populate_from(&mut lexer, tag)?;
                        dom.append(child_node);
                    }
                },
                Ok(other) => dom.append(DomChild::Leaf(other)),
                Err(e) => return Err(e),
            }
        }

        Ok(dom)
    }

    fn populate_from<'parse>(
        lexer: &mut Iter<'parse>,
        root: Tag,
    ) -> Result<DomChild, RakshaError> {
        let mut dom = Self::new(root.inner);

        while let Some(value) = lexer.next() {
            match value {
                Ok(Value::Tag(tag)) => match tag.kind {
                    TagKind::Open => {
                        let child_node = Self::populate_from(lexer, tag)?;
                        dom.append(child_node);
                    }
                    TagKind::SelfClosing => {
                        dom.append(DomChild::Leaf(Value::Tag(tag)));
                    }
                    TagKind::Close => {
                        if tag.inner == root.inner {
                            return Ok(DomChild::Node(dom));
                        } else {
                            panic!("Tag mismatch: {} != {}", tag, root);
                        }
                    }
                },
                Ok(other) => dom.append(DomChild::Leaf(other)),
                Err(e) => return Err(e),
            }
        }

        Ok(DomChild::Node(dom))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn raksha(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<DOM>()?;
    Ok(())
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test() {
        let input = r#"<START>

<TEXT> blablabla  blablabla blabla  bliblibli bliblibli blibli|</TEXT>
        <APP>\va <LEM>blabla</LEM> \msCa; bloblu \msCb</APP>
        <PARAL>\vab \similar\ \BhG\ 10.12ab$</PARAL>
        <NOTE>So this is a short 
        note...</NOTE>
        <TR>This is the beginning of the translation...</TR>

<TEXT> blobloblo  blobloblo bloblo  blublublublu blubluṃ blublu||</TEXT>
        <APP>\vd <LEM>blubluṃ</LEM> \msCa; bloblumda \msCb</APP>
        <TR>... and then it contimues.ह</TR>

</START>"#
            .trim();

        let dom = DOM::populate(input).unwrap();

        println!("{:#?}", dom);
    }
}
