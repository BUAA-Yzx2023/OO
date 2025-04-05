//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

package com.oocourse.elevator2;

import java.math.BigInteger;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class PersonRequest extends Request {
    private final String fromFloor;
    private final String toFloor;
    private final int personId;
    private final int priority;
    private static final String PARSE_PATTERN_STRING = "^(?<personId>\\d+)-PRI-(?<priority>\\d+)-FROM-(?<fromFloor>[BF]\\d+)-TO-(?<toFloor>[BF]\\d+)";
    private static final Pattern PARSE_PATTERN = Pattern.compile("^(?<personId>\\d+)-PRI-(?<priority>\\d+)-FROM-(?<fromFloor>[BF]\\d+)-TO-(?<toFloor>[BF]\\d+)");
    private static final BigInteger INT_MAX = BigInteger.valueOf(2147483647L);
    private static final BigInteger INT_MIN = BigInteger.valueOf(-2147483648L);

    private static boolean isValidPriority(Integer priority) {
        return priority != null && priority >= 1 && priority <= 100;
    }

    private static boolean isInvalidFloor(String floor) {
        if (floor == null) {
            return true;
        } else if (floor.length() != 2) {
            return true;
        } else if (floor.charAt(0) == 'B') {
            return floor.charAt(1) < '1' || floor.charAt(1) > '4';
        } else if (floor.charAt(0) != 'F') {
            return true;
        } else {
            return floor.charAt(1) < '1' || floor.charAt(1) > '7';
        }
    }

    public PersonRequest(String fromFloor, String toFloor, int personId, int priority) {
        this.fromFloor = fromFloor;
        this.toFloor = toFloor;
        this.personId = personId;
        this.priority = priority;
    }

    public String getFromFloor() {
        return this.fromFloor;
    }

    public String getToFloor() {
        return this.toFloor;
    }

    public int getPersonId() {
        return this.personId;
    }

    public int getPriority() {
        return this.priority;
    }

    public String toString() {
        return String.format("%d-PRI-%d-FROM-%s-TO-%s", this.personId, this.priority, this.fromFloor, this.toFloor);
    }

    public int hashCode() {
        return Arrays.hashCode(new Object[]{this.fromFloor, this.toFloor, this.personId, this.priority});
    }

    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        } else if (!(obj instanceof PersonRequest)) {
            return false;
        } else {
            PersonRequest req = (PersonRequest)obj;
            return req.fromFloor.equals(this.fromFloor) && req.toFloor.equals(this.toFloor) && req.personId == this.personId && req.priority == this.priority;
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

    static PersonRequest parse(String string) throws RequestException {
        Matcher matcher = PARSE_PATTERN.matcher(string);
        matcher.matches();
        String personIdString = matcher.group("personId");
        Integer personId = toValidInteger(personIdString);
        if (personId == null) {
            throw new InvalidIdException(string);
        } else {
            String fromFloorString = matcher.group("fromFloor");
            if (isInvalidFloor(fromFloorString)) {
                throw new InvalidFromFloorException(string);
            } else {
                String toFloorString = matcher.group("toFloor");
                if (isInvalidFloor(toFloorString)) {
                    throw new InvalidToFloorException(string);
                } else if (fromFloorString.equals(toFloorString)) {
                    throw new DuplicatedFloorException(string);
                } else {
                    String priorityString = matcher.group("priority");
                    Integer priority = toValidInteger(priorityString);
                    if (!isValidPriority(priority)) {
                        throw new InvalidPriorityException(string);
                    } else {
                        return new PersonRequest(fromFloorString, toFloorString, personId, priority);
                    }
                }
            }
        }
    }
}
