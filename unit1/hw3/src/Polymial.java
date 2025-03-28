import java.math.BigInteger;
import java.util.ArrayList;

public class Polymial {
    private ArrayList<Monomial> polymial;

    public Polymial() {
        this.polymial = new ArrayList<Monomial>();
    }

    public void addMonomial(Monomial monomial) {
        for (Monomial m : this.polymial) {
            if (m.equals(monomial)) {
                m.setCoeff(m.getCoeff().add(monomial.getCoeff()));
                return;
            }
        }
        this.polymial.add(monomial);
    }

    public Polymial addPoly(Polymial p1, Polymial p2) {
        Polymial result = new Polymial();
        for (Monomial mono : p1.polymial) {
            result.addMonomial(mono);
        }
        for (Monomial mono : p2.polymial) {
            result.addMonomial(mono);
        }
        return result;
    }

    public Polymial multPoly(Polymial p1, Polymial p2) {
        Polymial result = new Polymial();
        for (Monomial monoP1 : p1.polymial) {
            for (Monomial monoP2 : p2.polymial) {
                // 创建一个新的单项式
                Monomial newMono = monoP1.mult(monoP1, monoP2);
                result.addMonomial(newMono);
            }
        }
        return result;
    }

    public ArrayList<Monomial> getPolymial() {
        return polymial;
    }

    @Override
    public String toString() {
        Polymial poly = new Polymial();
        //取一个系数为正的项放在首项，其余随便
        Monomial mono = null;
        for (Monomial monomial : this.polymial) {
            if (monomial.getCoeff().compareTo(BigInteger.ZERO) > 0) {
                poly.addMonomial(monomial);
                mono = monomial;
                break;
            }
        }
        for (Monomial monomial : this.polymial) {
            if (mono != null && monomial == mono) {
                continue;
            }
            poly.addMonomial(monomial);
        }

        StringBuilder sb = new StringBuilder();
        for (Monomial monomial : poly.getPolymial()) {
            if (monomial.getCoeff().compareTo(BigInteger.ZERO) > 0) {
                sb.append("+");
            }
            sb.append(monomial.toString());
        }

        if (sb.length() == 0) {
            sb.append("0");
        } else if (sb.charAt(0) == '+') {
            sb.deleteCharAt(0);
        }
        return sb.toString();
    }

    public boolean equals(Polymial other) {
        if (this.polymial.size() != other.polymial.size()) {
            return false;
        }
        Polymial poly = new Polymial();
        for (Monomial monomial : other.getPolymial()) {
            poly.addMonomial(monomial);
        }
        for (Monomial m1 : this.polymial) {
            Monomial m3 = null;
            for (Monomial m2 : poly.getPolymial()) {
                if (m1.equals(m2) && m1.getCoeff().compareTo(m2.getCoeff()) == 0) {
                    m3 = m2;
                    break;
                }
            }
            if (m3 == null) {
                return false;
            } else {
                poly.getPolymial().remove(m3);
            }
        }
        return true;
    }

    public int getSize() {
        int size = 0;
        for (Monomial mono : this.polymial) {
            if (mono.getCoeff().compareTo(BigInteger.ZERO) != 0) {
                size += mono.getSize();
            }
        }
        return size;
    }
}
