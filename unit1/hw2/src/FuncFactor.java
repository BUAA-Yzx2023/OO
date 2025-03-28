public class FuncFactor implements Factor {
    private Factor factor1;
    private Factor factor2;
    private Integer n1;

    public FuncFactor(Integer n, Factor factor1, Factor factor2) {
        this.n1 = n;
        this.factor1 = factor1;
        this.factor2 = factor2;
    }

    public String getExpand(Integer n, Factor factor1, Factor factor2) {
        if (factor2 == null) {
            return FuncRecur.computeFn(n, factor1.toString());
        }
        return FuncRecur.computeFn(n, factor1.toString(), factor2.toString());
    }

    public Polymial toPoly() {
        String s = getExpand(n1, factor1, factor2);
        Preprocessing preprocessing = new Preprocessing(s);
        s = preprocessing.getPreprocessed();
        Lexer lexer = new Lexer(s);
        Parser parser = new Parser(lexer);
        Expr expr = parser.parseExpr();
        return expr.toPoly();
    }

    public String getType() {
        return "FuncFactor";
    }

    @Override
    public String toString() {
        return this.toPoly().toString();
    }

}
