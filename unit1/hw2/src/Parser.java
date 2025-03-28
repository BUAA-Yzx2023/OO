import java.math.BigInteger;

public class Parser {
    private final Lexer lexer;

    public Parser(Lexer lexer) {
        this.lexer = lexer;
    }

    public Expr parseExpr() {
        Expr expr = new Expr();

        int sign = 1;
        if (lexer.peek().equals("-")) {
            lexer.next();
            sign = -1;
        } else if (lexer.peek().equals("+")) {
            lexer.next();
        }
        expr.addTerm(parseTerm(sign));

        while (lexer.peek().equals("+") || lexer.peek().equals("-")) {
            sign = lexer.peek().equals("+") ? 1 : -1;
            lexer.next();
            expr.addTerm(parseTerm(sign));
        }
        return expr;
    }

    public Term parseTerm(int sign) {
        Term term = new Term(sign);
        term.addFactor(parseFactor());

        while (lexer.peek().equals("*")) {
            lexer.next();
            term.addFactor(parseFactor());
        }
        return term;
    }

    public Factor parseFactor() {
        if (lexer.peek().equals("(")) {
            lexer.next();
            Expr expr = parseExpr();
            lexer.next();                                           /* TODO */
            if (lexer.peek().equals("^")) {
                lexer.next();
                int index = Integer.parseInt(lexer.peek());
                lexer.next();
                expr.setIndex(index);
            }
            return expr;
        }
        else if (lexer.peek().matches("[0-9]+")) {
            BigInteger num = new BigInteger(lexer.peek());          /* TODO */
            lexer.next();
            if (lexer.peek().equals("^")) {
                lexer.next();
                int index = Integer.parseInt(lexer.peek());
                lexer.next();
                num = num.pow(index);
                return new Number(num);
            }
            return new Number(num);
        }
        else if (lexer.peek().equals("-")) {
            lexer.next();
            BigInteger num = new BigInteger(lexer.peek());          /* TODO */
            lexer.next();
            return new Number(num.negate());
        }
        else if (lexer.peek().equals("+")) {
            lexer.next();
            BigInteger num = new BigInteger(lexer.peek());          /* TODO */
            lexer.next();
            return new Number(num);
        }
        else if (lexer.peek().matches("x")) {
            String var = lexer.peek();
            lexer.next();
            int index = 1;
            if (lexer.peek().equals("^")) {
                lexer.next();
                index = Integer.parseInt(lexer.peek());
                lexer.next();
            }
            return new Var(var, index);
        }
        else if (lexer.peek().equals("sin") || lexer.peek().equals("cos")) {
            return parseTrianFactor();
        }
        else if (lexer.peek().equals("f")) {
            return parseFuncFactor();
        }
        else {
            System.out.println("Error");
            return null;
        }
    }

    public FuncFactor parseFuncFactor() {
        lexer.next();
        lexer.next();
        Integer n = Integer.valueOf(lexer.peek());
        lexer.next();
        lexer.next();
        lexer.next();
        Factor factor1 = parseFactor();
        Factor factor2 = null;
        Integer n2 = n;
        if (lexer.peek().equals(",")) {
            lexer.next();
            factor2 = parseFactor();
        }
        lexer.next();
        return new FuncFactor(n2, factor1, factor2);
    }

    public Trian parseTrianFactor() {
        String type = lexer.peek();
        lexer.next();
        lexer.next();
        Factor factor = parseFactor();
        lexer.next();
        String type2 = type;
        int index = 1;
        if (lexer.peek().equals("^")) {
            lexer.next();
            index = Integer.parseInt(lexer.peek());
            lexer.next();
        }
        return new Trian(factor, type2, index);
    }
}
