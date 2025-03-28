import java.math.BigInteger;
import java.util.HashSet;

public class Expr implements Factor {
    private final HashSet<Term> terms;
    private int index;

    public Expr() {
        this.index = 1;
        this.terms = new HashSet<>();
    }

    public int getIndex() {
        return index;
    }

    public void setIndex(int index) {
        this.index = index;
    }

    public void addTerm(Term term) {
        this.terms.add(term);
    }

    public String toString() {
        Polymial temPoly = this.toPoly();
        Polymial poly = new Polymial();
        //取一个系数为正的项放在首项，其余随便
        Monomial mono = null;
        for (Monomial monomial : temPoly.getPolymial()) {
            if (monomial.getCoeff().compareTo(BigInteger.ZERO) > 0) {
                poly.addMonomial(monomial);
                mono = monomial;
                break;
            }
        }
        temPoly.getPolymial().remove(mono);
        for (Monomial monomial : temPoly.getPolymial()) {
            poly.addMonomial(monomial);
        }

        StringBuilder sb = new StringBuilder();
        //输出多项式
        for (Monomial monomial : poly.getPolymial()) {
            if (monomial.getCoeff().compareTo(BigInteger.ZERO) == 0) {
                continue;
            } else if (monomial.getCoeff().compareTo(BigInteger.ZERO) > 0) {
                sb.append("+");
            }
            if (monomial.getIndex() == 0) {
                sb.append(monomial.getCoeff());
            } else if (monomial.getIndex() == 1) {
                if (monomial.getCoeff().compareTo(BigInteger.ONE) != 0) {
                    if (monomial.getCoeff().compareTo(BigInteger.ONE.negate()) != 0) {
                        sb.append(monomial.getCoeff());
                        sb.append("*");
                    } else {
                        sb.append("-");
                    }
                }
                sb.append("x");
            } else {
                if (monomial.getCoeff().compareTo(BigInteger.ONE) != 0) {
                    if (monomial.getCoeff().compareTo(BigInteger.ONE.negate()) != 0) {
                        sb.append(monomial.getCoeff());
                        sb.append("*");
                    } else {
                        sb.append("-");
                    }
                }
                sb.append("x^");
                sb.append(monomial.getIndex());
            }
        }
        if (sb.length() == 0) {
            sb.append("0");
        } else if (sb.charAt(0) == '+') {
            sb.deleteCharAt(0);
        }
        return sb.toString();
    }

    @Override
    public Polymial toPoly() {
        Polymial temPoly = new Polymial();
        for (Term term : terms) {
            temPoly = temPoly.addPoly(temPoly, term.toPoly());
        }
        Polymial poly = new Polymial();
        poly.addMonomial(new Monomial(BigInteger.ONE, 0));
        for (int i = 0; i < index; i++) {
            poly = poly.multPoly(poly, temPoly);
        }
        return poly;
    }
}
