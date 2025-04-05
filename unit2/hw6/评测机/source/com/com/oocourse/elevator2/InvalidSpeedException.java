package com.oocourse.elevator2;

class InvalidSpeedException extends RequestException {
    InvalidSpeedException(String original) {
        super(original);
    }
}