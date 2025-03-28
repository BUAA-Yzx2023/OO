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
}
