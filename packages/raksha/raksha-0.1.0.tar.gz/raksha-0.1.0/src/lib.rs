use pyo3::prelude::*;

use logos::{Lexer, Logos};
use std::fmt::Display;
use std::str::FromStr;
use strum::EnumString;

fn parse_shortcut<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) -> &'parse str {
    lexer.slice().trim_start_matches("\\")
}

fn parse_enclosed_shortcut<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) -> &'parse str {
    lexer
        .slice()
        .trim_start_matches("\\")
        .trim_end_matches("\\")
}

fn parse_open_tag<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) -> &'parse str {
    lexer.slice().trim_start_matches("<").trim_end_matches(">")
}

fn parse_close_tag<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) -> &'parse str {
    lexer.slice().trim_start_matches("</").trim_end_matches(">")
}

fn parse_self_closing_tag<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) -> &'parse str {
    lexer.slice().trim_start_matches("<").trim_end_matches("/>")
}

fn parse_text<'parse>(lexer: &mut Lexer<'parse, Token<'parse>>) -> &'parse str {
    lexer.slice()
}

#[derive(Logos, Debug, PartialEq)]
#[logos(skip r"[ \t\r\n\f]+")]
enum Token<'parse> {
    #[regex(r#"\\[A-Za-z0-9]+"#, parse_shortcut)]
    Shortcut(&'parse str),

    #[regex(r#"\\[A-Za-z0-9]+\\"#, parse_enclosed_shortcut)]
    EnclosedShortcut(&'parse str),

    #[regex(r#"<[A-Za-z0-9]+>"#, parse_open_tag)]
    OpenTag(&'parse str),

    #[regex(r#"</[A-Za-z0-9]+>"#, parse_close_tag)]
    CloseTag(&'parse str),

    #[regex(r#"<[A-Za-z0-9]+/>"#, parse_self_closing_tag)]
    SelfClosingTag(&'parse str),

    #[regex(r#"([^<^"\\]|\\["\\bnfrt]|u[a-fA-F0-9]{4})*"#, parse_text)]
    Text(&'parse str),
}

#[derive(Debug, PartialEq)]
enum ShortcutKind {
    Prefixed,
    Enclosed,
}

#[derive(EnumString, Debug, PartialEq)]
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

#[derive(Debug, PartialEq)]
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

#[derive(Debug, PartialEq)]
enum Value {
    Shortcut(Shortcut),
    Tag(Tag),
    Text(String),
}

impl Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Value::Shortcut(shortcut) => write!(f, "{}", shortcut),
            Value::Tag(tag) => write!(f, "{}", tag),
            Value::Text(text) => write!(f, "{}", text),
        }
    }
}

impl<'parse> TryFrom<Token<'parse>> for Value {
    type Error = String;

    fn try_from(value: Token<'parse>) -> Result<Self, Self::Error> {
        match value {
            Token::Shortcut(shortcut) => Ok(Value::Shortcut(Shortcut {
                kind: ShortcutKind::Prefixed,
                inner: Shortcuts::from_str(shortcut)
                    .map_err(|er| format!("{}; {}", er, shortcut))?,
            })),
            Token::EnclosedShortcut(shortcut) => Ok(Value::Shortcut(Shortcut {
                kind: ShortcutKind::Enclosed,
                inner: Shortcuts::from_str(shortcut)
                    .map_err(|er| format!("{}; {}", er, shortcut))?,
            })),
            Token::OpenTag(tag) => Ok(Value::Tag(Tag {
                kind: TagKind::Open,
                inner: Tags::from_str(tag).map_err(|er| format!("{}; {}", er, tag))?,
            })),
            Token::CloseTag(tag) => Ok(Value::Tag(Tag {
                kind: TagKind::Close,
                inner: Tags::from_str(tag).map_err(|er| format!("{}; {}", er, tag))?,
            })),
            Token::SelfClosingTag(tag) => Ok(Value::Tag(Tag {
                kind: TagKind::SelfClosing,
                inner: Tags::from_str(tag).map_err(|er| format!("{}; {}", er, tag))?,
            })),
            Token::Text(text) => Ok(Value::Text(String::from(text))),
        }
    }
}

struct Iter<'parse> {
    lexer: Lexer<'parse, Token<'parse>>,
}

impl<'parse> std::iter::Iterator for Iter<'parse> {
    type Item = Value;

    fn next(&mut self) -> Option<Self::Item> {
        match self.lexer.next() {
            Some(Ok(token)) => Value::try_from(token).ok(),
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
struct Element {
    root: Tags,
    children: Vec<DomChild>,
}

/// Either a childless or a regular Element node
#[derive(Debug, PartialEq)]
enum DomChild {
    Leaf(Value),
    Node(Element),
}

impl Element {
    fn new(tag: Tags) -> Self {
        Self {
            root: tag,
            children: vec![],
        }
    }

    fn append(&mut self, value: DomChild) {
        self.children.push(value);
    }

    fn populate<'parse>(input: &'parse str) -> Option<Self> {
        let mut lexer = Iter::from(input);

        let Some(val) = lexer.next() else { return None };

        let mut dom = match val {
            Value::Tag(tag) => Self::new(tag.inner),
            _ => {
                return None;
            }
        };

        while let Some(value) = lexer.next() {
            match value {
                Value::Tag(tag) => match tag.kind {
                    TagKind::Close => {}
                    _ => {
                        let child_node = Self::populate_from(&mut lexer, tag);
                        dom.append(child_node);
                    }
                },
                other => dom.append(DomChild::Leaf(other)),
            }
        }

        Some(dom)
    }

    fn populate_from<'parse>(lexer: &mut Iter<'parse>, root: Tag) -> DomChild {
        let mut dom = Self::new(root.inner);

        while let Some(value) = lexer.next() {
            match value {
                Value::Tag(tag) => match tag.kind {
                    TagKind::Open => {
                        let child_node = Self::populate_from(lexer, tag);
                        dom.append(child_node);
                    }
                    TagKind::SelfClosing => {
                        dom.append(DomChild::Leaf(Value::Tag(tag)));
                    }
                    TagKind::Close => {
                        if tag.inner == root.inner {
                            return DomChild::Node(dom);
                        } else {
                            panic!("Tag mismatch: {} != {}", tag, root);
                        }
                    }
                },
                other => dom.append(DomChild::Leaf(other)),
            }
        }

        DomChild::Node(dom)
    }
}

#[pyclass]
struct Parser {}

#[pymethods]
impl Parser {
    #[staticmethod]
    fn parse(input: &str) -> Option<Element> {
        Element::populate(input)
    }

    #[staticmethod]
    fn inspect(el: &Element) -> String {
        format!("{:#?}", el)
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn raksha(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Parser>()?;
    Ok(())
}
