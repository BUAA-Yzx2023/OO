package com.oocourse.elevator2;

class InvalidPriorityException extends RequestException {
    public InvalidPriorityException(String original) {
        super(original);
    }
}