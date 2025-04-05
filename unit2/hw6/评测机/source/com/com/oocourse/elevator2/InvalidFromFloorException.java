package com.oocourse.elevator2;

class InvalidFromFloorException extends RequestException {
    InvalidFromFloorException(String original) {
        super(original);
    }
}
