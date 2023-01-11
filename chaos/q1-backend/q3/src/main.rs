// q3
// In `student.psv` there are some fake student datas from UNSW CSE (no doxx!). In each row, the fields from left to right are
//
// - UNSW Course Code
// - UNSW Student Number
// - Name
// - UNSW Program
// - UNSW Plan
// - WAM
// - UNSW Session
// - Birthdate
// - Sex
// 
// Write a Rust program to find the course which has the highest average student WAM.

use std::collections::HashMap;
use std::io::{BufRead, BufReader};
use std::fs::File;

fn main() {
    let mut course_marks = HashMap::<String, (u32, f32)>::new();

    let reader = BufReader::new(File::open("../student.psv").unwrap());

    for line in reader.lines() {
        let line = line.unwrap();
        let mut student_data = line.split('|');
        let course = student_data.nth(0).unwrap();
        let wam = student_data.nth(4).unwrap().parse::<f32>().unwrap();

        match course_marks.get_mut(course) {
            Some(marks) => {
                marks.0 += 1;
                marks.1 += wam;
            },
            None => {
                course_marks.insert(course.to_owned(), (1, wam));
            },
        }
    }

    let mut best_course = "";
    let mut best_wam_avg = -0.1;

    for course in course_marks.iter() {
        let mark_info = course.1;
        let wam_avg = mark_info.1 / mark_info.0 as f32;

        if best_wam_avg <= wam_avg {
            best_wam_avg = wam_avg;
            best_course = course.0;
        }
    }

    println!("{} has the highest average WAM, which is {}", best_course, best_wam_avg);
}
