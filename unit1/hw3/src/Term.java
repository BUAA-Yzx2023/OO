import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashSet;

public class Term {
    private final HashSet<Factor> factors;
    private int sign;

    public Term(int sign) {
        this.sign = sign;
        this.factors = new HashSet<>();
    }

    public String getType() {
        return "term";
    }

    public void addFactor(Factor factor) {
        this.factors.add(factor);
    }

    public Polymial toPoly() {
        Polymial poly = new Polymial();
        poly.addMonomial(new Monomial(BigInteger.ONE, 0));
        for (Factor factor : factors) {
            poly = poly.multPoly(poly, factor.toPoly());
        }
        if (this.sign == -1) {
            for (Monomial monomial : poly.getPolymial()) {
                monomial.setCoeff(monomial.getCoeff().negate());
            }
        }
        return poly;
    }

    public HashSet<Factor> getFactors() {
        return factors;
    }

    public ArrayList<Term> derive() {
        ArrayList<Term> ret = new ArrayList<>();
        for (Factor factor : factors) {
            Term term = new Term(this.sign);
            term.addFactor(factor.derive());
            for (Factor f : factors) {
                if (!f.equals(factor)) {
                    term.addFactor(f);
                }
            }
            ret.add(term);
        }
        return ret;
    }

}
