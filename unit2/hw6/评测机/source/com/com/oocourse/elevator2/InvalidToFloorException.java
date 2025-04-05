package com.oocourse.elevator2;

class InvalidToFloorException extends RequestException {
    InvalidToFloorException(String original) {
        super(original);
    }
}