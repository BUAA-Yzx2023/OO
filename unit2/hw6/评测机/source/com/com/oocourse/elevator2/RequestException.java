//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package com.oocourse.elevator2;

abstract class RequestException extends Exception {
    RequestException(String original) {
        super(String.format("Person request parse failed! - \"%s\"", original));
    }
}
