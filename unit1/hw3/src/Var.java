import java.math.BigInteger;

public class Var implements Factor {
    private final String var;
    private final int index;

    public Var(String var, int index) {
        this.var = var;
        this.index = index;
    }

    public String getType() {
        return "var";
    }

    public Polymial toPoly() {
        Polymial poly = new Polymial();
        Monomial mono = new Monomial(BigInteger.ONE, index);
        poly.addMonomial(mono);
        return poly;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        if (this.index == 0) {
            return "1";
        }
        sb.append(var);
        if (index > 1) {
            sb.append("^");
            sb.append(index);
        }
        return sb.toString();
    }

    public Factor derive() {
        if (index == 0) {
            return new Number(BigInteger.ZERO);
        }
        Expr ret = new Expr();
        Term term = new Term(1);
        term.addFactor(new Number(BigInteger.valueOf(index)));
        term.addFactor(new Var(var, index - 1));
        ret.addTerm(term);
        return ret;
    }
}
