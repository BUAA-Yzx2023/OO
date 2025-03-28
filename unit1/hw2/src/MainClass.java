import java.util.Scanner;

public class MainClass {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        FuncRecur.Scanf(scanner);
        String input = scanner.nextLine();
        Preprocessing preprocessing = new Preprocessing(input);
        input = preprocessing.getPreprocessed();
        Lexer lexer = new Lexer(input);
        Parser parser = new Parser(lexer);
        Expr expr = parser.parseExpr();
        System.out.println(expr);
    }
}

