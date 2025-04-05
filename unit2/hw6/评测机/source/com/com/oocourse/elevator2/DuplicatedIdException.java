package com.oocourse.elevator2;

class DuplicatedIdException extends RequestException {
    DuplicatedIdException(String original) {
        super(original);
    }
}
