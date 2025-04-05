package com.oocourse.elevator2;

class InvalidRequestException extends Exception {
    private final String original;

    InvalidRequestException(String original) {
        super(String.format("Invalid input! - \"%s\"", original));
        this.original = original;
    }

    public String getOriginal() {
        return this.original;
    }
}