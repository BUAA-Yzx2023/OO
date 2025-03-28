import java.math.BigInteger;

public class Number implements Factor {
    private final BigInteger num;

    public Number(BigInteger num) {
        this.num = num;
    }

    public Polymial toPoly() {
        Polymial poly = new Polymial();
        Monomial monomial = new Monomial(this.num, 0);
        poly.addMonomial(monomial);
        return poly;
    }
}
