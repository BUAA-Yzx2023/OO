import java.math.BigInteger;
import java.util.HashMap;

public class Monomial {
    private BigInteger coeff;
    private int index;
    private HashMap<Polymial, Integer> sinFacs;
    private HashMap<Polymial, Integer> cosFacs;

    public Monomial(BigInteger coeff, int index) {
        this.coeff = coeff;
        this.index = index;
        this.sinFacs = new HashMap<>();
        this.cosFacs = new HashMap<>();
    }

    public BigInteger getCoeff() {
        return coeff;
    }

    public void setCoeff(BigInteger coeff) {
        this.coeff = coeff;
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }

    public void addSinFac(Polymial fac, int index) {
        for (Polymial thisfac : this.sinFacs.keySet()) {
            if (thisfac.equals(fac)) {
                this.sinFacs.put(thisfac, this.sinFacs.get(thisfac) + index);
                return;
            }
        }
        this.sinFacs.put(fac, index);
    }

    public void addCosFac(Polymial fac, int index) {
        for (Polymial thisfac : this.cosFacs.keySet()) {
            if (thisfac.equals(fac)) {
                this.cosFacs.put(thisfac, this.cosFacs.get(thisfac) + index);
                return;
            }
        }
        this.cosFacs.put(fac, index);
    }

    public boolean equals(Monomial other) {
        if (this.index != other.index) {
            return false;
        }
        if (this.sinFacs.size() != other.sinFacs.size()
            || this.cosFacs.size() != other.cosFacs.size()) {
            return false;
        }
        HashMap<Polymial, Integer> sin = new HashMap();
        for (Polymial fac : other.getSinFacs().keySet()) {
            sin.put(fac, other.getSinFacs().get(fac));
        }
        for (Polymial fac1 : this.sinFacs.keySet()) {
            Polymial fac3 = null;
            for (Polymial fac2 : sin.keySet()) {
                if (this.sinFacs.get(fac1).equals(sin.get(fac2))) {
                    if (fac1.equals(fac2)) {
                        fac3 = fac2;
                        break;
                    }
                }
            }
            if (fac3 == null) {
                return false;
            } else {
                sin.remove(fac3);
            }
        }
        HashMap<Polymial, Integer> cos = new HashMap<>();
        for (Polymial fac : other.getCosFacs().keySet()) {
            cos.put(fac, other.getCosFacs().get(fac));
        }
        for (Polymial fac1 : this.cosFacs.keySet()) {
            Polymial fac3 = null;
            for (Polymial fac2 : cos.keySet()) {
                if (this.cosFacs.get(fac1) == cos.get(fac2)) {
                    if (fac1.equals(fac2)) {
                        fac3 = fac2;
                        break;
                    }
                }
            }
            if (fac3 == null) {
                return false;
            } else {
                cos.remove(fac3);
            }
        }
        boolean b = sin.size() == 0 && cos.size() == 0;
        return b;
    }

    public Monomial mult(Monomial m1, Monomial m2) {
        Monomial res = new Monomial(BigInteger.ZERO, 0);
        res.setCoeff(m1.getCoeff().multiply(m2.getCoeff()));
        res.setIndex(m1.getIndex() + m2.getIndex());
        for (Polymial fac : m1.sinFacs.keySet()) {
            res.addSinFac(fac, m1.sinFacs.get(fac));
        }
        for (Polymial fac : m2.sinFacs.keySet()) {
            res.addSinFac(fac, m2.sinFacs.get(fac));
        }
        for (Polymial fac : m1.cosFacs.keySet()) {
            res.addCosFac(fac, m1.cosFacs.get(fac));
        }
        for (Polymial fac : m2.cosFacs.keySet()) {
            res.addCosFac(fac, m2.cosFacs.get(fac));
        }
        return res;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        if (coeff.compareTo(BigInteger.ZERO) == 0) {
            return "";
        } else if (this.index == 0 && this.sinFacs.size() == 0 && this.cosFacs.size() == 0) {
            sb.append(coeff);
            return sb.toString();
        } else {
            if (coeff.compareTo(BigInteger.ONE.negate()) == 0) {
                sb.append("-");
            } else if (coeff.compareTo(BigInteger.ONE) != 0) {
                sb.append(coeff);
                sb.append("*");
            }
            if (this.index != 0) {
                sb.append("x");
                if (this.index != 1) {
                    sb.append("^");
                    sb.append(this.index);
                }
                sb.append("*");
            }
            for (Polymial fac : this.sinFacs.keySet()) {
                sb.append("sin(");
                String s = fac.toString();
                if (fac.getSize() > 1) {
                    sb.append("(" + s + ")");
                } else {
                    sb.append(s);
                }
                sb.append(")");
                if (this.sinFacs.get(fac) != 1) {
                    sb.append("^");
                    sb.append(this.sinFacs.get(fac));
                }
                sb.append("*");
            }
            for (Polymial fac : this.cosFacs.keySet()) {
                sb.append("cos(");
                String s = fac.toString();
                if (fac.getSize() > 1) {
                    sb.append("(" + s + ")");
                } else {
                    sb.append(s);
                }
                sb.append(")");
                if (this.cosFacs.get(fac) != 1) {
                    sb.append("^");
                    sb.append(this.cosFacs.get(fac));
                }
                sb.append("*");
            }
            if (sb.charAt(sb.length() - 1) == '*') {
                sb.deleteCharAt(sb.length() - 1);
            }
            return sb.toString();
        }
    }

    public HashMap<Polymial, Integer> getCosFacs() {
        return cosFacs;
    }

    public HashMap<Polymial, Integer> getSinFacs() {
        return sinFacs;
    }

    public int getSize() {
        int size = 0;
        if (this.getCoeff().compareTo(BigInteger.ZERO) != 0
            && this.getCoeff().compareTo(BigInteger.ONE) != 0) {
            size++;
        }
        if (this.index != 0) {
            size++;
        }
        size += this.sinFacs.size() + this.cosFacs.size();
        if (size == 0) {
            size++;
        }
        return size;
    }
}
