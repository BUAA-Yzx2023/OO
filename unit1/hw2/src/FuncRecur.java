import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class FuncRecur {
    // 定义符号变量
    private static String arg1;
    private static String arg2;
    private static String n_1x;
    private static String n_1y;
    private static String n_2x;
    private static String n_2y;
    private static Map<String, String> functionMap;

    public static void Scanf(Scanner scanner) {
        // 读入一行整数
        int n = scanner.nextInt();
        scanner.nextLine();
        if (n > 0) {
            functionMap = parseRecursiveDefinition(scanner);
        }
    }

    private static Map<String, String> parseRecursiveDefinition(Scanner scanner) {
        Map<String, String> functionMap = new HashMap<>();
        for (int i = 0; i < 3; i++) {
            String line = scanner.nextLine().trim();
            // 去掉空白符
            line = line.replaceAll("\\s", "");
            // 判断是 f(0)、f(1) 还是 f(n)
            if (line.contains("f{0}")) {
                functionMap.put("f0", extractExpression(line));
            } else if (line.contains("f{1}")) {
                functionMap.put("f1", extractExpression(line));
            } else if (line.contains("f{n}")) {
                arg1 = String.valueOf(line.charAt(5));
                arg2 = String.valueOf(line.charAt(7));
                // 如果是一元函数
                line = extractExpression(line);
                functionMap.put("fn", line);
                if (arg2.equals("x") || arg2.equals("y")) {
                    String[] parts = extractPara2Array(line);
                    n_1x = parts[0];
                    n_1y = parts[1];
                    n_2x = parts[2];
                    n_2y = parts[3];
                } else {
                    String[] parts = extractPara1Array(line);
                    n_1x = parts[0];
                    n_1y = null;
                    n_2x = parts[1];
                    n_2y = null;
                }
            }
        }
        return functionMap;
    }

    private static String extractExpression(String line) {
        // 去掉 "f{...}(x, y) = "，提取等号后面的部分
        return line.split("=")[1].trim();
    }

    public static String computeFn(int n, String x, String y) {
        String theFn = "f" + n;
        if (functionMap.containsKey(theFn)) {
            String result = functionMap.get(theFn);
            result = result.replace(arg1, "#").replace(arg2, "$");
            return result.replace("#", "(" + x + ")").replace("$", "(" + y + ")");
        } else {
            String fnminus1 = computeFn(n - 1, n_1x, n_1y);
            String fnminus2 = computeFn(n - 2, n_2x, n_2y);
            String result = functionMap.get("fn");
            String fn1 = "f{n-1}(" + n_1x + "," + n_1y + ")";
            String fn2 = "f{n-2}(" + n_2x + "," + n_2y + ")";
            result = result.replace(fn1,
                    "#").replace(fn2, "$");
            result = result.replace("#",
                    "(" + fnminus1 + ")").replace("$", "(" + fnminus2 + ")");
            functionMap.put(theFn, result);
            result = result.replace(arg1, "#").replace(arg2, "$");
            return result.replace("#", "(" + x + ")").replace("$", "(" + y + ")");
        }
    }

    public static String computeFn(int n, String x) {
        String theFn = "f" + n;
        if (functionMap.containsKey(theFn)) {
            return functionMap.get(theFn).replace(arg1, "(" + x + ")");
        } else {
            String fnminus1 = computeFn(n - 1, n_1x);
            String fnminus2 = computeFn(n - 2, n_2x);
            String result = functionMap.get("fn");
            String fn1 = "f{n-1}(" + n_1x + ")";
            String fn2 = "f{n-2}(" + n_2x + ")";
            result = result.replace(fn1,
                    "(" + fnminus1 + ")").replace(fn2, "(" + fnminus2 + ")");
            functionMap.put(theFn, result);
            result = result.replace(arg1, "(" + x + ")");
            return result;
        }
    }

    private static String[] extractPara2Array(String line) {
        int top = -1;
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            result.append(c);
            if (c == 'f' && line.charAt(i + 4) == '2') {
                top = 0;
            } else if (top >= 0 && c == '(') {
                top++;
            } else if (top >= 0 && c == ')') {
                top--;
                if (top == 0) {
                    break;
                }
            }
        }
        // 定义正则表达式
        String regex1 = "f\\{n-1\\}\\(([^,]+),(.+)\\).+f";
        String regex2 = "f\\{n-2\\}\\(([^,]+),(.+)\\)";
        // 匹配 f{n-1}(x, y)
        String[] n1params = extractParametersFromRegex(result.toString(), regex1);
        // 匹配 f{n-2}(x, y^2)
        String[] n2params = extractParametersFromRegex(result.toString(), regex2);
        // 返回结果
        return new String[]{n1params[0], n1params[1], n2params[0], n2params[1]};
    }

    private static String[] extractPara1Array(String line) {
        int top = -1;
        StringBuilder result = new StringBuilder();
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            result.append(c);
            if (c == 'f' && line.charAt(i + 4) == '2') {
                top = 0;
            } else if (top >= 0 && c == '(') {
                top++;
            } else if (top >= 0 && c == ')') {
                top--;
                if (top == 0) {
                    break;
                }
            }
        }
        // 定义正则表达式
        String regex1 = "f\\{n-1\\}\\((.+)\\).+f";
        String regex2 = "f\\{n-2\\}\\((.+)\\)";
        // 匹配 f{n-1}(x, y)
        String[] n1params = extractParametersFromRegex(result.toString(), regex1);
        // 匹配 f{n-2}(x, y^2)
        String[] n2params = extractParametersFromRegex(result.toString(), regex2);
        // 返回结果
        return new String[]{n1params[0], n2params[0]};
    }

    private static String[] extractParametersFromRegex(String line, String regex) {
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(line);

        if (matcher.find()) {
            // 提取参数
            String param1 = matcher.group(1).trim(); // 第一个参数
            // 如果第二个参数为空，则设置为默认值null
            String param2 = matcher.groupCount() > 1 ? matcher.group(2).trim() : null;
            return new String[]{param1, param2};
        } else {
            throw new IllegalArgumentException("无法匹配参数: " + regex);
        }
    }
}