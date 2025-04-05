package com.oocourse.elevator2;

class InvalidIdException extends RequestException {
    InvalidIdException(String original) {
        super(original);
    }
}