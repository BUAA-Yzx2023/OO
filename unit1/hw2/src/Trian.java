import java.math.BigInteger;

public class Trian implements Factor {
    private Factor factor;
    private final String type;
    private final int index;

    public Trian(Factor factor, String type, int index) {
        this.factor = factor;
        this.type = type;
        this.index = index;
    }

    public Factor getFactor() {
        return factor;
    }

    public String getType() {
        return type;
    }

    public Polymial toPoly() {
        Polymial poly = new Polymial();
        Number num = new Number(BigInteger.ONE);
        Polymial numPoly = num.toPoly();
        if (this.index == 0) {
            return numPoly;
        }
        Monomial mono = new Monomial(BigInteger.ONE, 0);
        if (this.type.equals("sin")) {
            Polymial factorPoly = this.factor.toPoly();
            if (factorPoly.toString().equals("0")) {
                return poly;
            }
            mono.addSinFac(factorPoly, this.index);
        } else {
            Polymial factorPoly = this.factor.toPoly();
            if (factorPoly.toString().equals("0")) {
                return numPoly;
            }
            mono.addCosFac(factorPoly, this.index);
        }
        poly.addMonomial(mono);
        return poly;
    }

    @Override
    public String toString() {
        return this.toPoly().toString();
    }

    public int getIndex() {
        return index;
    }
}
