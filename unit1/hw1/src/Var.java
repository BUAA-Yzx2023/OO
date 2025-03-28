import java.math.BigInteger;

public class Var implements Factor {
    private final String var;
    private final int index;

    public Var(String var, int index) {
        this.var = var;
        this.index = index;
    }

    public Polymial toPoly() {
        Polymial poly = new Polymial();
        Monomial mono = new Monomial(BigInteger.ONE, index);
        poly.addMonomial(mono);
        return poly;
    }
}
