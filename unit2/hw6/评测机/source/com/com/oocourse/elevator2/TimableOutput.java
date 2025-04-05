//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package com.oocourse.elevator2;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public abstract class TimableOutput {
    private static long startTimestamp = 0L;
    private static final String RANDOM_START_STRING = "This is random start string.";
    private static final PrintStream DEFAULT_PRINT_STREAM;

    public TimableOutput() {
    }

    public static synchronized void initStartTimestamp() {
        if (startTimestamp == 0L) {
            startTimestamp = System.currentTimeMillis();
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            PrintStream printStream = new PrintStream(stream);
            println((Object)"This is random start string.", printStream);
            printStream.close();
        }

    }

    private static long getRelativeTimestamp(long timestamp) {
        return timestamp - startTimestamp;
    }

    private static long getRelativeTimestamp() {
        return getRelativeTimestamp(System.currentTimeMillis());
    }

    private static long println(Object obj, PrintStream stream) {
        ObjectWithTimestamp value = new ObjectWithTimestamp(obj);
        stream.println(value);
        stream.flush();
        return value.getTimestamp();
    }

    public static synchronized long println(Object obj) {
        return println(obj, DEFAULT_PRINT_STREAM);
    }

    private static long println(int i, PrintStream stream) {
        return println((Object)String.valueOf(i), stream);
    }

    public static synchronized long println(int i) {
        return println(i, DEFAULT_PRINT_STREAM);
    }

    private static long println(boolean b, PrintStream stream) {
        return println((Object)String.valueOf(b), stream);
    }

    public static synchronized long println(boolean b) {
        return println(b, DEFAULT_PRINT_STREAM);
    }

    private static long println(char c, PrintStream stream) {
        return println((Object)String.valueOf(c), stream);
    }

    public static synchronized long println(char c) {
        return println(c, DEFAULT_PRINT_STREAM);
    }

    private static long println(long l, PrintStream stream) {
        return println((Object)String.valueOf(l), stream);
    }

    public static synchronized long println(long l) {
        return println(l, DEFAULT_PRINT_STREAM);
    }

    private static long println(float f, PrintStream stream) {
        return println((Object)String.valueOf(f), stream);
    }

    public static synchronized long println(float f) {
        return println(f, DEFAULT_PRINT_STREAM);
    }

    private static long println(char[] s, PrintStream stream) {
        return println((Object)String.valueOf(s), stream);
    }

    public static synchronized long println(char[] s) {
        return println(s, DEFAULT_PRINT_STREAM);
    }

    private static long println(double d, PrintStream stream) {
        return println((Object)String.valueOf(d), stream);
    }

    public static synchronized long println(double d) {
        return println(d, DEFAULT_PRINT_STREAM);
    }

    static {
        DEFAULT_PRINT_STREAM = System.out;
    }

    private static class ObjectWithTimestamp {
        private final long timestamp;
        private final Object object;

        ObjectWithTimestamp(long timestamp, Object object) {
            this.timestamp = timestamp;
            this.object = object;
        }

        ObjectWithTimestamp(Object object) {
            this(System.currentTimeMillis(), object);
        }

        public long getTimestamp() {
            return this.timestamp;
        }

        public long getRelativeTimestamp() {
            return TimableOutput.getRelativeTimestamp(this.getTimestamp());
        }

        public double getRelativeSecondTimestamp() {
            return (double)this.getRelativeTimestamp() / 1000.0;
        }

        public Object getObject() {
            return this.object;
        }

        public String toString() {
            return String.format("[%9.4f]%s", this.getRelativeSecondTimestamp(), this.getObject().toString());
        }
    }
}
