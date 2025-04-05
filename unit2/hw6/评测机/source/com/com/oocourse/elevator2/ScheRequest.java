//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package com.oocourse.elevator2;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ScheRequest extends Request {
    private final int elevatorId;
    private final double speed;
    private final String toFloor;
    private static final String PARSE_PATTERN_STRING = "^SCHE-(?<elevatorId>\\d+)-(?<speed>0.\\d+)-(?<toFloor>[BF]\\d+)";
    private static final Pattern PARSE_PATTERN = Pattern.compile("^SCHE-(?<elevatorId>\\d+)-(?<speed>0.\\d+)-(?<toFloor>[BF]\\d+)");
    private static final BigInteger INT_MAX = BigInteger.valueOf(2147483647L);
    private static final BigInteger INT_MIN = BigInteger.valueOf(-2147483648L);

    private static boolean isInvalidFloor(String floor) {
        if (floor == null) {
            return true;
        } else if (floor.length() != 2) {
            return true;
        } else if (floor.charAt(0) == 'B') {
            return floor.charAt(1) < '1' || floor.charAt(1) > '2';
        } else if (floor.charAt(0) != 'F') {
            return true;
        } else {
            return floor.charAt(1) < '1' || floor.charAt(1) > '5';
        }
    }

    private static boolean isInvalidSpeed(String speed) {
        if (speed == null) {
            return true;
        } else {
            try {
                double d = Double.parseDouble(speed);
                return d != 0.2 && d != 0.3 && d != 0.4 && d != 0.5;
            } catch (Exception var3) {
                return true;
            }
        }
    }

    public ScheRequest(int elevatorId, double speed, String toFloor) {
        this.elevatorId = elevatorId;
        this.speed = speed;
        this.toFloor = toFloor;
    }

    public int getElevatorId() {
        return this.elevatorId;
    }

    public double getSpeed() {
        return this.speed;
    }

    public String getToFloor() {
        return this.toFloor;
    }

    public String toString() {
        return String.format("SCHE-ACCEPT-%d-%.1f-%s", this.elevatorId, this.speed, this.toFloor);
    }

    public int hashCode() {
        return Arrays.hashCode(new Object[]{this.elevatorId, this.speed, this.toFloor});
    }

    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        } else if (!(obj instanceof ScheRequest)) {
            return false;
        } else {
            ScheRequest req = (ScheRequest)obj;
            return this.elevatorId == req.elevatorId && this.speed == req.speed && this.toFloor.equals(req.toFloor);
        }
    }

    private static boolean isValidInteger(String string) {
        try {
            BigInteger integer = new BigInteger(string);
            return integer.compareTo(INT_MAX) <= 0 && integer.compareTo(INT_MIN) >= 0;
        } catch (Exception var2) {
            return false;
        }
    }

    private static Integer toValidInteger(String string) {
        return isValidInteger(string) ? (new BigInteger(string)).intValue() : null;
    }

    static boolean matches(String string) {
        Matcher matcher = PARSE_PATTERN.matcher(string);
        return matcher.matches();
    }

    static ScheRequest parse(String string) throws RequestException {
        Matcher matcher = PARSE_PATTERN.matcher(string);
        matcher.matches();
        String elevatorIdString = matcher.group("elevatorId");
        Integer elevatorId = toValidInteger(elevatorIdString);
        if (elevatorId == null) {
            throw new InvalidIdException(string);
        } else {
            String speedString = matcher.group("speed");
            if (isInvalidSpeed(speedString)) {
                throw new InvalidSpeedException(string);
            } else {
                String toFloorString = matcher.group("toFloor");
                if (isInvalidFloor(toFloorString)) {
                    throw new InvalidToFloorException(string);
                } else {
                    double speed = Double.parseDouble(speedString);
                    return new ScheRequest(elevatorId, speed, toFloorString);
                }
            }
        }
    }
}
