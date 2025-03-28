public class FuncFactor implements Factor {
    private final Factor factor1;
    private final Factor factor2;
    private final Integer n1;
    private final String name;

    public FuncFactor(String name, Integer n, Factor factor1, Factor factor2) {
        this.name = name;
        this.n1 = n;
        this.factor1 = factor1;
        this.factor2 = factor2;
    }

    public String getExpand(Integer n, Factor factor1, Factor factor2) {
        if (factor2 == null) {
            return FuncHandle.computeFn(n, factor1.toString());
        }
        return FuncHandle.computeFn(n, factor1.toString(), factor2.toString());
    }

    public String getExpand(String s, Factor factor1, Factor factor2) {
        if (factor2 == null) {
            return FuncHandle.computeFn(s, factor1.toString());
        }
        return FuncHandle.computeFn(s, factor1.toString(), factor2.toString());
    }

    public Expr toExpr() {
        String s = null;
        if (this.name.equals("f")) {
            s = getExpand(n1, factor1, factor2);
        } else {
            s = getExpand(name, factor1, factor2);
        }
        Preprocessing preprocessing = new Preprocessing(s);
        s = preprocessing.getPreprocessed();
        Lexer lexer = new Lexer(s);
        Parser parser = new Parser(lexer);
        Expr expr = parser.parseExpr();
        return expr;
    }

    public Polymial toPoly() {
        Expr expr = this.toExpr();
        return expr.toPoly();
    }

    public String getType() {
        return "FuncFactor";
    }

    @Override
    public String toString() {
        return this.toPoly().toString();
    }

    public Factor derive() {
        Expr expr = this.toExpr();
        return expr.derive();
    }

}
