1.  Identify one problem in the below code block, will this code compile? Discuss the related Rust feature regarding the problem you have identified, why does Rust choose to include this feature? A few sentences are good enough.

    ```rust
        let data = vec![1, 2, 3];
        let my_ref_cell = RefCell::new(69);
        let ref_to_ref_cell = &my_ref_cell;

        std::thread::spawn(move || {

            println!("captured {data:?} by value");

            println!("Whats in the cell?? {ref_to_ref_cell:?}")

        }).join().unwrap();
    ```

    A: This code attempts to move a reference to a RefCell into a thread, but RefCell is not Sync, so this is
    not possible. Rust uses the Send and Sync traits to indicate the thread safety of types, and in this case
    the unsynchronized interior mutability of RefCell makes it thread-unsafe. More specifically, it cannot be
    safely referenced by multiple threads, making it not Sync. It can however, be sent across threads, so it
    is still Send.

2.  Shortly discuss, when modelling a response to a HTTP request in Rust, would you prefer to use `Option` or `Result`?

    A: A response to an HTTP request primarily contains data along with a status code, which could be an error.
    If one had to be chosen over the other, Result would be more appropriate as it allows for indicating what
    kind of error may have occurred, rather than simply the presence or absence of a response as would be implied
    with Option.

3.  In `student.psv` there are some fake student datas from UNSW CSE (no doxx!). In each row, the fields from left to right are

    - UNSW Course Code
    - UNSW Student Number
    - Name
    - UNSW Program
    - UNSW Plan
    - WAM
    - UNSW Session
    - Birthdate
    - Sex

    Write a Rust program to find the course which has the highest average student WAM. **Write your program in the cargo project q3**.

