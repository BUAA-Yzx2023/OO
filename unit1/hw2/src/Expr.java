import java.math.BigInteger;
import java.util.HashSet;

public class Expr implements Factor {
    private final HashSet<Term> terms;
    private int index;

    public Expr() {
        this.index = 1;
        this.terms = new HashSet<>();
    }

    public String getType() {
        return "expr";
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

    @Override
    public String toString() {
        Polymial temPoly = this.toPoly();
        return temPoly.toString();
    }

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
