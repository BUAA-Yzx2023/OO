package com.oocourse.elevator2;

class DuplicatedFloorException extends RequestException {
    DuplicatedFloorException(String original) {
        super(original);
    }
}