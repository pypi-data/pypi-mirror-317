use crate::{
    compiler,
    error::ValidationError,
    keywords::{helpers::fail_on_non_positive_integer, CompilationResult},
    paths::{LazyLocation, Location},
    validator::Validate,
};
use serde_json::{Map, Value};

pub(crate) struct MinLengthValidator {
    limit: u64,
    location: Location,
}

impl MinLengthValidator {
    #[inline]
    pub(crate) fn compile<'a>(
        ctx: &compiler::Context,
        schema: &'a Value,
        location: Location,
    ) -> CompilationResult<'a> {
        if let Some(limit) = schema.as_u64() {
            return Ok(Box::new(MinLengthValidator { limit, location }));
        }
        if ctx.supports_integer_valued_numbers() {
            if let Some(limit) = schema.as_f64() {
                if limit.trunc() == limit {
                    #[allow(clippy::cast_possible_truncation)]
                    return Ok(Box::new(MinLengthValidator {
                        // NOTE: Imprecise cast as big integers are not supported yet
                        limit: limit as u64,
                        location,
                    }));
                }
            }
        }
        Err(fail_on_non_positive_integer(schema, location))
    }
}

impl Validate for MinLengthValidator {
    fn is_valid(&self, instance: &Value) -> bool {
        if let Value::String(item) = instance {
            if (bytecount::num_chars(item.as_bytes()) as u64) < self.limit {
                return false;
            }
        }
        true
    }

    fn validate<'i>(
        &self,
        instance: &'i Value,
        location: &LazyLocation,
    ) -> Result<(), ValidationError<'i>> {
        if let Value::String(item) = instance {
            if (bytecount::num_chars(item.as_bytes()) as u64) < self.limit {
                return Err(ValidationError::min_length(
                    self.location.clone(),
                    location.into(),
                    instance,
                    self.limit,
                ));
            }
        }
        Ok(())
    }
}

#[inline]
pub(crate) fn compile<'a>(
    ctx: &compiler::Context,
    _: &'a Map<String, Value>,
    schema: &'a Value,
) -> Option<CompilationResult<'a>> {
    let location = ctx.location().join("minLength");
    Some(MinLengthValidator::compile(ctx, schema, location))
}

#[cfg(test)]
mod tests {
    use crate::tests_util;
    use serde_json::json;

    #[test]
    fn location() {
        tests_util::assert_schema_location(&json!({"minLength": 1}), &json!(""), "/minLength")
    }
}
