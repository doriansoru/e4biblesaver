use easy_reader::EasyReader;
use std::{
    fs::File,
    io::Error,
};
use pyo3::prelude::*;

fn get_verse() -> Result<String, Error> {
    let max_verse_line_len = 40;
    let separator = "|";

    let bible = File::open(include!("bible.h"))?;
    let mut reader = EasyReader::new(bible)?;

    //Select the verse
    let verse = reader.random_line()?.unwrap();

    let fields: Vec<&str> = verse.split(separator).collect();

    //fields[0] = book name; fields[1] = chapter number; fields[2] = verse number; fields[3] = verse text
    let mut formatted_verse: String = format!("[{} {}:{}] {}", &(fields[0]).trim(), &(fields[1]).trim(), &(fields[2]).trim(), &(fields[3]).trim());
    
    //Format the verse to max max_verse_line_len characters
    //by adding \n
    let cloned_verse = formatted_verse.clone();
    let mut i: usize = 0;
    formatted_verse = String::from("");
    for word in cloned_verse.split_whitespace() {
        let count: usize = word.chars().count();
        if (i + count) > max_verse_line_len {
            formatted_verse.push_str("\n");
            i = 0;
        } else {
            i += count;
        }
        formatted_verse.push_str(word);
        formatted_verse.push_str(" ");
    }

    Ok(formatted_verse)
}

#[pymodule]
fn e4biblelib(_py: Python, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    #[pyo3(name="get_verse")]
    fn get_verse_py(_py: Python) -> PyResult<String> {
        let formatted_verse = get_verse();
        Ok(formatted_verse.unwrap())
    }

    Ok(())
}