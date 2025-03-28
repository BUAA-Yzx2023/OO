package Factor;

public class Var implements Factor {
    
    private String name;
    
    public Var(String name) {
        this.name = name;
    }
    
    @Override
    public String toString() {
        return name;
    }
    
    @Override
    public Factor derive() {
        Term term = new Term();
        /* TODO 2 */
        term.addFactor(new Number("1"));
        /*finished*/
        return term;
    }
    
    @Override
    public Factor clone() {
        return new Var(name);
    }
}
