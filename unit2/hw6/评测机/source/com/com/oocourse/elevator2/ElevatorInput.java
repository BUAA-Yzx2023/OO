package com.oocourse.elevator2;

import java.io.Closeable;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashSet;
import java.util.Scanner;

public class ElevatorInput implements Closeable {
    private final Scanner scanner;
    private final HashSet<Integer> existedPersonId = new HashSet();

    public ElevatorInput(InputStream inputStream) {
        this.scanner = new Scanner(inputStream);
    }

    public static int getVersion() {
        return 2;
    }

    public void close() throws IOException {
        this.scanner.close();
    }

    public Request nextRequest() {
        while(this.scanner.hasNextLine()) {
            String line = this.scanner.nextLine();
            RequestException e;
            if (PersonRequest.matches(line)) {
                try {
                    PersonRequest request = PersonRequest.parse(line);
                    if (this.existedPersonId.contains(request.getPersonId())) {
                        throw new DuplicatedIdException(line);
                    }

                    this.existedPersonId.add(request.getPersonId());
                    return request;
                } catch (RequestException var3) {
                    e = var3;
                    e.printStackTrace(System.err);
                }
            } else if (ScheRequest.matches(line)) {
                try {
                    ScheRequest request = ScheRequest.parse(line);
                    if (request.getElevatorId() >= 1 && request.getElevatorId() <= 6) {
                        TimableOutput.println(request.toString());
                        return request;
                    }

                    throw new InvalidElevatorIdException(line);
                } catch (RequestException var4) {
                    e = var4;
                    e.printStackTrace(System.err);
                }
            } else {
                try {
                    throw new InvalidRequestException("Illegal Request: " + line);
                } catch (InvalidRequestException var5) {
                    InvalidRequestException e1 = var5;
                    e1.printStackTrace(System.err);
                }
            }
        }

        return null;
    }
}
