// Mostly taken from hg-core/src/matchers.rs
//
// Copyright 2019 Raphaël Gomès <rgomes@octobus.net>
// Copyright 2024 Georges Racinet <georges.racinet@octobus.net> for the minor adaptations
//
// This software may be used and distributed according to the terms of the
// GNU General Public License version 2 or any later version.
use hg::filepatterns::glob_to_re as glob_to_regex_bytes_pattern;
use regex::bytes::Regex;
use std::io::Write;

/// Convert a glob pattern into a regular expression
///
/// Taken from [`hg::matchers::re_matcher`] with the following changes:
///
///   - we don't need the multithread optimizations, hence to enclose with thread-locals
///     in `hg::matchers::RegexMatcher`.
///   - we don't need huge regexps, as the main use case in RHGitaly is `fnmatch` on path segments.
#[allow(rustdoc::broken_intra_doc_links)]
pub fn glob_to_regex(pat: &[u8]) -> Regex {
    let rx_pat = glob_to_regex_bytes_pattern(pat);
    let pattern = &rx_pat;

    // The `regex` crate adds `.*` to the start and end of expressions if there
    // are no anchors, so add the start anchor.
    let mut escaped_bytes = vec![b'^', b'(', b'?', b':'];
    for byte in pattern {
        if *byte > 127 {
            write!(escaped_bytes, "\\x{:x}", *byte).unwrap();
        } else {
            escaped_bytes.push(*byte);
        }
    }
    escaped_bytes.push(b')');

    // Avoid the cost of UTF8 checking
    //
    // # Safety
    // This is safe because we escaped all non-ASCII bytes.
    let pattern_string = unsafe { String::from_utf8_unchecked(escaped_bytes) };
    regex::bytes::RegexBuilder::new(&pattern_string)
        .unicode(false)
        .build()
        .unwrap() // TODO unwrap. In theory (must be checked) we cannot make a wrong regexp pattern
}
