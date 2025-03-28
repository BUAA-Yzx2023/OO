import java.math.BigInteger;
import java.util.ArrayList;

public class Polymial {
    private ArrayList<Monomial> polymial;

    public Polymial() {
        this.polymial = new ArrayList<Monomial>();
    }

    public void addMonomial(Monomial monomial) {
        //遍历列表，如果指数相同，则合并
        for (Monomial m : this.polymial) {
            if (m.getIndex() == monomial.getIndex()) {
                m.setCoeff(m.getCoeff().add(monomial.getCoeff()));
                return;
            }
        }
        this.polymial.add(monomial);
    }

    public Polymial addPoly(Polymial p1, Polymial p2) {
        //result为p1的深拷贝
        Polymial result = new Polymial();
        for (Monomial mono : p1.polymial) {
            result.addMonomial(new Monomial(mono.getCoeff(), mono.getIndex()));
        }

        for (Monomial monoP2 : p2.polymial) {
            boolean found = false;
            for (Monomial monoResult : result.polymial) {
                if (monoResult.getIndex() == monoP2.getIndex()) {
                    // 如果指数相同，合并系数
                    monoResult.setCoeff(monoResult.getCoeff().add(monoP2.getCoeff()));
                    found = true;
                    break;
                }
            }
            if (!found) {
                // 如果指数不存在，直接添加该项
                result.addMonomial(new Monomial(monoP2.getCoeff(), monoP2.getIndex()));
            }
        }
        return result;
    }

    public Polymial multPoly(Polymial p1, Polymial p2) {
        Polymial result = new Polymial();
        for (Monomial monoP1 : p1.polymial) {
            for (Monomial monoP2 : p2.polymial) {
                // 创建一个新的单项式，并计算系数和指数
                BigInteger coeff = monoP1.getCoeff().multiply(monoP2.getCoeff());
                int index = monoP1.getIndex() + monoP2.getIndex();
                Monomial newMono = new Monomial(coeff, index);
                result.addMonomial(newMono);
            }
        }
        return result;
    }

    public ArrayList<Monomial> getPolymial() {
        return polymial;
    }
}
