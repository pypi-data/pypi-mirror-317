use std::borrow::Cow;

use serde_json::Value;

use crate::{Anchor, Draft, Error, Resolved, Resolver, Segments};

/// A document with a concrete interpretation under a JSON Schema specification.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Resource {
    contents: Value,
    draft: Draft,
}

impl Resource {
    pub(crate) fn new(contents: Value, draft: Draft) -> Self {
        Self { contents, draft }
    }
    /// Resource contents.
    #[must_use]
    pub fn contents(&self) -> &Value {
        &self.contents
    }
    /// JSON Schema draft under which this contents is interpreted.
    #[must_use]
    pub fn draft(&self) -> Draft {
        self.draft
    }
    /// Create a resource with automatically detecting specification which applies to the contents.
    ///
    /// # Errors
    ///
    /// On unknown `$schema` value it returns [`Error::UnknownSpecification`]
    pub fn from_contents(contents: Value) -> Result<Resource, Error> {
        Self::from_contents_and_specification(contents, Draft::default())
    }

    pub(crate) fn from_contents_and_specification(
        contents: Value,
        draft: Draft,
    ) -> Result<Resource, Error> {
        Ok(draft.detect(&contents)?.create_resource(contents))
    }
    /// Resource identifier.
    #[must_use]
    pub fn id(&self) -> Option<&str> {
        self.as_ref().id()
    }

    pub(crate) fn subresources(&self) -> Box<dyn Iterator<Item = Result<Resource, Error>> + '_> {
        Box::new(self.draft.subresources_of(&self.contents).map(|contents| {
            Resource::from_contents_and_specification(contents.clone(), self.draft)
        }))
    }

    pub(crate) fn anchors(&self) -> impl Iterator<Item = Anchor> + '_ {
        self.draft.anchors(&self.contents)
    }
    pub(crate) fn pointer<'r>(
        &'r self,
        pointer: &str,
        mut resolver: Resolver<'r>,
    ) -> Result<Resolved<'r>, Error> {
        // INVARIANT: Pointer always starts with `/`
        let mut contents = &self.contents;
        let mut segments = Segments::new();
        let original_pointer = pointer;
        let pointer = percent_encoding::percent_decode_str(&pointer[1..])
            .decode_utf8()
            .map_err(|err| Error::invalid_percent_encoding(original_pointer, err))?;
        for segment in pointer.split('/') {
            if let Some(array) = contents.as_array() {
                let idx = segment
                    .parse::<usize>()
                    .map_err(|err| Error::invalid_array_index(original_pointer, segment, err))?;
                if let Some(next) = array.get(idx) {
                    contents = next;
                } else {
                    return Err(Error::pointer_to_nowhere(original_pointer));
                }
                segments.push(idx);
            } else {
                let segment = unescape_segment(segment);
                if let Some(next) = contents.get(segment.as_ref()) {
                    contents = next;
                } else {
                    return Err(Error::pointer_to_nowhere(original_pointer));
                }
                segments.push(segment);
            }
            let last = &resolver;
            let new_resolver = self.draft.maybe_in_subresource(
                &segments,
                &resolver,
                self.draft.create_resource_ref(contents),
            )?;
            if new_resolver != *last {
                segments = Segments::new();
            }
            resolver = new_resolver;
        }
        Ok(Resolved::new(contents, resolver, self.draft()))
    }
    /// Give a reference to the underlying contents together with draft.
    #[must_use]
    pub fn as_ref(&self) -> ResourceRef<'_> {
        ResourceRef::new(&self.contents, self.draft)
    }
}

/// A reference to a document with a concrete interpretation under a JSON Schema specification.
#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub struct ResourceRef<'a> {
    contents: &'a Value,
    draft: Draft,
}

impl<'a> ResourceRef<'a> {
    /// Create a new resource reference.
    #[must_use]
    pub(crate) fn new(contents: &'a Value, draft: Draft) -> Self {
        ResourceRef { contents, draft }
    }
    /// Resource identifier.
    #[must_use]
    pub fn id(&self) -> Option<&'a str> {
        self.draft
            .id_of(self.contents)
            .map(|id| id.trim_end_matches('#'))
    }
    /// Resource contents.
    #[must_use]
    pub fn contents(&self) -> &'a Value {
        self.contents
    }
    #[must_use]
    pub fn draft(&self) -> Draft {
        self.draft
    }
}

fn unescape_segment(mut segment: &str) -> Cow<str> {
    // Naively, checking for `~` and then replacing implies two passes
    // over the input buffer. First, search in the first `contains('~')` call
    // and then replacing `~1` & `~0` at once in a single pass.
    //
    // This implementation is ~3x faster than the naive one.
    //
    // **NOTE**: Heavily inspired by the implementation in `boon`:
    // `https://github.com/santhosh-tekuri/boon/blob/fb09df2db19be75c32c0970b4bdedf1655f5f943/src/util.rs#L31`
    let Some(mut tilde_idx) = segment.find('~') else {
        return Cow::Borrowed(segment);
    };

    let mut buffer = String::with_capacity(segment.len());
    loop {
        let (before, after) = segment.split_at(tilde_idx);
        buffer.push_str(before);
        segment = &after[1..];
        let next_char_size = match segment.chars().next() {
            Some('1') => {
                buffer.push('/');
                1
            }
            Some('0') => {
                buffer.push('~');
                1
            }
            Some(next) => {
                buffer.push('~');
                buffer.push(next);
                next.len_utf8()
            }
            None => {
                buffer.push('~');
                break;
            }
        };
        segment = &segment[next_char_size..];
        let Some(next_tilde_idx) = segment.find('~') else {
            buffer.push_str(segment);
            break;
        };
        tilde_idx = next_tilde_idx;
    }
    Cow::Owned(buffer)
}

#[cfg(test)]
mod tests {
    use std::error::Error;

    use crate::{Draft, Registry};

    use super::unescape_segment;
    use serde_json::json;
    use test_case::test_case;

    #[test_case("abc")]
    #[test_case("a~0b")]
    #[test_case("a~1b")]
    #[test_case("~01")]
    #[test_case("~10")]
    #[test_case("a~0~1b")]
    #[test_case("~"; "single tilde")]
    #[test_case("~~"; "double tilde")]
    #[test_case("~~~~~"; "many tildas")]
    #[test_case("~2")]
    #[test_case("a~c")]
    #[test_case("~0~1~")]
    #[test_case("")]
    #[test_case("a/d")]
    #[test_case("a~01b")]
    #[test_case("🌟~0🌠~1🌡️"; "Emojis with escapes")]
    #[test_case("~🌟"; "Tilde followed by emoji")]
    #[test_case("Café~0~1"; "Accented characters with escapes")]
    #[test_case("~é"; "Tilde followed by accented character")]
    #[test_case("αβγ"; "Greek")]
    #[test_case("~αβγ"; "Tilde followed by Greek")]
    #[test_case("∀∂∈ℝ∧∪≡∞"; "Mathematical symbols")]
    #[test_case("~∀∂∈ℝ∧∪≡∞"; "Tilde followed by mathematical symbols")]
    #[test_case("¡¢£¤¥¦§¨©"; "Special characters")]
    #[test_case("~¡¢£¤¥¦§¨©"; "Tilde followed by special characters")]
    #[test_case("\u{10FFFF}"; "Highest valid Unicode code point")]
    #[test_case("~\u{10FFFF}"; "Tilde followed by highest valid Unicode code point")]
    fn test_unescape_segment_equivalence(input: &str) {
        let unescaped = unescape_segment(input);
        let double_replaced = input.replace("~1", "/").replace("~0", "~");
        assert_eq!(unescaped, double_replaced, "Failed for: {input}");
    }

    fn create_test_registry() -> Registry {
        let schema = Draft::Draft202012.create_resource(json!({
            "type": "object",
            "properties": {
                "foo": { "type": "string" },
                "bar": { "type": "array", "items": [{"type": "number"}, {"type": "boolean"}] }
            }
        }));
        Registry::try_new("http://example.com", schema).expect("Invalid resources")
    }

    #[test]
    fn test_empty_ref() {
        let schema = Draft::Draft202012.create_resource(json!({
            "type": "object",
            "properties": {
                "foo": { "type": "string" }
            }
        }));
        let registry =
            Registry::try_new("http://example.com", schema.clone()).expect("Invalid resources");
        let resolver = registry
            .try_resolver("http://example.com")
            .expect("Invalid base URI");

        let resolved = resolver.lookup("#").expect("Lookup failed");
        assert_eq!(resolved.contents(), &schema.contents);
    }

    #[test]
    fn test_percent_encoded_non_utf8() {
        let registry = create_test_registry();
        let resolver = registry
            .try_resolver("http://example.com")
            .expect("Invalid base URI");

        let result = resolver.lookup("#/%FF");
        let error = result.expect_err("Should fail");
        assert_eq!(
            error.to_string(),
            "Invalid percent encoding in pointer '/%FF': the decoded bytes do not represent valid UTF-8"
        );
        assert!(error.source().is_some());
    }

    #[test]
    fn test_array_index_as_string() {
        let registry = create_test_registry();
        let resolver = registry
            .try_resolver("http://example.com")
            .expect("Invalid base URI");

        let result = resolver.lookup("#/properties/bar/items/one");
        let error = result.expect_err("Should fail");
        assert_eq!(
            error.to_string(),
            "Failed to parse array index 'one' in pointer '/properties/bar/items/one'"
        );
        assert!(error.source().is_some());
    }

    #[test]
    fn test_array_index_out_of_bounds() {
        let registry = create_test_registry();
        let resolver = registry
            .try_resolver("http://example.com")
            .expect("Invalid base URI");

        let result = resolver.lookup("#/properties/bar/items/2");
        assert_eq!(
            result.expect_err("Should fail").to_string(),
            "Pointer '/properties/bar/items/2' does not exist"
        );
    }

    #[test]
    fn test_unknown_property() {
        let registry = create_test_registry();
        let resolver = registry
            .try_resolver("http://example.com")
            .expect("Invalid base URI");

        let result = resolver.lookup("#/properties/baz");
        assert_eq!(
            result.expect_err("Should fail").to_string(),
            "Pointer '/properties/baz' does not exist"
        );
    }
}
