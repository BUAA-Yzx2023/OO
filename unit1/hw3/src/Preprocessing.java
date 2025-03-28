public class Preprocessing {
    private String expression;

    public Preprocessing(String input) {
        this.expression = input;
    }

    public String getPreprocessed() {
        this.expression = this.expression.replaceAll("\\s+", "");
        // 循环删除多余的++、+-、--、-+
        while (this.expression.contains("^+") || this.expression.contains("++")
                || this.expression.contains("--") || this.expression.contains("+-")
                || this.expression.contains("-+") || this.expression.contains("*+")) {
            this.expression = this.expression.replaceAll("\\+\\+", "+");
            this.expression = this.expression.replaceAll("--", "+");
            this.expression = this.expression.replaceAll("\\+\\-", "-");
            this.expression = this.expression.replaceAll("\\-\\+", "-");
            this.expression = this.expression.replaceAll("\\^\\+", "^");
            this.expression = this.expression.replaceAll("\\*\\+", "*");
        }
        return this.expression;
    }

}
