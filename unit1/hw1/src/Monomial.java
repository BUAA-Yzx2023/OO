import java.math.BigInteger;

public class Monomial {
    private BigInteger coeff;
    private int index;

    public Monomial(BigInteger coeff, int index) {
        this.coeff = coeff;
        this.index = index;
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
}
