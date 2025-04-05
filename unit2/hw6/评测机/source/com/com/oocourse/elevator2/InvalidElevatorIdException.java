package com.oocourse.elevator2;

class InvalidElevatorIdException extends RequestException {
    InvalidElevatorIdException(String original) {
        super(original);
    }
}